# AI Waste Segregation Assistant ♻️

> A beginner-level Agentic AI web application built for a college internship demonstration.  
> Aligned with **SDG 12 – Responsible Consumption and Production**.

---

## 1. Project Objective

Build a simple AI-powered web application where a user uploads an image of a waste item and the AI:

- Identifies the item
- Classifies it into a waste category
- Recommends the correct disposal method

---

## 2. SDG 12 Connection

**Sustainable Development Goal 12** focuses on responsible consumption and production.  
Proper waste segregation is one of the most practical actions individuals can take to reduce landfill waste, support recycling, and lower pollution.  
This project makes waste classification accessible to everyone with a phone or computer.

---

## 3. Problem Statement

People often mix different types of household waste together — plastic, paper, glass, organic, and metal — making recycling and proper waste management difficult.  
Without clear guidance, recyclable materials end up in landfills unnecessarily.

---

## 4. Solution

An Agentic AI web application where:

1. The user uploads a photo of a waste item.
2. A **Waste Management Agent** uses Google Gemini Vision to identify and classify the item.
3. The app recommends the correct disposal bin with a short explanation.

---

## 5. Features

- 📷 Image upload (click or drag-and-drop)
- 🔍 AI-powered waste identification using Google Gemini Vision
- ♻️ Classification into 6 waste categories
- 🗑️ Disposal recommendation with explanation
- 🕒 Analysis history stored in browser (localStorage)
- 📱 Responsive design (works on mobile, tablet, desktop)
- 🔐 API key kept securely on the server — never exposed to the browser

---

## 6. Agentic AI Workflow

```
User
  ↓
Image Upload (browser)
  ↓
Flask Backend (receives image)
  ↓
Waste Management Agent (app.py → waste_agent())
  ↓
Google Gemini Vision (identifies item + category)
  ↓
Disposal Map (maps category → recommendation)
  ↓
JSON Response
  ↓
Frontend Result Card (Detected Item, Category, Disposal, Why)
```

The **Waste Management Agent** is a single Python function (`waste_agent`) that:
1. Sends the image to Gemini with a structured prompt
2. Parses the JSON response
3. Maps the category to a pre-defined disposal recommendation

---

## 7. Technology Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Frontend    | HTML, CSS, JavaScript       |
| Backend     | Python, Flask               |
| AI Vision   | Google Gemini 2.0 Flash     |
| AI SDK      | google-genai                |
| Config      | python-dotenv               |
| Production  | gunicorn (WSGI server)      |
| Deployment  | Render (free tier)          |

---

## 8. Project Structure

```
waste-app/
├── app.py               ← Flask server + Waste Management Agent
├── requirements.txt     ← Python dependencies
├── .env.example         ← API key template (copy to .env)
├── .gitignore           ← Keeps .env and cache out of Git
├── render.yaml          ← Render deployment configuration
├── README.md            ← This file
└── templates/
    └── index.html       ← Complete web UI
```

---

## 9. Local Setup

```bash
# 1. Clone or download the project
cd waste-app

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key (see section below)

# 5. Run the app
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## 10. Gemini API Configuration

1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account (free)
3. Click **"Create API key"**
4. Copy the key

Create a file named `.env` in the `waste-app/` folder:

```
GEMINI_API_KEY=your_actual_api_key_here
```

> ⚠️ Never share or commit your `.env` file. It is already listed in `.gitignore`.

---

## 11. Deployment Instructions (Render — Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/waste-app.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to **https://render.com** and sign up (free)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub account and select your repository
4. Render will auto-detect `render.yaml` — confirm the settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add the environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: your actual API key
6. Click **"Deploy"**

Render will give you a public URL like: `https://waste-app-xxxx.onrender.com`

---

## 12. Waste Categories

| Category | Disposal             |
|----------|----------------------|
| Plastic  | Plastic/recycling bin |
| Paper    | Paper/recycling bin  |
| Glass    | Glass/recycling bin  |
| Metal    | Metal/recycling bin  |
| Organic  | Organic/compost bin  |
| Other    | General waste / special collection |

---

## 13. Limitations

- Results depend on image quality — use clear, well-lit photos
- The free Gemini API tier has usage limits
- The Waste Management Agent uses fixed disposal rules (no external database)
- Only single-item images are supported (one waste item per photo works best)

---

## 14. Future Improvements

- Multi-language support
- Camera capture on mobile devices
- Location-based recycling centre finder
- More granular sub-categories (e.g. PET vs HDPE plastic)
- Offline mode with a local model

---

## Author

Built as a college internship project demonstrating Agentic AI for SDG 12.
