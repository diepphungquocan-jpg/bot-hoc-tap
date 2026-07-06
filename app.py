import streamlit as st
from google import genai
from google.genai import types

API_KEY = "AQ.Ab8RN6JdB3rPoDl6-5zycDCXnl7CLPsOzmSI4SzSZ5nT8Zm-sQ"
client = genai.Client(api_key=API_KEY)

# Giao diện
st.set_page_config(page_title="Trợ Lý Học Tập AI Q.A Pro", page_icon="🎓", layout="wide")
st.title("🎓 Trợ Lý Học Tập AI Thông Minh Q.A (Bản Pro)")

# 1. THANH CHỌN CHẾ ĐỘ HỌC TẬP (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Cài đặt trợ lý")
    che_do = st.selectbox(
        "Chọn chế độ hỗ trợ học tập:",
        ["Gia sư tổng hợp", "Chuyên gia Giải Toán/Lý/Hóa", "Luyện Tiếng Anh", "Tạo câu hỏi trắc nghiệm ôn tập"]
    )
    st.write("---")
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

# Định nghĩa tính cách AI tùy theo chế độ bạn chọn
system_prompts = {
    "Gia sư tổng hợp": "Bạn là gia sư hỗ trợ học tập. Hãy trả lời ngắn gọn, chia nhỏ kiến thức, dùng gạch đầu dòng dễ hiểu.",
    "Chuyên gia Giải Toán/Lý/Hóa": "Bạn là chuyên gia tự nhiên. Khi giải bài, hãy ghi rõ: Tóm tắt đề, Công thức áp dụng, Giải chi tiết từng bước.",
    "Luyện Tiếng Anh": "You are a friendly English teacher. Reply in English (with brief Vietnamese translation if needed). Correct any grammar mistakes made by the user.",
    "Tạo câu hỏi trắc nghiệm ôn tập": "Khi người dùng đưa một chủ đề, hãy tạo ra 3 câu hỏi trắc nghiệm kèm đáp án giải thích để họ tự kiểm tra kiến thức."
}

# 2. LƯU LỊCH SỬ CHAT (Để AI không bị quên những câu nói trước)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các câu chat cũ ra màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Ô NHẬP LIỆU DẠNG CHATBOX XỊN
if prompt := st.chat_input("Nhập câu hỏi học tập của bạn tại đây..."):
    # Hiển thị tin nhắn của bạn
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AI phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompts[che_do],
                        temperature=0.7
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Lỗi kết nối API hoặc mạng. Vui lòng kiểm tra lại.")
