import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

# ── Configure Gemini ──────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Waste Management Agent ────────────────────────────────────────────────────
CATEGORIES = ["Plastic", "Paper", "Glass", "Metal", "Organic", "Other"]

DISPOSAL_MAP = {
    "Plastic": {
        "action": "Put it in the plastic / recycling bin.",
        "explanation": (
            "Plastic takes hundreds of years to decompose. Recycling it "
            "saves energy and reduces pollution. Make sure it is clean and dry."
        ),
    },
    "Paper": {
        "action": "Put it in the paper / recycling bin.",
        "explanation": (
            "Paper is highly recyclable. Keep it dry and free from food stains. "
            "Recycling paper saves trees and reduces landfill waste."
        ),
    },
    "Glass": {
        "action": "Put it in the glass / recycling bin.",
        "explanation": (
            "Glass can be recycled indefinitely without losing quality. "
            "Rinse the item before disposing to avoid contamination."
        ),
    },
    "Metal": {
        "action": "Put it in the metal / recycling bin.",
        "explanation": (
            "Metals like aluminium and steel are 100 % recyclable. "
            "Recycling metal uses far less energy than producing new metal."
        ),
    },
    "Organic": {
        "action": "Put it in the organic / compost bin.",
        "explanation": (
            "Organic waste breaks down naturally and makes excellent compost. "
            "Composting reduces methane emissions from landfills."
        ),
    },
    "Other": {
        "action": "Dispose of it at a general waste or special collection point.",
        "explanation": (
            "This item does not fit standard recycling categories. "
            "Check your local waste authority for proper disposal guidelines."
        ),
    },
}


def waste_agent(image_bytes: bytes, mime_type: str) -> dict:
    """
    Waste Management Agent:
    1. Sends the image to Gemini Vision for identification.
    2. Classifies the detected item into one of the six categories.
    3. Returns the result with a disposal recommendation.
    """
    if not GEMINI_API_KEY:
        return {
            "error": "GEMINI_API_KEY is not set. Please add it to the .env file."
        }

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = (
        "You are a waste classification assistant. "
        "Look at this image and respond ONLY with valid JSON in this exact format:\n"
        '{"item": "<short name of the waste item>", "category": "<one of: Plastic, Paper, Glass, Metal, Organic, Other>"}\n'
        "Do not add any explanation outside the JSON."
    )

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, image_part],
    )
    raw = response.text.strip()

    # Strip markdown code fences if Gemini adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    parsed = json.loads(raw)
    item = parsed.get("item", "Unknown item")
    category = parsed.get("category", "Other")

    # Normalise category in case the model returns a variant
    if category not in CATEGORIES:
        category = "Other"

    disposal = DISPOSAL_MAP[category]
    return {
        "item": item,
        "category": category,
        "action": disposal["action"],
        "explanation": disposal["explanation"],
    }


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    image_bytes = file.read()
    mime_type = file.mimetype or "image/jpeg"

    try:
        result = waste_agent(image_bytes, mime_type)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
