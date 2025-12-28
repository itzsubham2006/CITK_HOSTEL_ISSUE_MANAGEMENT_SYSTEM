// ===============mega-menu=================
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




// --------------------------------------analytics------------------------
document.getElementById('total-issues').innerText = document.getElementById('total-issues').dataset.value;
document.getElementById('total-upvotes').innerText = document.getElementById('total-upvotes').dataset.value;
document.getElementById('pending-count').innerText = document.getElementById('pending-count').dataset.value;
document.getElementById('resolved-count').innerText = document.getElementById('resolved-count').dataset.value;

const statusCanvas = document.getElementById('statusChart');
const statusCounts = {
    Pending: parseInt(statusCanvas.dataset.pending),
    "In Progress": parseInt(statusCanvas.dataset.inprogress),
    Resolved: parseInt(statusCanvas.dataset.resolved)
};

new Chart(statusCanvas.getContext('2d'), {
    type: 'doughnut',
    data: {
        labels: Object.keys(statusCounts),
        datasets: [{
            data: Object.values(statusCounts),
            backgroundColor: ['#ffa000', '#03a9f4', '#2e7d32']
        }]
    },
    options: {}
});


const categoryCanvas = document.getElementById('categoryChart');
const categories = JSON.parse(categoryCanvas.dataset.categories);
const categoryCounts = JSON.parse(categoryCanvas.dataset.counts);

new Chart(categoryCanvas.getContext('2d'), {
    type: 'bar',
    data: {
        labels: categories,
        datasets: [{
            label: 'Issues',
            data: categoryCounts,
            backgroundColor: '#198754'
        }]
    },
    options: {}
});


const topIssuesData = JSON.parse(document.querySelector('.top-issues').dataset.topissues);
const topIssuesList = document.getElementById('top-issues-list');

topIssuesData.forEach(issue => {
    const li = document.createElement('li');
    li.innerHTML = `${issue.category} — <strong>${issue.upvotes}</strong> upvotes`;
    topIssuesList.appendChild(li);
});

