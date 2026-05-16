document.addEventListener("DOMContentLoaded", function () {
    // console.log("Ticket autosave loaded");

    function saveChangelist() {
        const saveButton = document.querySelector(
            'button[type="submit"][form="changelist-form"][name="_save"]'
        );

        if (saveButton) {
            saveButton.click();
        }
    }

    // Normal select change
    document.addEventListener("change", function (event) {
        if (
            event.target.matches('select[name*="routing"]') ||
            event.target.matches('select[name*="completion_status"]')
        ) {
            console.log("Field changed. Saving...");
            saveChangelist();
        }
    });

    // Select2 change
    if (window.django && django.jQuery) {
        django.jQuery(document).on(
            "select2:select select2:clear",
            'select[name*="routing"], select[name*="completion_status"]',
            function () {
                console.log("Select2 changed. Saving...");
                saveChangelist();
            }
        );
    }
});
