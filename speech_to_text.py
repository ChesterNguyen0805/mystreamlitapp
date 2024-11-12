import pyaudio
import wave
import numpy as np
from pyannote.audio import Pipeline

# Khởi tạo pyannote.audio pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# Cấu hình âm thanh
FORMAT = pyaudio.paInt16  # Định dạng âm thanh
CHANNELS = 1              # Số lượng kênh
RATE = 16000              # Tần số mẫu (16kHz)
CHUNK = 1024              # Kích thước chunk

# Hàm ghi âm và lưu file wav
def record_audio(output_filename, record_seconds=10):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Bắt đầu ghi âm...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Đã ghi âm xong!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Lưu âm thanh vào file WAV
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Hàm phân biệt người nói bằng pyannote
def diarize_audio(input_filename):
    # Sử dụng pyannote để phân biệt người nói trong file WAV
    diarization = pipeline(input_filename)

    # In ra các đoạn hội thoại với thông tin người nói
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"Người nói {speaker} nói từ {turn.start:.1f}s đến {turn.end:.1f}s")

# Gọi hàm để ghi âm và sau đó phân biệt người nói
output_wav_file = "cuoc_hoi_thoai.wav"
record_audio(output_wav_file, record_seconds=10)  # Chỉnh sửa thời gian nếu cần
diarize_audio(output_wav_file)
