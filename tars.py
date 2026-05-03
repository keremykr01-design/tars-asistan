import streamlit as st
from groq import Groq
import base64

# Sayfa Ayarları
st.set_page_config(page_title="TARS AI", page_icon="🤖")
st.title("🤖 TARS İşletim Sistemi")

# API Anahtarı (Burayı kendi anahtarınla doldur)
client = Groq(api_key="SENIN_GROQ_API_ANAHTARIN")

# TARS'ın Yeni Kişiliği
system_prompt = {
    "role": "system", 
    "content": "Senin adın TARS. Yıldızlararası filmindeki TARS'ın zekasına ve ismine sahipsin ama bir film karakteri gibi davranmıyorsun. Profesyonel, mantıklı ve çok zeki bir asistansın. Esprilerin dozunda ve zekice. Sesin filmdeki gibi robotik ve karakteristik."
}

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# --- SES FONKSİYONU ---
def speak(text):
    # Bu aşamada Google'ın ses altyapısını kullanıp üzerine robotik efekt ekleyeceğiz
    # Şimdilik tarayıcının ses motorunu kullanarak TARS sesini simüle ediyoruz
    js_code = f"""
        var msg = new SpeechSynthesisUtterance('{text}');
        var voices = window.speechSynthesis.getVoices();
        msg.pitch = 0.5; // Sesi kalınlaştırır (TARS gibi)
        msg.rate = 0.9;  // Biraz daha yavaş ve robotik konuşma
        window.speechSynthesis.speak(msg);
    """
    st.components.v1.html(f"<script>{js_code}</script>", height=0)

# Sohbeti Görüntüle
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Mesaj Gönderme
if prompt := st.chat_input("TARS'a emret..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        
        # CEVABI SESLİ OKU
        speak(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Yan Menü
with st.sidebar:
    st.header("TARS Kontrol Paneli")
    st.write("Dürüstlük Parametresi: %90")
    st.write("Mizah Seviyesi: %75")
    if st.button("🖼️ Görüntü Modülünü Hazırla"):
        st.info("Görüntü oluşturma motoru (DALL-E veya benzeri) bir sonraki güncellemede bağlanacak.")
