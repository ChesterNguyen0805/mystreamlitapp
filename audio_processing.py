from flask import Flask, request
import os
from utils import process_audio  # Cập nhật import từ utils

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Gọi hàm xử lý âm thanh
    process_audio(file_path)

    return "File uploaded and processed successfully", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Chạy server trên localhost với port 5000
