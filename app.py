# app.py
import os
import certifi
import streamlit as st
import json
import datetime
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pymongo import MongoClient

# ---------------- IMPORT SYSTEM PROMPT ----------------
try:
    from prompt import SYSTEM_PROMPT
except ImportError:
    st.error("❌ prompt.py not found")
    st.stop()

# ---------------- SSL PATCH ----------------
os.environ["SSL_CERT_FILE"] = certifi.where()

# ---------------- CONFIG ----------------
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL_ID")
MONGO_URI = os.getenv("MONGO_URI")

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🐧",
    layout="wide"   # REQUIRED for sidebar
)

# ---------------- UI (SIMPLE & SAFE) ----------------
st.markdown("""
<style>
body {
    background-color: #020617;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* --- REMOVE RED BORDER COMPLETELY FROM CHAT INPUT --- */

/* Wrapper */
[data-testid="stChatInput"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Inner container */
[data-testid="stChatInput"] > div {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Textarea */
[data-testid="stChatInput"] textarea {
    border: 1px solid #334155 !important;   /* neutral border */
    border-radius: 20px !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Focus / active / visible states */
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] textarea:active,
[data-testid="stChatInput"] textarea:focus-visible {
    border: 1px solid #334155 !important;
    outline: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR (LEFT – SIMPLE) ----------------
with st.sidebar:
    st.title("🧠 TalentScout AI")

    status = "🟢 In Progress" if not st.session_state.get("interview_complete", False) else "✅ Completed"
    st.write(f"**Status:** {status}")
    st.write(f"**Date:** {datetime.datetime.now().strftime('%d %b %Y')}")

    st.divider()

    st.subheader("📊 Interview Progress")
    answered = len([m for m in st.session_state.get("messages", []) if m["role"] == "user"])

    TOTAL_STEPS = 13  # 8 info fields + 5 technical questions
    progress = min(answered / TOTAL_STEPS, 1.0)

    st.progress(progress)

    st.divider()

    st.subheader("💡 Tips")
    st.write("- Explain your approach")
    st.write("- Be clear & structured")
    st.write("- Type `exit` to quit anytime")

# ---------------- HEADER ----------------
st.title("🐧 TalentScout Hiring Assistant")
st.caption("Enterprise-grade AI technical interviews • Secure • Structured • Fair")

# ---------------- DATABASE (UNCHANGED) ----------------
@st.cache_resource
def init_db():
    if not MONGO_URI:
        return None
    cluster = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    return cluster["talentscout_db"]["candidates"]

collection = init_db()

# ---------------- AI CLIENT (UNCHANGED) ----------------
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# ---------------- SAVE FUNCTION (UNCHANGED) ----------------
def save_to_mongo(chat_history):
    extraction_prompt = [
        {"role": "system", "content": """
Extract candidate details as JSON:
{
 "Name":"",
 "Email":"",
 "Phone":"",
 "Education":"",
 "Experience":"",
 "Tech_Stack":"",
 "Technical_Interview":[{"Question":"","Candidate_Answer":""}]
}
Return ONLY JSON.
"""},
        {"role": "user", "content": str(chat_history)}
    ]

    try:
        response = client.chat_completion(messages=extraction_prompt, max_tokens=1000, stream=False)
        raw = response.choices[0].message.content.replace("```json", "").replace("```", "")
        extracted = json.loads(raw)
    except Exception:
        extracted = {"error": "Extraction failed"}

    record = {
        "timestamp": datetime.datetime.now(),
        "status": "completed",
        "candidate_summary": extracted,
        "full_chat_history": chat_history
    }

    if collection is not None:
        collection.insert_one(record)

# ---------------- CHAT STATE (UNCHANGED) ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I am the TalentScout AI. Write 'start' to begin ."}
    ]
    st.session_state.interview_complete = False

# ---------------- DISPLAY CHAT (UNCHANGED) ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- USER INPUT (UNCHANGED LOGIC) ----------------
if prompt := st.chat_input("Type your answer here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.lower() in ["exit", "quit", "bye"]:
        with st.chat_message("assistant"):
            with st.spinner("Saving interview..."):
                save_to_mongo(st.session_state.messages)
                st.success("Interview saved. You may close this tab.")
        st.stop()

    if not st.session_state.interview_complete:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat_completion(
                    messages=st.session_state.messages,
                    max_tokens=500,
                    stream=False
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                if any(p in reply for p in ["Thank you for your time", "recruitment team will review", "Good luck"]):
                    st.session_state.interview_complete = True
                    save_to_mongo(st.session_state.messages)
                    st.success("Interview completed successfully!")
