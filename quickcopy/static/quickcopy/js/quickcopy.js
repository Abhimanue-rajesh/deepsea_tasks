document.addEventListener("DOMContentLoaded", function () {
    const copySvg = `
        <svg xmlns="http://www.w3.org/2000/svg"
             fill="none"
             viewBox="0 0 24 24"
             stroke-width="1.5"
             stroke="currentColor"
             style="width:20px;height:20px">
            <path stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125H4.875A1.125 1.125 0 013.75 20.625V9.75c0-.621.504-1.125 1.125-1.125H8.25m7.5-5.25h3.375c.621 0 1.125.504 1.125 1.125v10.875c0 .621-.504 1.125-1.125 1.125H9.375A1.125 1.125 0 018.25 15.375V4.5c0-.621.504-1.125 1.125-1.125H15.75z" />
        </svg>
    `;

    const checkIcon = `
        <span class="material-symbols-outlined text-base" style="color: green;">
            check
        </span>
    `;

    document.querySelectorAll(".quickcopy-btn").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();

            const rawText = this.dataset.copyText || "";

            const text = rawText
                .replace(/\\u000D\\u000A/g, "\n")
                .replace(/\\r\\n/g, "\n")
                .replace(/\\n/g, "\n")
                .replace(/\\u002D/g, "-");

            const icon = this.querySelector(".copy-icon");

            if (!text || !icon) return;

            navigator.clipboard.writeText(text).then(() => {
                icon.innerHTML = checkIcon;

                setTimeout(() => {
                    icon.innerHTML = copySvg;
                }, 1200);
            });
        });
    });
});
