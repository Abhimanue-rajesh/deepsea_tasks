document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("tbody tr").forEach((row) => {
        const link = row.querySelector("th a, td a");

        if (!link) return;

        row.style.cursor = "pointer";

        row.addEventListener("click", function (e) {
            if (
                e.target.closest("a, button, input, select, textarea, label") ||
                e.target.closest("[role='button']")
            ) {
                return;
            }

            window.location.href = link.href;
        });
    });
});
