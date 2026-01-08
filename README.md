****🧠 TalentScout AI – Hiring Assistant Chatbot****


📌** Project Overview**

TalentScout AI is an AI-powered hiring assistant designed to conduct structured, fair, and skill-based technical interviews through a conversational interface.

The chatbot acts as a virtual interviewer that:

Collects candidate personal and professional information

Dynamically asks technical questions based on the candidate’s skill set

Stores complete interview data (candidate details + Q&A) securely in MongoDB

Provides a clean, industry-grade UI experience similar to modern ATS platforms

This project demonstrates the practical application of LLMs, prompt engineering, Streamlit UI, and database integration in a real-world hiring scenario.

⚙️ Installation Instructions

Follow these steps to run the application locally.

**1️⃣ Clone the Repository**
git clone https://github.com/JK110/TalentScout.git
cd TalentScout

**2️⃣ Create and Activate Virtual Environment**
python -m venv myvenv


**Windows**

myvenv\Scripts\activate


Mac/Linux

source myvenv/bin/activate

**3️⃣ Install Dependencies**
pip install -r requirements.txt

**4️⃣ Setup Environment Variables**

Create a .env file in the project root:

HF_TOKEN=your_huggingface_api_token
HF_MODEL_ID=your_model_id
MONGO_URI=your_mongodb_connection_string

**5️⃣ Run the Application**
streamlit run app.py


The app will be available at:

http://localhost:8501

**🚀 Usage Guide**

Open the application in your browser.

The AI interviewer greets the candidate and starts the interview.

Candidate provides:

Name

Contact details

Education

Experience

Technical skills

Based on the provided skills, the AI:

Generates relevant technical questions

Evaluates responses conversationally

On completion:

The interview is automatically saved in MongoDB

Candidate can exit safely using exit, quit, or bye

**💡 Note:**
No webcam, screen recording, or invasive monitoring is used. The system focuses purely on skill evaluation.

**🛠 Technical Details**
📚 Libraries & Tools Used

**Streamlit** – Frontend UI and chat interface

**Hugging Face Inference API** – LLM-powered responses

**PyMongo** – MongoDB database integration

**Python-dotenv** – Environment variable management

**Certifi** – Secure TLS/SSL database connections

**🤖 Model Details**

Uses a Hugging Face-hosted Large Language Model (LLM)

The model is accessed via InferenceClient

Designed for:

Natural language understanding

Technical question generation

Structured data extraction

**🏗 Architecture Overview**
      User (Browser)
            ↓
Streamlit UI (Chat Interface)
            ↓
LLM (Hugging Face Inference API)
            ↓
Structured Data Extraction (Prompt-based)
            ↓
MongoDB (Candidate Records)


Each interview session stores:

Full chat history

Extracted candidate profile

Technical questions & answers

Timestamp and interview status

**🧩 Prompt Design Strategy**

Prompt engineering is a core part of this project.

🔹 Information Gathering Prompt

Designed to politely collect personal and professional details

Ensures conversational flow without overwhelming the candidate

🔹 Technical Question Generation

Questions are generated dynamically based on:

Candidate’s declared tech stack

Experience level (implicit from responses)

🔹 Data Extraction Prompt

A dedicated system prompt extracts structured data in strict JSON format, including:

{
  "Name": "",
  "Email": "",
  "Phone": "",
  "Education": "",
  "Experience": "",
  "Tech_Stack": "",
  "Technical_Interview": [
    {
      "Question": "",
      "Candidate_Answer": ""
    }
  ]
}


This separation of prompts ensures:

Reliability

Maintainability

Clean database records

**🚧 Challenges & Solutions**
❗ Challenge 1: Extracting Structured Data from Free-Text Chat

Problem:
LLM responses are unstructured by default.

Solution:
Used a dedicated extraction prompt that enforces strict JSON output and handles missing fields gracefully.

❗ Challenge 2: MongoDB Boolean Check Error

Problem:
PyMongo collections cannot be evaluated using if collection:.

Solution:
Used the correct pattern:

if collection is not None:


This aligns with PyMongo best practices.

❗ Challenge 3: UI Looked Distracting or Unprofessional

Problem:
Default Streamlit styles and input borders caused poor UX.

Solution:

Custom CSS

Calm dark theme

Clean input design

Sidebar for trust & guidance

Industry-style layout similar to ATS platforms

❗ Challenge 4: Maintaining Logic While Improving UI

Problem:
UI changes risked breaking core logic.

Solution:
UI enhancements were done purely via CSS and layout, ensuring:

No backend changes

No prompt changes

No database logic changes

**✅ Future Enhancements**

Recruiter/Admin dashboard

Resume upload and parsing

Skill scoring & confidence metrics

Role-based interview flows

Deployment on Streamlit Cloud / AWS / Docker

**📄 License**

This project is for educational and demonstration purposes.
You are free to extend and customize it.

[Live demo]([https://myportfolio.com](https://talentscout-ai-hiringassistant.streamlit.app/))
