from pyannote.audio import Pipeline
import torch
import os

# Load HuggingFace token from environment (recommended)
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("Please set your HuggingFace token as environment variable: HUGGINGFACE_TOKEN")

# Load diarization pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HF_TOKEN
)

# Use CPU (since you likely don’t have GPU)
pipeline.to(torch.device("cpu"))


def diarize_audio(file_path: str):
    """
    Takes audio file path and returns speaker segments
    """
    try:
        diarization = pipeline(file_path)

        result = []

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            result.append({
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
                "speaker": speaker
            })

        return result

    except Exception as e:
        return {"error": str(e)}