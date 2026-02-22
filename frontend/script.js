const state = {
  sessionId: null,
  totalRounds: 0,
  currentRound: 1,
  averageScore: 0,
};

const el = {
  apiBase: document.getElementById("apiBase"),
  field: document.getElementById("field"),
  customFieldWrap: document.getElementById("customFieldWrap"),
  customField: document.getElementById("customField"),
  interviewType: document.getElementById("interviewType"),
  difficulty: document.getElementById("difficulty"),
  rounds: document.getElementById("rounds"),
  resume: document.getElementById("resume"),
  jobDescription: document.getElementById("jobDescription"),
  startBtn: document.getElementById("startBtn"),
  summaryBtn: document.getElementById("summaryBtn"),
  resetBtn: document.getElementById("resetBtn"),
  interviewPanel: document.getElementById("interviewPanel"),
  feedbackPanel: document.getElementById("feedbackPanel"),
  finalPanel: document.getElementById("finalPanel"),
  summaryPanel: document.getElementById("summaryPanel"),
  questionText: document.getElementById("questionText"),
  answerText: document.getElementById("answerText"),
  submitAnswerBtn: document.getElementById("submitAnswerBtn"),
  feedbackText: document.getElementById("feedbackText"),
  finalReportText: document.getElementById("finalReportText"),
  summaryText: document.getElementById("summaryText"),
  sessionPill: document.getElementById("sessionPill"),
  roundPill: document.getElementById("roundPill"),
  avgPill: document.getElementById("avgPill"),
  logText: document.getElementById("logText"),
};

function apiRoot() {
  return el.apiBase.value.trim().replace(/\/+$/, "");
}

function toggleCustomField() {
  const isCustom = el.field.value === "custom";
  el.customFieldWrap.classList.toggle("hidden", !isCustom);
}

function getSelectedField() {
  if (el.field.value !== "custom") {
    return el.field.value;
  }
  return el.customField.value.trim();
}

function log(message, isError = false) {
  const stamp = new Date().toLocaleTimeString();
  const line = `[${stamp}] ${message}`;
  el.logText.textContent = `${line}\n${el.logText.textContent}`.trim();
  if (isError) {
    el.logText.style.borderColor = "#8b1e3f";
  }
}

async function callApi(path, method, payload) {
  const response = await fetch(`${apiRoot()}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: payload ? JSON.stringify(payload) : undefined,
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error(`Non-JSON response from ${path}`);
  }

  if (!response.ok) {
    throw new Error(data.detail || `HTTP ${response.status}`);
  }

  if (data && data.error) {
    throw new Error(data.error);
  }

  return data;
}

function setPanels({ interview = false, feedback = false, final = false, summary = false }) {
  el.interviewPanel.classList.toggle("hidden", !interview);
  el.feedbackPanel.classList.toggle("hidden", !feedback);
  el.finalPanel.classList.toggle("hidden", !final);
  el.summaryPanel.classList.toggle("hidden", !summary);
}

function renderStatus() {
  el.sessionPill.textContent = state.sessionId ? `Session: ${state.sessionId}` : "No Session";
  el.roundPill.textContent = `Round: ${state.currentRound}/${state.totalRounds || "-"}`;
  el.avgPill.textContent = `Avg: ${state.averageScore || 0}`;
}

function resetSessionState() {
  state.sessionId = null;
  state.totalRounds = 0;
  state.currentRound = 1;
  state.averageScore = 0;
  el.questionText.textContent = "";
  el.answerText.value = "";
  el.feedbackText.textContent = "";
  el.finalReportText.textContent = "";
  el.summaryText.textContent = "";
  setPanels({ interview: false, feedback: false, final: false, summary: false });
  el.summaryBtn.disabled = true;
  renderStatus();
}

async function startInterview() {
  try {
    const selectedField = getSelectedField();
    if (!selectedField) {
      alert("Please enter a custom field.");
      return;
    }

    el.startBtn.disabled = true;
    const payload = {
      field: selectedField,
      interview_type: el.interviewType.value,
      difficulty: Number(el.difficulty.value),
      total_rounds: Number(el.rounds.value),
      resume: el.resume.value.trim(),
      job_description: el.jobDescription.value.trim(),
    };

    const data = await callApi("/start-interview", "POST", payload);

    state.sessionId = data.session_id;
    state.totalRounds = payload.total_rounds;
    state.currentRound = 1;
    state.averageScore = 0;

    el.questionText.textContent = data.question || "";
    el.answerText.value = "";
    el.feedbackText.textContent = "";
    el.finalReportText.textContent = "";
    el.summaryText.textContent = "";

    setPanels({ interview: true, feedback: false, final: false, summary: false });
    el.summaryBtn.disabled = false;
    renderStatus();
    log("Interview started.");
  } catch (error) {
    log(`Start failed: ${error.message}`, true);
    alert(`Could not start interview: ${error.message}`);
  } finally {
    el.startBtn.disabled = false;
  }
}

function formatFeedback(feedback) {
  if (!feedback || typeof feedback !== "object") {
    return String(feedback || "");
  }
  return [
    `Score: ${feedback.score}`,
    `Communication: ${feedback.communication_score}`,
    `Technical: ${feedback.technical_score}`,
    `Confidence: ${feedback.confidence_score}`,
    "",
    `Strengths: ${feedback.strengths}`,
    "",
    `Weaknesses: ${feedback.weaknesses}`,
  ].join("\n");
}

async function submitAnswer() {
  if (!state.sessionId) {
    alert("Start an interview first.");
    return;
  }

  const answer = el.answerText.value.trim();
  if (!answer) {
    alert("Please write an answer first.");
    return;
  }

  try {
    el.submitAnswerBtn.disabled = true;
    const data = await callApi("/submit-answer", "POST", {
      session_id: state.sessionId,
      answer,
    });

    el.feedbackText.textContent = formatFeedback(data.feedback);
    setPanels({ interview: true, feedback: true, final: false, summary: false });

    state.averageScore = data.average_score || state.averageScore;

    if (data.interview_complete) {
      el.finalReportText.textContent = data.final_report || "";
      setPanels({ interview: false, feedback: true, final: true, summary: false });
      log("Interview complete.");
    } else {
      state.currentRound = data.current_round || state.currentRound + 1;
      el.questionText.textContent = data.next_question || "";
      el.answerText.value = "";
      log(`Round ${state.currentRound - 1} submitted. Next question loaded.`);
    }

    renderStatus();
  } catch (error) {
    log(`Submit failed: ${error.message}`, true);
    alert(`Could not submit answer: ${error.message}`);
  } finally {
    el.submitAnswerBtn.disabled = false;
  }
}

async function loadSummary() {
  if (!state.sessionId) {
    alert("No active session.");
    return;
  }

  try {
    const data = await callApi(`/session-summary/${state.sessionId}`, "GET");
    el.summaryText.textContent = JSON.stringify(data, null, 2);
    setPanels({
      interview: !el.interviewPanel.classList.contains("hidden"),
      feedback: !el.feedbackPanel.classList.contains("hidden"),
      final: !el.finalPanel.classList.contains("hidden"),
      summary: true,
    });
    state.averageScore = data.average_score || state.averageScore;
    renderStatus();
    log("Session summary updated.");
  } catch (error) {
    log(`Summary failed: ${error.message}`, true);
    alert(`Could not load summary: ${error.message}`);
  }
}

el.startBtn.addEventListener("click", startInterview);
el.submitAnswerBtn.addEventListener("click", submitAnswer);
el.summaryBtn.addEventListener("click", loadSummary);
el.field.addEventListener("change", toggleCustomField);
el.resetBtn.addEventListener("click", () => {
  el.field.value = "Software Engineering";
  el.customField.value = "";
  toggleCustomField();
  resetSessionState();
  log("UI state reset.");
});

toggleCustomField();
resetSessionState();
