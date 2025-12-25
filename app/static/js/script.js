document.querySelectorAll(".sp-mega-parent").forEach(menu => {
    menu.addEventListener("mouseenter", () => {
        menu.classList.add("active");
    });

    menu.addEventListener("mouseleave", () => {
        menu.classList.remove("active");
    });
});





// ------------------------------------animatedr counting---------------------------------
const counters = document.querySelectorAll('.counter');

const runCounter = (counter) => {
    const target = +counter.dataset.target;
    let count = 0;
    const speed = target / 80;

    const update = () => {
        count += speed;
        if (count < target) {
            counter.innerText = Math.ceil(count);
            requestAnimationFrame(update);
        } else {
            counter.innerText = target;
        }
    };
    update();
};

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            runCounter(entry.target);
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.6 });

counters.forEach(counter => observer.observe(counter));





// ------------------------dark-mode_toggle-------------------------
const toggle = document.getElementById("darkToggle");

toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    toggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});
