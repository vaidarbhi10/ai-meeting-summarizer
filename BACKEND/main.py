from fastapi import FastAPI, UploadFile, File, HTTPException
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

print("Loading Whisper...")
model = whisper.load_model("tiny")

UPLOAD_DIR = "uploads"
PDF_DIR = "pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)


# ---------------- OLLAMA ----------------
def process_with_ollama(text):
    prompt = f"""
You are a professional AI meeting assistant.

STRICT RULES:
- Do NOT use words like "name", "person"
- Use real names if present in transcript
- If no names, use "Speaker 1", "Speaker 2"
- Keep output structured and clean

FORMAT:

Summary:
Write 4-5 clear sentences summarizing the meeting.

Keywords:
- keyword1
- keyword2
- keyword3

Action Items:
- Person: Task
- Person: Task

Transcript:
{text[:3000]}
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180,
        )

        if res.status_code != 200:
            print("OLLAMA ERROR:", res.text)
            return ""

        return res.json().get("response", "")

    except Exception as e:
        print("OLLAMA ERROR:", str(e))
        return ""


# ---------------- PARSER ----------------
def parse_output(output):
    summary = ""
    keywords = []
    actions = []

    try:
        output = output.replace("**", "").strip()

        # SUMMARY
        if "Summary:" in output:
            summary = output.split("Summary:")[1].split("Keywords:")[0].strip()

        # KEYWORDS
        if "Keywords:" in output:
            k_part = output.split("Keywords:")[1].split("Action Items:")[0]
            keywords = [
                k.strip(" -*\n")
                for k in k_part.split("\n")
                if k.strip()
            ]

        # ACTION ITEMS
        if "Action Items:" in output:
            a_part = output.split("Action Items:")[1]
            actions = [
                a.strip(" -*\n")
                for a in a_part.split("\n")
                if a.strip()
            ]

    except Exception as e:
        print("PARSE ERROR:", str(e))

    return summary, keywords, actions


# ---------------- PDF ----------------
def generate_pdf(data, file_id):
    filename = f"{PDF_DIR}/meeting_{file_id}.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Transcript:</b>", styles["Heading2"]))
    content.append(Paragraph(data["transcription"], styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    content.append(Paragraph(data["summary"], styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Keywords:</b>", styles["Heading2"]))
    content.append(Paragraph(", ".join(data["keywords"]), styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Action Items:</b>", styles["Heading2"]))

    if data["action_items"]:
        for a in data["action_items"]:
            content.append(Paragraph(f"• {a}", styles["Normal"]))
    else:
        content.append(Paragraph("No action items found.", styles["Normal"]))

    doc.build(content)
    return filename


# ---------------- ROUTES ----------------
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        with open(path, "wb") as f:
            f.write(await file.read())

        print("Audio saved")

        # TRANSCRIPTION
        text = model.transcribe(path)["text"]
        print("Transcription done")

        # AI PROCESSING
        ai_output = process_with_ollama(text)
        print("AI OUTPUT:", ai_output[:300])

        summary, keywords, actions = parse_output(ai_output)

        data = {
            "transcription": text,
            "summary": summary,
            "keywords": keywords,
            "action_items": actions,
        }

        generate_pdf(data, file_id)
        print("PDF generated")

        return {
            "transcript": text,
            "summary": summary,
            "keywords": keywords,
            "action_items": actions,
            "pdf_download_url": f"http://localhost:8000/download/{file_id}",
        }

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return JSONResponse({"error": str(e)})


@app.get("/download/{file_id}")
def download(file_id: str):
    file = f"{PDF_DIR}/meeting_{file_id}.pdf"

    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(
        file,
        media_type="application/pdf",
        filename="meeting-summary.pdf"
    )