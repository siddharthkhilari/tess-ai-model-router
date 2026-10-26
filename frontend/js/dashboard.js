// Dashboard JavaScript with Chart.js integration (need.md Section 22, 30)

let modelChart = null;
let latencyChart = null;
let costChart = null;
let complexityChart = null;

async function loadDashboard() {
  try {
    const [statsRes, reqsRes] = await Promise.all([
      fetch("/api/dashboard/stats"),
      fetch("/api/requests?limit=25")
    ]);

    const stats = await statsRes.json();
    const reqs = await reqsRes.json();

    updateMetricsCards(stats);
    renderCharts(stats);
    updateRequestsTable(reqs);
  } catch (err) {
    console.error("Dashboard data load error:", err);
  }
}

function updateMetricsCards(stats) {
  document.getElementById("totalRequests").innerText = stats.total_requests;
  document.getElementById("avgLatency").innerText = `${stats.average_latency_ms} ms`;
  document.getElementById("totalCost").innerText = `₹${stats.estimated_total_cost.toFixed(2)}`;
  document.getElementById("totalSavings").innerText = `₹${stats.estimated_total_savings.toFixed(2)}`;
  document.getElementById("savingsPct").innerText = `${stats.overall_saving_percentage}% vs Large model baseline`;
  document.getElementById("cacheHitRate").innerText = `${stats.cache_hit_rate}%`;
  document.getElementById("cacheHitsSub").innerText = `${stats.cache_hits} queries served instantly`;
}

function renderCharts(stats) {
  // Chart 1: Model Usage Donut
  const ctxModel = document.getElementById("modelUsageChart").getContext("2d");
  if (modelChart) modelChart.destroy();
  modelChart = new Chart(ctxModel, {
    type: "doughnut",
    data: {
      labels: ["Small Model (SLM)", "Medium Model", "Large Model (LLM)"],
      datasets: [{
        data: [
          stats.model_usage.small || 0,
          stats.model_usage.medium || 0,
          stats.model_usage.large || 0
        ],
        backgroundColor: ["#10b981", "#3b82f6", "#8b5cf6"],
        borderWidth: 2,
        borderColor: "#ffffff"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });

  // Chart 2: Latency by Model
  const ctxLatency = document.getElementById("latencyChart").getContext("2d");
  if (latencyChart) latencyChart.destroy();
  latencyChart = new Chart(ctxLatency, {
    type: "bar",
    data: {
      labels: ["Small Model", "Medium Model", "Large Model"],
      datasets: [{
        label: "Avg Latency (ms)",
        data: [
          stats.latency_by_model.small || 0,
          stats.latency_by_model.medium || 0,
          stats.latency_by_model.large || 0
        ],
        backgroundColor: ["#10b981", "#3b82f6", "#8b5cf6"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: "Milliseconds (ms)" } }
      },
      plugins: { legend: { display: false } }
    }
  });

  // Chart 3: Cost by Model
  const ctxCost = document.getElementById("costChart").getContext("2d");
  if (costChart) costChart.destroy();
  costChart = new Chart(ctxCost, {
    type: "bar",
    data: {
      labels: ["Small Model", "Medium Model", "Large Model"],
      datasets: [{
        label: "Total Cost (₹ INR)",
        data: [
          stats.cost_by_model.small || 0,
          stats.cost_by_model.medium || 0,
          stats.cost_by_model.large || 0
        ],
        backgroundColor: ["#10b981", "#3b82f6", "#8b5cf6"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: "Cost (₹ INR)" } }
      },
      plugins: { legend: { display: false } }
    }
  });

  // Chart 4: Complexity Distribution
  const ctxComp = document.getElementById("complexityChart").getContext("2d");
  if (complexityChart) complexityChart.destroy();
  complexityChart = new Chart(ctxComp, {
    type: "bar",
    data: {
      labels: ["LOW (0.0 - 0.39)", "MEDIUM (0.40 - 0.69)", "HIGH (0.70 - 1.0)"],
      datasets: [{
        label: "Request Count",
        data: [
          stats.complexity_distribution.LOW || 0,
          stats.complexity_distribution.MEDIUM || 0,
          stats.complexity_distribution.HIGH || 0
        ],
        backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } }
      },
      plugins: { legend: { display: false } }
    }
  });
}

function updateRequestsTable(reqs) {
  const tbody = document.getElementById("requestsTableBody");
  tbody.innerHTML = "";

  if (!reqs || reqs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No requests processed yet. Try routing a prompt on the AI Router page!</td></tr>`;
    return;
  }

  reqs.forEach(r => {
    const tr = document.createElement("tr");

    let modelBadgeClass = "badge-small";
    if (r.selected_model === "medium") modelBadgeClass = "badge-medium";
    else if (r.selected_model === "large") modelBadgeClass = "badge-large";

    let compClass = "badge-low";
    if (r.complexity_level === "MEDIUM") compClass = "badge-med";
    else if (r.complexity_level === "HIGH") compClass = "badge-high";

    const cacheBadge = r.cache_hit 
      ? `<span class="badge badge-cache-hit">HIT</span>`
      : `<span class="badge badge-cache-miss">MISS</span>`;

    tr.innerHTML = `
      <td>#${r.id}</td>
      <td title="${r.question}" style="max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;">${r.question}</td>
      <td><span style="font-size: 0.78rem; color: #475569;">${r.task_type}</span></td>
      <td><span class="badge ${compClass}">${r.complexity_level}</span></td>
      <td><span class="badge ${modelBadgeClass}">${r.selected_model.toUpperCase()}</span></td>
      <td>${r.latency_ms} ms</td>
      <td>₹${r.estimated_cost.toFixed(2)}</td>
      <td style="color: var(--success); font-weight: 600;">₹${r.estimated_saving.toFixed(2)}</td>
      <td>${cacheBadge}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Initial load
document.addEventListener("DOMContentLoaded", loadDashboard);
