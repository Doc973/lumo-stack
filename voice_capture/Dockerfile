#---
# Dockerfile per il servizio di cattura e trascrizione vocale
# Basato su Python 3.11‑slim
#---

FROM python:3.11-slim   # immagine di base

#---
# Dipendenze del sistema (audio + runtime)
#---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsndfile1 \
        ffmpeg \
        curl \
        wget \
        git \
        python3-pip \
        libportaudio2 \
        libasound2 \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

#---
# Librerie Python (Vosk, sounddevice, Flask)
#---
RUN pip install --no-cache-dir \
    vosk==0.3.45 \
    sounddevice \
    numpy \
    flask

#---
# Cartella di lavoro
#---
WORKDIR /app

#---
# Copia lo script di avvio
#---
COPY listen.py .

#---
# Porta su cui l'API espone i comandi
#---
EXPOSE 8500

#---
# Avvio del servizio
#---
CMD ["python", "listen.py"]
