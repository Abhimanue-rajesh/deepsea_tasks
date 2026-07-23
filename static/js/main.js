function initializeWorldClock() {
    const clocks = [
        {
            id: "india-time",
            timezone: "Asia/Kolkata",
        },
        {
            id: "uae-time",
            timezone: "Asia/Dubai",
        },
        {
            id: "ksa-time",
            timezone: "Asia/Riyadh",
        },
    ];

    function updateClock() {
        const now = new Date();

        // Show today's date only once (using the browser's local date)
        const dateElement = document.getElementById("current-date");

        if (dateElement) {
            dateElement.textContent = now.toLocaleDateString("en-GB", {
                day: "2-digit",
                month: "short",
                year: "numeric",
            });
        }

        clocks.forEach((clock) => {
            const element = document.getElementById(clock.id);

            if (!element) return;

            element.textContent = now.toLocaleTimeString("en-IN", {
                timeZone: clock.timezone,
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
            });
        });
    }

    updateClock();
    setInterval(updateClock, 1000);
}

document.addEventListener("DOMContentLoaded", initializeWorldClock);
