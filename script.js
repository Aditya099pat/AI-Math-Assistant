const API_URL = "http://127.0.0.1:8000/api/solve";

const chatWindow = document.querySelector("#chatWindow");
const form = document.querySelector("#mathForm");
const input = document.querySelector("#promptInput");
const clearChat = document.querySelector("#clearChat");

function addMessage(role, content, loading = false) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}${loading ? " loading" : ""}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "YOU" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  wrapper.append(avatar, bubble);
  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  return wrapper;
}

function resizeTextarea() {
  input.style.height = "auto";
  input.style.height = `${input.scrollHeight}px`;
}

async function askBackend(question) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
    }),
  });

  if (!response.ok) {
    throw new Error(`Backend request failed with status ${response.status}`);
  }

  const data = await response.json();

  if (!data.success) {
    throw new Error(data.answer || "Backend returned an error.");
  }

  return data.answer;
}

async function handlePrompt(prompt) {
  addMessage("user", prompt);

  const pending = addMessage("assistant", "Thinking", true);

  try {
    const answer = await askBackend(prompt);
    pending.querySelector(".bubble").textContent = answer;
  } catch (error) {
    console.error("Backend connection error:", error);

    pending.querySelector(".bubble").textContent =
      "Could not connect to the Python backend. Make sure FastAPI is running at http://127.0.0.1:8000 and then try again.";
  } finally {
    pending.classList.remove("loading");
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();

  const prompt = input.value.trim();

  if (!prompt) {
    return;
  }

  input.value = "";
  resizeTextarea();

  handlePrompt(prompt);
});

input.addEventListener("input", resizeTextarea);

input.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

clearChat.addEventListener("click", () => {
  chatWindow.innerHTML = "";
  addMessage("assistant", "Chat cleared. Ask me a new math question.");
});

document.addEventListener("click", event => {
  const button = event.target.closest("[data-example]");

  if (!button) {
    return;
  }

  document.querySelectorAll(".tool").forEach(tool => {
    tool.classList.remove("active");
  });

  if (button.classList.contains("tool")) {
    button.classList.add("active");
  }

  input.value = button.dataset.example;
  resizeTextarea();
  input.focus();
});