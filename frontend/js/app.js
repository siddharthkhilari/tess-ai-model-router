// Frontend JavaScript for Prompt Complexity Analyzer

function setPreset(text) {
  document.getElementById("promptInput").value = text;
  handleAnalyze();
}

async function handleAnalyze() {
  const prompt = document.getElementById("promptInput").value.trim();
  if (!prompt) {
    alert("Please enter a prompt.");
    return;
  }

  const btn = document.getElementById("analyzeBtn");
  btn.disabled = true;
  btn.innerText = "Analyzing Complexity...";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: prompt })
    });
    const data = await res.json();
    displayComplexityResult(data);
  } catch (err) {
    alert("Analysis failed: " + err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "<span>🔍 Analyze Complexity</span>";
  }
}

function displayComplexityResult(data) {
  const box = document.getElementById("primaryResultBox");
  box.style.display = "block";

  const hero = document.getElementById("complexityHeroText");
  const scorePill = document.getElementById("complexityScorePill");

  const level = data.complexity_level; // LOW, MEDIUM, HIGH
  hero.innerText = level;
  scorePill.innerText = `Overall Score: ${data.score} / 100`;

  // Apply visual theme
  box.className = "primary-result-container";
  if (level === "LOW") {
    box.classList.add("theme-low");
  } else if (level === "MEDIUM") {
    box.classList.add("theme-medium");
  } else {
    box.classList.add("theme-high");
  }

  // Breakdown values
  const b = data.breakdown || {};
  document.getElementById("bLength").innerText = `${b.length_score || 0} / 20`;
  document.getElementById("bInstr").innerText = `${b.instruction_score || 0} / 20`;
  document.getElementById("bReason").innerText = `${b.reasoning_score || 0} / 25`;
  document.getElementById("bTech").innerText = `${b.technical_score || 0} / 20`;
  document.getElementById("bTask").innerText = `${b.task_score || 0} / 15`;

  // Reasons list
  const list = document.getElementById("reasonsList");
  list.innerHTML = "";
  (data.reasons || []).forEach(r => {
    const li = document.createElement("li");
    li.innerText = r;
    list.appendChild(li);
  });

  // Smooth scroll to result
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Allow Enter key to trigger analysis
document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("promptInput");
  if (textarea) {
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleAnalyze();
      }
    });
  }
});
