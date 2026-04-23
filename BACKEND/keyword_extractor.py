from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import whisper
import os
import spacy

from keybert import KeyBERT

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- APP INIT ----------------
app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
model = whisper.load_model("base")
kw_model = KeyBERT()
nlp = spacy.load("en_core_web_sm")

# ---------------- PATHS ----------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PDF_FILE = "output.pdf"


# ---------------- TEXT PROCESSING ----------------

def simple_summary(text):
    return text[:300] if text else ""


# ---------- KEYBERT (KEYWORDS) ----------
def extract_keywords(text):
    keywords = kw_model.extract_keywords(text, top_n=8)
    return [k[0] for k in keywords]


# ---------- SPACY PROCESSING ----------
def process_text(text):
    doc = nlp(text)

    sentences = [sent.text for sent in doc.sents]
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return sentences, entities


# ---------- HYBRID ACTION EXTRACTION ----------
def extract_actions(sentences):
    actions = []

    for s in sentences:
        doc = nlp(s)

        if any(token.pos_ == "VERB" for token in doc):
            if any(word in s.lower() for word in ["will", "need", "must", "should", "assign"]):
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
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Entities:</b>", styles["Heading2"]))
    content.append(Paragraph(str(data["entities"]), styles["Normal"]))

    doc.build(content)
    return filename


# ---------------- ROUTES ----------------

@app.get("/")
def home():
    return {"message": "API Running Successfully 🚀"}


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Whisper transcription
        result = model.transcribe(file_path)
        text = result["text"]

        # spaCy processing
        sentences, entities = process_text(text)

        # Final structured data
        data = {
            "transcription": text,
            "summary": simple_summary(text),
            "keywords": extract_keywords(text),
            "action_items": extract_actions(sentences),
            "entities": entities
        }

        # Generate PDF
        generate_pdf(data)

        return FileResponse(
            PDF_FILE,
            media_type="application/pdf",
            filename="meeting-summary.pdf"
        )

    except Exception as e:
        return JSONResponse({"error": str(e)})


@app.get("/download-pdf")
def download_pdf():
    return FileResponse(
        PDF_FILE,
        media_type="application/pdf",
        filename="meeting-summary.pdf"
    )