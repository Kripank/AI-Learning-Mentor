AI Learning Mentor 🎓
A beginner-level AI chatbot web application built for a college internship demonstration.
Aligned with SDG 4 – Quality Education.
1. Project Objective
Build a simple AI-powered web application where students can chat with an AI Learning Mentor to:
- Understand difficult academic concepts
- Get simple explanations
- Generate practice questions and quizzes
- Create study plans
- Summarize topics
2. SDG 4 Connection
Sustainable Development Goal 4 focuses on Quality Education.
Students may struggle to understand difficult topics, prepare for exams, or organize their study time. This project provides an accessible AI learning assistant for quick and simple learning support.
3. Problem Statement
Students often have difficulty understanding complex academic concepts and may not always have immediate access to personalized learning support.
Creating study plans, summaries, and practice questions manually can also take time.
4. Solution
An AI-powered web chatbot where:
1. The student enters a question or learning request.
2. The Flask backend sends the conversation to the Groq API.
3. The AI Learning Mentor generates a student-friendly response.
4. The response is displayed in the chat interface.
5. Features
💬 Simple AI chat interface
📚 Student-friendly topic explanations
📝 Quiz and practice-question generation
📅 Simple study-plan generation
📖 Topic summarization
🔄 Follow-up conversation support
🗑️ Clear chat functionality
📱 Responsive design
🔐 API key kept securely on the server
6. AI Workflow
Student
   ↓
Chat Interface
   ↓
Flask Backend
   ↓
AI Learning Mentor
   ↓
Groq API
   ↓
AI Response
   ↓
Frontend Chat Response
The AI Learning Mentor receives the student's message, uses the current conversation context, sends the request to the Groq conversational AI model, and returns the response.
7. Technology Stack
Layer	Technology
Frontend	HTML, CSS, JavaScript
Backend	Python, Flask
AI	Groq Cloud API
Configuration	python-dotenv
Production	Gunicorn
Deployment	Render or other Python-compatible hosting


8. Project Structure
AI-Learning-Mentor/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── concept.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
9. Local Setup
Clone the project
git clone https://github.com/Kripank/AI-Learning-Mentor.git
cd AI-Learning-Mentor
Create a virtual environment (optional)
Windows:
python -m venv venv
venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Configure the API key
Create a .env file:
GROQ_API_KEY=your_actual_groq_api_key_here
Never share or commit the .env file.
Run the application
python app.py
Open:
http://127.0.0.1:5000
10. Groq API Configuration
The application uses Groq Cloud for the AI chatbot.
Store the API key in .env:
GROQ_API_KEY=your_actual_groq_api_key_here
Do not hardcode the API key in Python, HTML, CSS, or JavaScript.
11. Example Conversations
Student:
Explain photosynthesis in simple words.
Student:
Give me 5 questions about photosynthesis.
Student:
Create a 7-day study plan for my exams.
Student:
Explain Newton's second law in a simple way.
12. Main Learning Capabilities
Capability	Purpose
Topic Explanation	Makes difficult concepts easier
Quiz Generation	Helps students practice
Study Planning	Helps organize exam preparation
Summarization	Provides important points
Follow-up Chat	Allows natural conversation


13. Limitations
- Responses depend on the AI model and the quality of the student's question.
- AI-generated information should be checked for important academic work.
- The project does not use a dedicated educational knowledge database.
- This is a beginner-level internship prototype.
- Groq API usage may be subject to account/model limits.
14. Future Improvements
- Multi-language learning support
- Personalized learning profiles
- Subject-specific learning modes
- Progress tracking
- Advanced quiz modes
- Voice interaction
- Educational resource integration
- Teacher/institution dashboards
Author
Kripank Kumbhare
Built as a college internship project demonstrating AI/LLM-based Agentic AI for SDG 4 – Quality Education.
