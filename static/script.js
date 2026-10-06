const chatBox   = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn   = document.getElementById('send-btn');

// ── Auto-resize textarea ──────────────────────────────────────────────────────
userInput.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// ── Send on Enter (Shift+Enter = new line) ────────────────────────────────────
userInput.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── Fill input from example prompt chips ─────────────────────────────────────
function usePrompt(text) {
  userInput.value = text;
  userInput.focus();
  userInput.style.height = 'auto';
  userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
}

// ── Add a message bubble to the chat box ─────────────────────────────────────
function addMessage(role, text) {
  const wrapper = document.createElement('div');
  wrapper.classList.add('message');

  const sender = document.createElement('span');
  sender.classList.add('sender');

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  bubble.textContent = text;

  if (role === 'user') {
    wrapper.classList.add('user-message');
    sender.textContent = '🎓 You';
  } else if (role === 'ai') {
    wrapper.classList.add('ai-message');
    sender.textContent = '🤖 Mentor';
  } else if (role === 'error') {
    wrapper.classList.add('error-message');
    sender.textContent = '⚠️ Error';
  } else if (role === 'thinking') {
    wrapper.classList.add('ai-message', 'thinking');
    sender.textContent = '🤖 Mentor';
    bubble.textContent = 'Thinking…';
  }

  wrapper.appendChild(sender);
  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
  return wrapper;
}

// ── Send message to Flask backend ────────────────────────────────────────────
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Show user message
  addMessage('user', message);

  // Clear input
  userInput.value = '';
  userInput.style.height = 'auto';
  sendBtn.disabled = true;

  // Show thinking indicator
  const thinkingEl = addMessage('thinking', '');

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await res.json();

    // Remove thinking indicator
    chatBox.removeChild(thinkingEl);

    if (data.error) {
      addMessage('error', data.error);
    } else {
      addMessage('ai', data.reply);
    }
  } catch (err) {
    chatBox.removeChild(thinkingEl);
    addMessage('error', 'Connection error. Please check that the server is running and try again.');
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

// ── Clear chat ────────────────────────────────────────────────────────────────
async function clearChat() {
  try {
    await fetch('/clear', { method: 'POST' });
  } catch (_) {
    // Best-effort server clear
  }

  // Remove all messages except the initial greeting
  chatBox.innerHTML = '';
  addMessage('ai', 'Chat cleared! Feel free to start a new conversation. What would you like to learn?');
}
