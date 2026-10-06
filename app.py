import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from groq import Groq

# Always load .env from the same folder as app.py, regardless of cwd
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # needed for session

# ── Groq configuration ────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = "qwen/qwen3.8-27b"

if GROQ_API_KEY:
    print(f"[GROQ] API key loaded (ends ...{GROQ_API_KEY[-4:]})")
else:
    print("[GROQ] WARNING: GROQ_API_KEY is NOT set.")
    print("[GROQ] Create waste-app/.env and add:  GROQ_API_KEY=your_key_from_console.groq.com")

print(f"[GROQ] Using model: {GROQ_MODEL}")

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an AI Learning Mentor for students. "
    "Help students understand educational topics using clear, simple explanations. "
    "Break difficult concepts into smaller parts. "
    "Give examples when useful. "
    "Help create study plans, summaries, practice questions, and quizzes. "
    "Use bullet points and numbered lists to make answers easy to read. "
    "Encourage students to understand concepts instead of blindly copying answers. "
    "Do not pretend to have real-world teaching credentials. "
    "Do not give dangerous or inappropriate advice. "
    "If you are unsure about something, say so honestly."
)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Initialise conversation history for this session
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({
            "error": (
                "GROQ_API_KEY is missing. "
                "Create a .env file and add your Groq API key: "
                "GROQ_API_KEY=your_key_from_console.groq.com"
            )
        }), 500

    data = request.get_json()
    user_message = (data or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Please enter a message."}), 400

    # Build conversation history
    history = session.get("history", [])
    history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        ai_reply = completion.choices[0].message.content.strip()
    except Exception as exc:
        print(f"[GROQ ERROR] {type(exc).__name__}: {exc}")
        return jsonify({"error": f"Groq API error: {exc}"}), 500

    history.append({"role": "assistant", "content": ai_reply})
    session["history"] = history

    return jsonify({"reply": ai_reply})


@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
