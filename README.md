# TalentScout — Hiring Assistant 

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]

A secure, opinionated Streamlit-based AI assistant for conducting structured technical interviews and capturing candidate data. The app uses Hugging Face Inference API to run a conversational model, stores transcripts and extracted candidate summaries in MongoDB, and is driven by a system prompt defined in `prompt.py`.

This README is tailored to the current `app.py` implementation and explains required environment variables, how the app behaves, how data is stored, and how to run it locally.

Table of contents
- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Environment variables (.env)](#environment-variables-env)
- [Quick start (local)](#quick-start-local)
- [Development notes & important details](#development-notes--important-details)
- [Data model (MongoDB)](#data-model-mongodb)
- [Security & privacy notes](#security--privacy-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Streamlit chat UI for running structured, multi-step technical interviews.
- Uses Hugging Face InferenceClient (`huggingface_hub`) to perform chat completions.
- Persists interviews and a JSON-extracted candidate summary to MongoDB.
- Lightweight UI customizations (dark background, custom chat input styling).
- Safe exit workflow: type `exit`, `quit`, or `bye` to save and stop the interview.

## How it works (high level)

1. On start, `app.py` loads a system prompt from `prompt.py` (`SYSTEM_PROMPT`) and places it in the session messages.
2. User interacts via the Streamlit chat input. Each user message is appended to `st.session_state.messages`.
3. On every user input, the app sends the conversation (messages) to the Hugging Face Inference API using `InferenceClient.chat_completion`.
4. The assistant reply is shown, appended to session state, and — when the assistant signals interview completion — the app extracts candidate details (via a second chat completion using a JSON extraction prompt) and stores both the extraction and full chat history to MongoDB.
5. Typing `exit`/`quit`/`bye` triggers saving the interview and stops the app.

## Requirements

- Python 3.9+
- A Hugging Face API token with access to the chosen model
- A running MongoDB instance (or MongoDB Atlas)
- Recommended packages:
  - streamlit
  - huggingface-hub
  - pymongo
  - python-dotenv
  - certifi

You can install the basic dependencies with:
```bash
python -m pip install streamlit huggingface-hub pymongo python-dotenv certifi
```

(Optionally add these to a `requirements.txt` for reproducible installs.)

## Environment variables (.env)

The app reads configuration from environment variables. Create a `.env` file in the repository root (or set env vars in your environment). Example values are shown in `.env.example` (file included in this repo).

Key variables used by `app.py`:
- HF_TOKEN — Hugging Face API token (string)
- HF_MODEL_ID — Hugging Face model id used by `InferenceClient` (example: `"gpt-4o-mini"` or any chat-capable model you have access to)
- MONGO_URI — MongoDB connection URI (example: `mongodb+srv://user:pass@cluster0.mongodb.net/?retryWrites=true&w=majority`)

See the provided `.env.example` for a template.

## Quick start (local)

1. Clone the repository
```bash
git clone https://github.com/JK110/TalentScout.git
cd TalentScout
```

2. Create and edit `.env` (or copy `.env.example`)
```bash
cp .env.example .env
# edit .env to set HF_TOKEN, HF_MODEL_ID, MONGO_URI
```

3. Install dependencies
```bash
python -m pip install -r requirements.txt  # if present
# or
python -m pip install streamlit huggingface-hub pymongo python-dotenv certifi
```

4. Add a `prompt.py` that defines `SYSTEM_PROMPT` (required)
```python
# prompt.py (example)
SYSTEM_PROMPT = "You are an AI interviewer. Ask for candidate details and then technical questions..."
```
The app will show an error and stop if `prompt.py` is missing.

5. Run the Streamlit app
```bash
streamlit run app.py
```

6. Open the UI in the browser (default: http://localhost:8501). The sidebar shows interview progress, tips, and status.

## Development notes & important details

- SSL certificates are patched via `certifi`:
  app sets `SSL_CERT_FILE = certifi.where()` for secure TLS connections to MongoDB and external APIs.
- The app caches the MongoDB collection using `@st.cache_resource` for efficient reuse.
- The app maintains a session-scoped `st.session_state.messages` list containing the system message, assistant prompts, and user answers.
- The app detects interview completion when the assistant's reply contains phrases like:
  - "Thank you for your time"
  - "recruitment team will review"
  - "Good luck"
  When detected, it triggers extraction and saves the interview automatically.
- Exit flow: if the user types `exit`, `quit`, or `bye` the app saves the interview and stops.

## Data model (MongoDB)

Saved document structure (approximate):
- timestamp: Date
- status: "completed" (string)
- candidate_summary: JSON produced by the extraction step. The intended shape is:

```json
{
  "Name": "",
  "Email": "",
  "Phone": "",
  "Education": "",
  "Experience": "",
  "Tech_Stack": "",
  "Technical_Interview": [{"Question": "", "Candidate_Answer": ""}]
}
```

- full_chat_history: the full list of conversation messages (system/assistant/user)

Mongo collection used: `talentscout_db.candidates` (this is created/used by `app.py` via the provided `MONGO_URI`).

## Security & privacy notes

- Candidate data (names, email, phone, resumes, answers) is personally identifiable information (PII). Treat the database and model inputs/outputs as sensitive.
- Do not commit secrets to the repository. Keep `HF_TOKEN` and `MONGO_URI` in environment variables or a local `.env` that is excluded from Git.
- Carefully review your Hugging Face model's privacy and retention policies. Some hosted models may log requests.
- For production use consider:
  - Using an encrypted/managed database (e.g., MongoDB Atlas) with IP allowlists.
  - Rotating API keys and storing secrets in a secure secret manager.
  - Adding authentication and role-based access to the Streamlit UI (not included in `app.py`).

## Troubleshooting

- If `prompt.py` is missing you will see an error in the UI and the app will stop.
- If the app cannot connect to MongoDB, ensure `MONGO_URI` is valid and reachable from your machine.
- If Hugging Face returns auth errors, ensure `HF_TOKEN` is valid and `HF_MODEL_ID` is a model your token can use.

## Contributing

- Please open issues for bugs and feature requests.
- For code changes: fork, create a feature branch, add tests where applicable, and open a pull request with a clear description.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
