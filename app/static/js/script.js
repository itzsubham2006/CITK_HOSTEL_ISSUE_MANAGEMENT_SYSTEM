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








// ----------------------------------------------------------nav responsive----------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('.sp-nav-list');
    const mobileTriggers = document.querySelectorAll('.mobile-trigger');

 
    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navList.classList.toggle('is-active');
        });
    }

   
    mobileTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const parent = this.parentElement;
            
            
            parent.classList.toggle('is-open');
            
           
            document.querySelectorAll('.sp-mega-parent').forEach(item => {
                if (item !== parent) item.classList.remove('is-open');
            });
        });
    });

    
    document.addEventListener('click', function(e) {
        if (navList.classList.contains('is-active') && !navList.contains(e.target) && e.target !== menuToggle) {
            navList.classList.remove('is-active');
        }
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const closeBtn = document.querySelector('.close-menu');
    const navList = document.querySelector('.sp-nav-list');
    const triggers = document.querySelectorAll('.mobile-trigger');

  
    menuToggle.addEventListener('click', () => {
        navList.classList.add('is-active');
    });

   
    closeBtn.addEventListener('click', () => {
        navList.classList.remove('is-active');
    });

   
    triggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            parent.classList.toggle('is-open');
        });
    });
});