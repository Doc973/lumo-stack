#!/usr/bin/env python3
"""
Simple Flask service that:
  • /listen/start  – starts microphone capture (Vosk)
  • /listen/stop   – stops capture, writes transcript to /voice_tmp/transcript.txt
"""

import os
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from flask import Flask, jsonify

app = Flask(__name__)

# Queue where audio chunks are stored
audio_q = queue.Queue()

# Path to the Vosk model (must be present inside the container)
MODEL_PATH = "/app/model"          # we will mount the model folder later
if not os.path.isdir(MODEL_PATH):
    raise RuntimeError(f"Vosk model not found in {MODEL_PATH}")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)


def _audio_callback(indata, frames, time, status):
    """Callback called by sounddevice for each audio block."""
    audio_q.put(bytes(indata))


@app.route("/listen/start", methods=["POST"])
def start_listen():
    """Open the microphone stream and start feeding the queue."""
    sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        callback=_audio_callback,
    ).start()
    return jsonify({"msg": "listening started"}), 200


@app.route("/listen/stop", methods=["POST"])
def stop_listen():
    """Stop the stream, collect all queued audio, run Vosk, write transcript."""
    sd.stop()                     # stop the InputStream
    transcript = ""

    while not audio_q.empty():
        data = audio_q.get()
        if recognizer.AcceptWaveform(data):
            res = json.loads(recognizer.Result())
            transcript += res.get("text", "") + " "

    # Flush the final partial result
    final_res = json.loads(recognizer.FinalResult())
    transcript += final_res.get("text", "")

    # Write the cleaned transcript to the shared volume
    out_path = "/voice_tmp/transcript.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(transcript.strip())

    return jsonify({"transcript": transcript.strip()}), 200


if __name__ == "__main__":
    # Flask runs on 0.0.0.0:8500 (exposed in Dockerfile)
    app.run(host="0.0.0.0", port=8500)
