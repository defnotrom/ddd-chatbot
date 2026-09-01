import streamlit as st
import random
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Nova Bot", page_icon="🤖")
st.title("🤖 Nova Chatbot")
st.caption("Chatbot interaktif sederhana berbasis Streamlit")

# Inisialisasi Riwayat Obrolan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Aku Nova. Ada yang mau kamu ceritakan hari ini?"}
    ]

# Tampilkan Seluruh Riwayat Obrolan
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Fungsi Logika Pemrosesan Pesan
def respons_bot(pesan_user):
    text = pesan_user.lower().strip()
    
    if any(w in text for w in ["halo", "hai", "salam", "pagi", "siang", "malam"]):
        hr = datetime.now().hour
        salam = "pagi" if 4 <= hr < 11 else "siang" if 11 <= hr < 15 else "sore" if 15 <= hr < 18 else "malam"
        return f"Selamat {salam}! Gimana harimu sejauh ini?"
    elif "humor" in text or "lucu" in text or "joke" in text:
        jokes = [
            "Kenapa es batu rasanya dingin? Soalnya kalau hangat namanya teh manis!",
            "Kucing apa yang kuno? Kucing-galan zaman!",
            "Kenapa HP kalau jatuh ke air rusak? Soalnya belum belajar berenang!"
        ]
        return random.choice(jokes)
    elif "siapa kamu" in text or "namamu" in text:
        return "Aku Nova, chatbot yang dibuat menggunakan Streamlit dan Python!"
    elif any(w in text for w in ["capek", "sedih", "pusing"]):
        return "Istirahat dulu sejenak ya. Jangan lupa minum air putih!"
    else:
        defaults = [
            "Menarik sekali! Cerita lebih banyak dong.",
            "Wah, aku baru tahu soal itu!",
            "Coba minta 'lelucon' biar nggak bosan!"
        ]
        return random.choice(defaults)

# Area Input Pesan dari Pengguna
if prompt := st.chat_input("Ketik pesan di sini..."):
    # Simpan & tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Proses & tampilkan balasan bot
    balasan = respons_bot(prompt)
    st.session_state.messages.append({"role": "assistant", "content": balasan})
    st.chat_message("assistant").write(balasan)
