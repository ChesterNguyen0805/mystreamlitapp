import streamlit as st
import os
import pyaudio
import wave
import subprocess
from pyannote.audio import Pipeline
import google.generativeai as genai

# Initialize PyAudio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10  # Change as needed
OUTPUT_WAV_FILE = "recorded_audio.wav"

# Initialize Gemini API configuration
genai.configure(api_key="AIzaSyAo5cL01yJ1I_QK93Y_XPAOHxR-pLhtBU8")
generation_config = {
    "temperature": 0,
    "top_p": 0.2,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

# Initialize pyannote.audio pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# Streamlit App
st.title("Real-Time Conversation Recording and Summarization")
st.write("This app allows you to record a conversation, transcribe it, and get a summary of key points.")

# Step 1: Record Audio
st.header("Step 1: Record Audio")
if st.button("Start Recording"):
    st.write("Recording...")

    # Record audio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to WAV file
    wf = wave.open(OUTPUT_WAV_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    st.success("Recording finished and saved.")

# Step 2: Speaker Diarization
st.header("Step 2: Speaker Diarization")
if st.button("Perform Speaker Diarization"):
    if os.path.exists(OUTPUT_WAV_FILE):
        diarization = pipeline(OUTPUT_WAV_FILE)
        st.write("Speaker Diarization Results:")
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            st.write(f"Speaker {speaker} spoke from {turn.start:.1f}s to {turn.end:.1f}s")
    else:
        st.error("No audio file found. Please record audio first.")

# Step 3: Transcribe and Summarize Conversation
st.header("Step 3: Summarize Conversation")
if st.button("Generate Summary"):
    # Call speech-to-text process (assuming a transcription file is saved as `transcription.txt`)
    transcription_file = "transcription.txt"
    try:
        # Run speech-to-text script and store output in `transcription.txt`
        result = subprocess.run(["python", "speech_to_text.py"], capture_output=True, text=True, check=True)
        with open(transcription_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        st.write("Transcription successful.")

        # Summarize the transcription
        with open(transcription_file, 'r', encoding='utf-8') as f:
            transcript = f.read()
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
        prompt = f"Tóm tắt những gì bạn nghe được từ cuộc hội thoại và chỉ liệt kê những nội dung chính:\n\n{transcript}"
        response = model.start_chat().send_message(prompt)
        summary = response.text
        st.write("Summary of the conversation:")
        st.write(summary)

    except Exception as e:
        st.error(f"Error in summarization: {e}")

# Ensure the necessary audio files and summaries are deleted after use if desired
if st.button("Clear Files"):
    if os.path.exists(OUTPUT_WAV_FILE):
        os.remove(OUTPUT_WAV_FILE)
    if os.path.exists(transcription_file):
        os.remove(transcription_file)
    st.success("Temporary files cleared.")
