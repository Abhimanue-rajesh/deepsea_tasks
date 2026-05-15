import unittest

from django.test import TestCase
from django.test.runner import DiscoverRunner
from django.urls import reverse


class VerboseTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"[✔️] {test}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"[❌] {test}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"[⚠️] {test}")


class VerboseTestRunner(unittest.TextTestRunner):
    resultclass = VerboseTestResult


class CustomTestRunner(DiscoverRunner):
    def get_test_runner_kwargs(self):
        return super().get_test_runner_kwargs() | {"resultclass": VerboseTestResult}

    def run_suite(self, suite, **kwargs):
        return VerboseTestRunner(verbosity=self.verbosity).run(suite)


class TemplateRenderTest(TestCase):
    def test_admin_template_render(self):
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_home_template_render(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_login_template_render(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_template_render(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
