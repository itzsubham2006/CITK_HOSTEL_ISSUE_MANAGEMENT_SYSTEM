document.addEventListener("DOMContentLoaded", () => {

  /* COUNT-UP ANIMATION */
  document.querySelectorAll(".count").forEach(el => {
    const target = +el.dataset.value;
    let current = 0;
    const step = Math.max(1, target / 40);

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(current);
      }
    }, 25);
  });

  /* STATUS DONUT */
  const sc = document.getElementById("statusChart");
  new Chart(sc, {
    type: "doughnut",
    data: {
      labels: ["Pending", "In Progress", "Resolved"],
      datasets: [{
        data: [
          sc.dataset.pending,
          sc.dataset.inprogress,
          sc.dataset.resolved
        ],
        backgroundColor: ["#fb923c", "#38bdf8", "#22c55e"],
        cutout: "72%",
        borderWidth: 0
      }]
    },
    options: {
      plugins: {
        legend: {
          position: "top",
          labels: { color: "#e5e7eb", boxWidth: 10 }
        }
      }
    }
  });

  /* CATEGORY BAR */
  const cc = document.getElementById("categoryChart");
  new Chart(cc, {
    type: "bar",
    data: {
      labels: JSON.parse(cc.dataset.categories),
      datasets: [{
        data: JSON.parse(cc.dataset.counts),
        backgroundColor: "#38bdf8",
        borderRadius: 6
      }]
    },
    options: {
      scales: {
        x: { ticks: { color: "#9ca3af" }, grid: { display: false }},
        y: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,.05)" }}
      },
      plugins: { legend: { display: false } }
    }
  });

  /* WEEKLY LINE (PREMIUM) */
  const wc = document.getElementById("weeklyChart");
  const ctx = wc.getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, 0, 260);
  gradient.addColorStop(0, "rgba(56,189,248,.35)");
  gradient.addColorStop(1, "rgba(56,189,248,0)");

  new Chart(wc, {
    type: "line",
    data: {
      labels: JSON.parse(wc.dataset.labels),
      datasets: [{
        data: JSON.parse(wc.dataset.values),
        borderColor: "#38bdf8",
        backgroundColor: gradient,
        fill: true,
        tension: .4,
        pointRadius: 3
      }]
    },
    options: {
      scales: {
        x: { ticks: { color: "#9ca3af" }, grid: { display: false }},
        y: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,.05)" }}
      },
      plugins: { legend: { display: false } }
    }
  });

});
