# 🎙️ AI Meeting Summarizer

An AI-powered web application that converts meeting audio into **structured insights** including summary, keywords, action items, and downloadable PDF reports.

---

## 🚀 Features

* 🎧 Upload meeting audio files
* 📝 Automatic transcription using Whisper
* 📋 Smart meeting summary generation
* 🏷️ Keyword extraction
* ✅ Action items detection (with names)
* 📄 Downloadable PDF report
* 🌙 Dark mode UI with modern design
* ⚡ Fast and responsive frontend

---

## 🛠️ Tech Stack

### Frontend

* React (Vite)
* CSS (Custom UI + animations)
* Axios

### Backend

* FastAPI
* Whisper (Speech-to-Text)
* Ollama (LLM for summary)
* ReportLab (PDF generation)

---

## 📂 Project Structure

```
AI MEETING/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Upload.jsx
│   │   │   ├── Results.jsx
│   │   ├── api/
│   │   ├── utils/
│   │   └── ...
│   ├── package.json
│
├── backend/
│   ├── main.py
│   ├── services/
│   ├── uploads/
│   ├── pdfs/
│   └── ...
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 🔹 1. Clone Repository

```
git clone https://github.com/your-username/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

---

### 🔹 2. Backend Setup

```
cd backend
pip install -r requirements.txt
```

Run server:

```
uvicorn main:app --reload
```

👉 Backend runs on:

```
http://localhost:8000
```

---

### 🔹 3. Frontend Setup

```
cd frontend
npm install
npm run dev
```

👉 Frontend runs on:

```
http://localhost:5173
```

---

## 🧠 How It Works

1. User uploads audio file
2. Whisper converts audio → text
3. Ollama processes transcript → summary, keywords, action items
4. Backend generates PDF report
5. Frontend displays structured results

---

## ⚠️ Requirements

* Python 3.9+
* Node.js 18+
* Ollama installed & running locally

  ```
  http://localhost:11434
  ```

---

## 👨‍💻 Author

VAIDARBHI GOYAL
B.Tech Student | Developer

---

⭐ If you like this project, give it a star on GitHub!

