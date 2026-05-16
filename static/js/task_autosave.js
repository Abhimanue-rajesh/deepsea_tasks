document.addEventListener("DOMContentLoaded", function () {
    // console.log("Task autosave script loaded.");

    document.addEventListener("change", function (event) {
        const field = event.target;

        if (field.closest('[data-label="status"]')) {
            const saveButton = document.querySelector(
                'button[type="submit"][form="changelist-form"][name="_save"]'
            );

            if (saveButton) {
                saveButton.click();
            }
        }
    });
});
