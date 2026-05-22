from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


class EncryptedTextField(models.TextField):
    # Custom Django field extending TextField
    # Behaves like a normal TextField but stores encrypted data

    description = "Encrypted text field"

    def _get_cipher(self):
        # Creates and returns the Fernet encryption object

        key = getattr(settings, "FIELD_ENCRYPTION_KEY", None)
        # Reads encryption key from Django settings

        if not key:
            # If key is missing, stop execution with proper Django error

            raise ImproperlyConfigured("FIELD_ENCRYPTION_KEY is missing in settings.")

        if isinstance(key, str):
            # Fernet requires bytes, not string
            # Convert string key into bytes

            key = key.encode()

        return Fernet(key)
        # Returns Fernet encryption/decryption instance

    def get_prep_value(self, value):
        # Runs BEFORE saving data into database
        # Used to encrypt the value

        value = super().get_prep_value(value)
        # Gets the standard Django-prepared value

        if value in [None, ""]:
            # Do not encrypt empty values

            return value

        if isinstance(value, str) and value.startswith("gAAAA"):
            # Prevents double encryption
            # Fernet encrypted values usually start with "gAAAA"

            return value

        cipher = self._get_cipher()
        # Gets Fernet cipher instance

        return cipher.encrypt(value.encode()).decode()
        # Encrypts text and converts bytes back into string for DB storage

    def from_db_value(self, value, expression, connection):
        # Runs automatically when retrieving value from database
        # Used to decrypt stored data

        if value in [None, ""]:
            # Return empty values directly

            return value

        try:
            cipher = self._get_cipher()
            # Gets Fernet cipher instance

            return cipher.decrypt(value.encode()).decode()
            # Decrypts DB value back into readable text

        except InvalidToken:
            # If decryption fails, return raw value
            # Prevents application crash

            return value

    def to_python(self, value):
        # Converts value into Python datatype
        # Django calls this during model/form handling

        return value
        # Returning value directly because decryption already happens above
