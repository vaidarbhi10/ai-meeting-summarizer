from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()

# ---------------- CORS FIX ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD MODEL ----------------
model = whisper.load_model("base")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PDF_FILE = "output.pdf"


# ---------------- TEXT PROCESSING ----------------
def simple_summary(text):
    return text[:300] if text else ""


def extract_keywords(text):
    words = text.split()
    return list(set(words))[:10]


def extract_actions(text):
    actions = []
    sentences = text.split(".")
    for s in sentences:
        if "will" in s.lower() or "need" in s.lower() or "do" in s.lower():
            actions.append(s.strip())
    return actions


# ---------------- PDF GENERATION ----------------
def generate_pdf(data, filename=PDF_FILE):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Transcription:</b>", styles["Heading2"]))
    content.append(Paragraph(data["transcription"], styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    content.append(Paragraph(data["summary"], styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Keywords:</b>", styles["Heading2"]))
    content.append(Paragraph(", ".join(data["keywords"]), styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Action Items:</b>", styles["Heading2"]))
    content.append(Paragraph(", ".join(data["action_items"]), styles["Normal"]))

    doc.build(content)
    return filename


# ---------------- ROUTES ----------------

@app.get("/")
def home():
    return {"message": "API Running Successfully 🚀"}


# ⚠️ IMPORTANT: THIS MUST MATCH FRONTEND (/upload)
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Transcription
        result = model.transcribe(file_path)
        text = result["text"]

        # Process data
        data = {
            "transcription": text,
            "summary": simple_summary(text),
            "keywords": extract_keywords(text),
            "action_items": extract_actions(text)
        }

        # Generate PDF
        pdf_path = "output.pdf"
        generate_pdf(data, pdf_path)

        # ✅ IMPORTANT FIX: return REAL PDF (not JSON)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="meeting-summary.pdf"
        )

    except Exception as e:
        return JSONResponse({
            "error": str(e)
        })
@app.get("/download-pdf")
def download_pdf():
    return FileResponse(
        PDF_FILE,
        media_type="application/pdf",
        filename="meeting-summary.pdf"
    )