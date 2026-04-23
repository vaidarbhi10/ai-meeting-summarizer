from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import whisper
import os
import requests
import uuid

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- FAST WHISPER ----------------
print("Loading Whisper (tiny for speed)...")
model = whisper.load_model("tiny")
print("Whisper loaded ✅")

UPLOAD_DIR = "uploads"
PDF_DIR = "pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ---------------- OLLAMA ----------------
def process_with_ollama(text):
    try:
        prompt = f"""
Summarize this meeting:

1. Summary
2. Keywords
3. Action Items

Transcript:
{text[:2000]}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        print("OLLAMA STATUS:", response.status_code)
        print("OLLAMA RESPONSE PREVIEW:", response.text[:200])

        if response.status_code != 200:
            return "Error: Ollama failed"

        data = response.json()
        return data.get("response", "No response")

    except Exception as e:
        print("OLLAMA ERROR:", str(e))
        return "Error generating output"

# ---------------- PARSER ----------------
def parse_output(output):
    summary, keywords, actions = "", "", ""

    try:
        if "Keywords:" in output:
            parts = output.split("Keywords:")
            summary = parts[0].replace("Summary:", "").strip()

            if "Action Items:" in parts[1]:
                k, a = parts[1].split("Action Items:")
                keywords = k.strip()
                actions = a.strip()
            else:
                keywords = parts[1].strip()
        else:
            summary = output

    except:
        pass

    return summary, keywords, actions

# ---------------- PDF ----------------
def generate_pdf(data, file_id):
    filename = f"{PDF_DIR}/meeting_{file_id}.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Transcription:</b>", styles["Heading2"]))
    content.append(Paragraph(data["transcription"], styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    content.append(Paragraph(data["summary"], styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Keywords:</b>", styles["Heading2"]))
    content.append(Paragraph(data["keywords"], styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Action Items:</b>", styles["Heading2"]))
    content.append(Paragraph(data["action_items"], styles["Normal"]))

    doc.build(content)
    return filename

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "AI Meeting Summarizer Running 🚀"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("AUDIO SAVED")

        # Whisper
        result = model.transcribe(file_path)
        text = result["text"]

        print("TRANSCRIPTION DONE")

        # Ollama
        ai_output = process_with_ollama(text)

        summary, keywords, actions = parse_output(ai_output)

        data = {
            "transcription": text,
            "summary": summary,
            "keywords": keywords,
            "action_items": actions
        }

        pdf_path = generate_pdf(data, file_id)

        print("PDF GENERATED")

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="meeting-summary.pdf"
        )

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return JSONResponse({"error": str(e)})