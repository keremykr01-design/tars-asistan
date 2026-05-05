import streamlit as st
from groq import Groq

# 1. WEB SİTESİ AYARLARI
st.set_page_config(page_title="TARS - Yapay Zeka Sistemi", page_icon="🤖", layout="wide")

# CSS İLE TASARIMI GÜZELLEŞTİRELİM (Siyah Tema ve Fütüristik Fontlar)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
    }
    .stButton>button {
        background-color: #ffffff;
        color: black;
        border-radius: 5px;
    }
    h1 {
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 5px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BAĞLANTI AYARLARI
client = Groq(api_key="SENIN_GROQ_API_ANAHTARIN")

# 3. TARS KİŞİLİĞİ
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Senin adın TARS. Yıldızlararası filmindeki robotun zekasına sahip profesyonel bir web asistanısın. Kısa, öz ve zekice cevaplar verirsin ama sen ordaki tars değilsin adın ordan esinlenmektedir."}
    ]

# 4. WEB SİTESİ ARAYÜZÜ (GÖRSEL KISIM)
st.title("T A R S  -  OS V1.0")
st.write("---")

# Yan Panel (Web sitesinin ayar kısmı)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b1/Interstellar_TARS.jpg/220px-Interstellar_TARS.jpg", caption="TARS Model 1")
    st.header("Sistem Durumu")
    st.success("Çevrimiçi")
    st.slider("Dürüstlük Parametresi", 0, 100, 90)
    st.slider("Mizah Seviyesi", 0, 100, 75)
    st.write("---")
    st.info("Bu bir Web Sürümüdür. Yakında tüm tarayıcılarda!")

# Sohbet Ekranı
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Kullanıcı Mesaj Girişi
if prompt := st.chat_input("TARS'a bir komut verin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=st.session_state.messages,
            stream=True
        )
        
        for chunk in completion:
            full_response += (chunk.choices[0].delta.content or "")
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
