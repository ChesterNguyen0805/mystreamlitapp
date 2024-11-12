import google.generativeai as genai

# Cấu hình API Gemini
genai.configure(api_key="AIzaSyAo5cL01yJ1I_QK93Y_XPAOHxR-pLhtBU8")  # Đảm bảo thay thế YOUR_API_KEY bằng khóa thực của bạn

generation_config = { 
    "temperature": 0,
    "top_p": 0.2,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

def summarize_meeting_from_file(input_file, output_file):
    """Đọc nội dung từ file và gửi đến API Gemini để tóm tắt nội dung."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            transcript = f.read()

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        prompt = f"Tóm tắt những gì bạn nghe được từ cuộc hội thoại và chỉ liệt kê những nội dung chính:\n\n{transcript}"
        
        response = model.start_chat().send_message(prompt)
        summary = response.text

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"Đã lưu nội dung tóm tắt vào file: {output_file}")

    except Exception as e:
        print(f"Lỗi khi gọi API Gemini: {e}")

# Gọi hàm với đường dẫn tới file cuoc_hoi_thoai.txt và file đầu ra noi_dung_chinh.txt
summarize_meeting_from_file('cuoc_hoi_thoai.txt', 'noi_dung_chinh.txt')
