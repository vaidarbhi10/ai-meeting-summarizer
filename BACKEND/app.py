from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.speech_to_text import transcribe_audio
from services.diarization import diarize_audio
from services.summarizer import generate_mom
from services.keyword_extractor import extract_keywords
from file_handler import save_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import uuid

app = FastAPI()

PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_pdf(data, file_id):
    filename = os.path.join(PDF_DIR, f"meeting_{file_id}.pdf")
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("<b>Transcript</b>", styles["Heading2"]))
    content.append(Paragraph(data["transcript"], styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    content.append(Paragraph(data["summary"], styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Keywords</b>", styles["Heading2"]))
    keywords_text = ", ".join(data["keywords"]) if isinstance(data["keywords"], list) else str(data["keywords"])
    content.append(Paragraph(keywords_text, styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Action Items</b>", styles["Heading2"]))
    if isinstance(data["action_items"], list) and data["action_items"]:
        for action in data["action_items"]:
            content.append(Paragraph(f"• {action}", styles["BodyText"]))
    else:
        content.append(Paragraph(str(data["action_items"] or "None"), styles["BodyText"]))

    doc.build(content)
    return filename


@app.get("/")
def home():
    return {"message": "AI Smart Meeting Analyzer Running 🚀"}

@app.post("/upload")
async def upload_and_analyze(file: UploadFile = File(...)):

    file_path = save_file(file)

    # Step 1: Speech-to-Text
    transcript = transcribe_audio(file_path)

    # Step 2: Speaker Identification
    speakers = diarize_audio(file_path)

    # Step 3: Keywords
    keywords = extract_keywords(transcript)

    # Step 4: MoM + Action Items
    mom, actions = generate_mom(transcript)

    file_id = str(uuid.uuid4())
    pdf_data = {
        "transcript": transcript,
        "summary": mom,
        "keywords": keywords,
        "action_items": actions,
    }

    generate_pdf(pdf_data, file_id)

    return {
        "transcript": transcript,
        "speakers": speakers,
        "keywords": keywords,
        "summary": mom,
        "action_items": actions,
        "pdf_download_url": f"/download/{file_id}",
    }


@app.get("/download/{file_id}")
def download_pdf(file_id: str):
    filename = os.path.join(PDF_DIR, f"meeting_{file_id}.pdf")
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(filename, media_type="application/pdf", filename="meeting-summary.pdf")