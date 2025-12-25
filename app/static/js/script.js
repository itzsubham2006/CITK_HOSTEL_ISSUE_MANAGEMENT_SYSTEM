document.querySelectorAll(".sp-mega-parent").forEach(menu => {
    menu.addEventListener("mouseenter", () => {
        menu.classList.add("active");
    });

    menu.addEventListener("mouseleave", () => {
        menu.classList.remove("active");
    });
});
