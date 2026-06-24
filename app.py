import streamlit as st
from gradio_client import Client

# ตั้งค่าหน้าเพจแบบ Centered และใส่ไอคอน
st.set_page_config(page_title="Shan TTS Generator", page_icon="🎙️", layout="centered")

# Custom CSS ขั้นสูงสำหรับแอนิเมชัน
st.markdown("""
    <style>
    /* CSS สำหรับเอฟเฟกต์ Shimmer ที่หัวข้อ */
    .shimmer-text {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(to right, #6e8efb, #a777e3, #6e8efb);
        background-size: 200% auto;
        color: #fff;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    @keyframes shimmer {
        to { background-position: 200% center; }
    }

    /* CSS สำหรับปุ่ม "แปลงเป็นเสียง" พร้อม Ripple และ Glow */
    .stButton>button {
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        font-weight: bold;
        padding: 12px 28px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        transform: scale(1.03) translateY(-2px);
        box-shadow: 0 8px 15px rgba(167, 119, 227, 0.5);
    }

    /* CSS สำหรับสร้างเอฟเฟกต์ Ripple */
    .stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.4);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }

    .stButton>button:active::after {
        animation: ripple 0.6s ease-out;
    }

    @keyframes ripple {
        0% { transform: scale(0, 0); opacity: 0.8; }
        20% { transform: scale(25, 25); opacity: 0.6; }
        100% { transform: scale(40, 40); opacity: 0; }
    }

    /* ปรับแต่งส่วนย่อยๆ */
    .stTextArea label, .stSlider label {
        font-weight: bold;
        color: #333;
    }
    
    .stSlider .st-at {
        background-color: #6e8efb;
    }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวที่มี Shimmer Text และแอนิเมชัน
st.markdown("<h1 class='shimmer-text'>Shan TTS Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>ၶိူင်ႈမိုဝ်းတႃႇဢဝ်တူဝ်လိၵ်ႈတႆးလၢႆႈပဵၼ်သဵင်ဢၢၼ်ႇ (v1)</p>", unsafe_allow_html=True)

st.write("---")

# กล่องรับข้อความขนาดใหญ่
text = st.text_area("📝 ပေႃႉလိၵ်ႈတႆးသႂ်ႇတီႈၼႆႈ:", height=150, placeholder="ပေႃႉလိၵ်ႈသႂ်ႇၼင်ႇၸဝ်ႈၵဝ်ႇၶႆႈသၢင်ႈသဵင်...")

# ตัวควบคุมความเร็ว (Slider)
speed = st.slider("⚡ တၢင်းဝႆးသဵင်", min_value=0.5, max_value=2.0, value=1.0, step=0.1, help="1.0 ပဵၼ်တၢင်းဝႆးပၢၼ်ၵၢင်")

# ปุ่มแปลงเสียงพร้อมเอฟเฟกต์
if st.button("✨ သၢင်ႈသဵင်"):
    if text.strip():
        # แอนิเมชันการโหลด
        with st.spinner('တိုၵ်ႉသၢင်ႈသဵင်ယူႇ...'):
            try:
                # ยังคงเรียกใช้ API เดิมโดยไม่เปลี่ยนแปลง
                client = Client("innkl24/shan-tts-api")
                result = client.predict(
                    text=text,
                    file_input=None, 
                    speed=speed,
                    api_name="/text_to_speech_api"
                )
                
                # แสดงข้อความสำเร็จแบบ Fade-in
                st.markdown("<div style='animation: fadeIn 1s; color:green; text-align:center;'>သၢင်ႈသဵင်ယဝ်ႉယဝ်ႉ!</div>", unsafe_allow_html=True)
                
                # แสดงเครื่องเล่นเสียง
                st.audio(result)
                
                # ปุ่มดาวน์โหลด
                with open(result, "rb") as file:
                    st.download_button(
                        label="⬇️ ၸၼ်ဢဝ်သဵင်လူင်းၼႂ်းၶိူင်ႈ(.wav)",
                        data=file,
                        file_name="shan_audio_generated.wav",
                        mime="audio/wav"
                    )
            except Exception as e:
                st.error(f"မီးလွင်ႈၽိတ်းပိူင်ႈလွင်ႈသိူမ်ႉတေႃႇ API: {e}")
    else:
        st.warning("ၶႅၼ်းတေႃႈပေႃႉလိၵ်ႈသႂ်ႇၵွၼ်ႇၶႃႈ")