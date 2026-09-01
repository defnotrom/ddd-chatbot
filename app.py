from flask import Flask, render_template_string, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Template Tampilan Web Chatbot
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Chatbot</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { background: #121212; color: #fff; margin: 0; padding: 15px; display: flex; justify-content: center; }
        .chat-container { width: 100%; max-width: 450px; background: #1e1e1e; height: 90vh; border-radius: 12px; display: flex; flex-direction: column; box-shadow: 0 4px 15px rgba(0,0,0,0.5); overflow: hidden; }
        .chat-header { background: #3700b3; padding: 15px; font-weight: bold; text-align: center; }
        #chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 80%; padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.4; }
        .user { align-self: flex-end; background: #03dac6; color: #000; border-bottom-right-radius: 0; }
        .bot { align-self: flex-start; background: #2c2c2c; color: #fff; border-bottom-left-radius: 0; }
        .input-box { display: flex; padding: 10px; background: #2c2c2c; gap: 8px; }
        input { flex: 1; padding: 12px; border: none; border-radius: 20px; outline: none; background: #3a3a3a; color: #fff; }
        button { background: #bb86fc; color: #000; border: none; padding: 0 18px; border-radius: 20px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
<div class="chat-container">
    <div class="chat-header">🐍 Python Bot Interaktif</div>
    <div id="chat-box">
        <div class="msg bot"><b>Bot:</b> Halo! Saya chatbot yang berjalan di server Python. Mau ngobrol apa hari ini?</div>
    </div>
    <div class="input-box">
        <input type="text" id="userInput" placeholder="Ketik pesan..." onkeypress="if(event.key==='Enter') kirimPesan()">
        <button onclick="kirimPesan()">Kirim</button>
    </div>
</div>

<script>
    async function kirimPesan() {
        let inputEl = document.getElementById("userInput");
        let text = inputEl.value.trim();
        if (text === "") return;

        let chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += `<div class="msg user">${text}</div>`;
        inputEl.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        // Kirim pesan ke backend Python
        let response = await fetch('/get_response', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        let data = await response.json();

        chatBox.innerHTML += `<div class="msg bot"><b>Bot:</b> ${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>
</body>
</html>
"""

# Logika Pemrosesan Pesan dalam Python
def logika_bot(pesan):
    p = pesan.lower()
    
    # Respons Waktu
    if any(k in p for k in ["halo", "hai", "salam", "pagi", "siang", "malam"]):
        jam = datetime.now().hour
        waktu = "pagi" if 4 <= jam < 11 else "siang" if 11 <= jam < 15 else "sore" if 15 <= jam < 18 else "malam"
        return f"Halo! Selamat {waktu}. Ada yang bisa dibantu?"

    # Kabar dan Perasaan
    elif "kabar" in p:
        return "Server Python saya berjalan lancar! Kamu gimana kabarnya?"
    elif any(k in p for k in ["sedih", "capek", "pusing"]):
        return "Istirahat sejenak dulu ya. Jangan terlalu memaksakan diri."

    # Lelucon
    elif any(k in p for k in ["lucu", "lelucon", "jokes"]):
        jokes = [
            "Kenapa bahasa Python populer? Karena nggak suka digigit!",
            "Kucing apa yang kuno? Kucing-galan zaman!",
            "Kenapa komputer suka dingin? Karena banyak kipasnya!"
        ]
        return random.choice(jokes)

    # Identitas
    elif "siapa kamu" in p or "namamu" in p:
        return "Saya adalah chatbot berbasis Python Flask yang siap nemenin kamu ngobrol!"

    # Default
    else:
        balasan_default = [
            "Menarik sekali! Cerita lebih banyak tentang itu dong.",
            "Wah, saya perlu memperluas pustaka kata saya untuk memahami itu!",
            "Coba tanya hal lain atau minta lelucon!"
        ]
        return random.choice(balasan_default)

# Route Halaman Utama
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Route API untuk menerima pesan
@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_reply = logika_bot(user_message)
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
