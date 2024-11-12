from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        os.makedirs('uploads', exist_ok=True)
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Gọi hàm xử lý âm thanh
        from utils import process_audio  # Import tại đây nếu cần gọi

        process_audio(file_path)

        # Call speech_to_text.py
        try:
            subprocess.run(["python", "speech_to_text.py"], check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Error running speech_to_text.py: {e}"}), 500

        # Call summarize_meeting.py
        try:
            subprocess.run(["python", "summarize_meeting.py"], check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Error running summarize_meeting.py: {e}"}), 500

        return jsonify({"message": "File uploaded and processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
