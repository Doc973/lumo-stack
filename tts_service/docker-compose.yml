# --------------------------------------------------------------
# Dockerfile per il micro‑servizio TTS usato da Lumo
# Basato su Python 3.11‑slim (immagine leggera)
# --------------------------------------------------------------

FROM python:3.11-slim

# -----------------------------------------------------------------
# Dipendenze di sistema necessarie per la sintesi audio
# -----------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsndfile1 \
        ffmpeg \
        curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# -----------------------------------------------------------------
# Installazione dipendenze Python
# -----------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------
# Copia del codice sorgente
# -----------------------------------------------------------------
COPY . .

EXPOSE 8002

# -----------------------------------------------------------------
# Health‑check (curl è ora disponibile nell’immagine)
# -----------------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=5 \
  CMD ["curl", "-f", "http://localhost:8002/healthz"]

# -----------------------------------------------------------------
# Avvio del server FastAPI (uvicorn)
# -----------------------------------------------------------------
CMD ["uvicorn", "tts_api:app", "--host", "0.0.0.0", "--port", "8002"]
