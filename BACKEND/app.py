from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.speech_to_text import transcribe_audio
from services.diarization import diarize_audio
from services.summarizer import generate_mom
from services.keyword_extractor import extract_keywords
from file_handler import save_file

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    return {
        "transcript": transcript,
        "speakers": speakers,
        "keywords": keywords,
        "mom": mom,
        "action_items": actions
    }