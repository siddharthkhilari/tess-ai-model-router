// Model Comparison JavaScript (need.md Section 22, 29)

function setCompPreset(text) {
  document.getElementById("compPromptInput").value = text;
}

async function handleCompare() {
  const prompt = document.getElementById("compPromptInput").value.trim();
  if (!prompt) {
    alert("Please enter a question or prompt first.");
    return;
  }

  const btn = document.getElementById("compareBtn");
  btn.disabled = true;
  btn.innerText = "Running multi-tier inference...";

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: prompt })
    });
    const data = await res.json();
    renderComparison(data);
  } catch (err) {
    alert("Comparison failed: " + err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "<span>📊 Run Side-by-Side Comparison</span>";
  }
}

function renderComparison(data) {
  // Recommendation banner
  const banner = document.getElementById("recommendationBanner");
  banner.style.display = "block";
  document.getElementById("recModelName").innerText = data.recommended_model;
  document.getElementById("recReasonText").innerText = data.recommendation_reason;

  // Comparison Grid
  const grid = document.getElementById("comparisonGrid");
  grid.style.display = "grid";
  grid.innerHTML = "";

  data.models.forEach(m => {
    const card = document.createElement("div");
    card.className = "comp-card" + (m.is_recommended ? " recommended" : "");

    let badgeHtml = "";
    if (m.is_recommended) {
      badgeHtml = `<div class="comp-badge">★ RECOMMENDED</div>`;
    }

    let tierColor = "#10b981";
    if (m.tier === "medium") tierColor = "#3b82f6";
    if (m.tier === "large") tierColor = "#8b5cf6";

    card.innerHTML = `
      ${badgeHtml}
      <div style="font-size: 1.15rem; font-weight: 700; color: ${tierColor}; margin-bottom: 0.75rem;">
        ${m.model_name}
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.88rem;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed var(--border); padding-bottom: 0.25rem;">
          <span style="color: var(--text-muted);">Estimated Quality:</span>
          <strong>${m.expected_quality} / 100</strong>
        </div>
        <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed var(--border); padding-bottom: 0.25rem;">
          <span style="color: var(--text-muted);">Cost per Request:</span>
          <strong>₹${m.estimated_cost.toFixed(2)}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed var(--border); padding-bottom: 0.25rem;">
          <span style="color: var(--text-muted);">Expected Latency:</span>
          <strong>${m.expected_latency.toFixed(1)}s</strong>
        </div>
        <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed var(--border); padding-bottom: 0.25rem;">
          <span style="color: var(--text-muted);">Actual Latency:</span>
          <strong style="color: #2563eb;">${m.actual_latency_ms} ms</strong>
        </div>
      </div>

      <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.4rem;">
        Generated Output Preview:
      </div>
      <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 0.75rem; font-size: 0.84rem; line-height: 1.5; max-height: 250px; overflow-y: auto; white-space: pre-wrap;">
${m.response}
      </div>
    `;
    grid.appendChild(card);
  });

  banner.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
