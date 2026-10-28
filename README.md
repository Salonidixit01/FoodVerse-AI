# FoodVerse AI — Multimodal Food Intelligence Platform

Full-stack capstone prototype built with **React + Vite** and **FastAPI**. Modules include food recognition/nutrition summaries, freshness screening, kitchen hygiene video workflow, audio upload workflow, cooking assistance and sample personalized meal plans.

## Capability transparency
This is a runnable **prototype with clearly labelled demo outputs**. The backend validates uploads but does not yet run real computer vision, video understanding, speech recognition or an LLM. Demo results must not be represented as real media analysis. Food safety, nutrition and hygiene decisions require independent verification.

## Project structure
```text
FoodVerse_AI/
├── frontend/ (React + Vite)
│   ├── src/App.jsx
│   ├── src/main.jsx
│   ├── src/styles.css
│   └── package.json
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

## Run on Windows

### 1. Backend — first terminal
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
If PowerShell blocks activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000`.

API docs: http://localhost:8000/docs

### 2. Frontend — second terminal
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL, usually http://localhost:5173. Frontend API default is `http://localhost:8000`.

## Deployment outline
- Frontend: Vercel/Netlify, root directory `frontend`, build command `npm run build`, output `dist`.
- Backend: Render or another ASGI host, root directory `backend`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Set frontend `VITE_API_URL` to the deployed backend URL and backend `CORS_ORIGINS` to the deployed frontend URL.

## Production roadmap
Integrate a real multimodal model for image recognition/freshness, frame sampling and video analysis for hygiene, speech-to-text for audio, a grounded LLM for cooking, validated nutrition data and allergy handling. Add automated tests, rate limits, upload scanning, privacy controls and monitoring before production use.
