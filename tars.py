
    

import streamlit as st
from groq import Groq

# Sayfa Genişliği ve Tema
st.set_page_config(page_title="TARS İşletim Sistemi", layout="wide")

# API Anahtarın
client = Groq(api_key="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")

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ TARS Kontrol Paneli")
    st.info("Dürüstlük Parametresi: %90")
    st.info("Espri Anlayışı: %75")
    
    st.markdown("---")
    st.subheader("📁 Kategoriler")
    kategori = st.selectbox("Bir mod seçin:", ["Genel Sohbet", "Kod Yardımı", "Analiz", "Geyik Modu"])
    
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title(f"🤖 TARS - {kategori} Modu")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sohbet Girişi
if prompt := st.chat_input("TARS'a bir komut gönder..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Seçilen kategoriye göre TARS'ın kişiliğini ayarlıyoruz
        sistem_mesaji = f"Sen TARS'sın. Şu an {kategori} modundasın. Karakterine sadık kal."
        
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sistem_mesaji}, *st.session_state.messages],
            model="llama-3.3-70b-versatile",
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})