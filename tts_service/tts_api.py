from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pathlib

app = FastAPI()

class TTSRequest(BaseModel):
    text: str

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/tts")
def generate(request: TTSRequest):
    # --- QUI inserisci la tua logica TTS reale ---
    # Per ora creiamo un file WAV fittizio vuoto (placeholder)
    out_dir = pathlib.Path("/app/outputs/tts")
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_path = out_dir / "placeholder.wav"
    wav_path.touch()   # crea file vuoto
    return {"message": "TTS generated (placeholder)", "wav_path": str(wav_path)}
