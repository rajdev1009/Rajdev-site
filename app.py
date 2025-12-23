<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raj News - Dev AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --bg: #050505; --primary: #00ff00; }
        body { font-family: 'Poppins', sans-serif; background: var(--bg); color: white; margin: 0; padding: 0; }
        
        @keyframes rgb-glow {
            0% { box-shadow: 0 0 15px #ff0000; border-color: #ff0000; }
            33% { box-shadow: 0 0 15px #00ff00; border-color: #00ff00; }
            66% { box-shadow: 0 0 15px #0000ff; border-color: #0000ff; }
            100% { box-shadow: 0 0 15px #ff0000; border-color: #ff0000; }
        }

        /* Smooth Talking Animation (No Layout Shake) */
        @keyframes talk-pulse {
            0% { transform: scale(1); filter: brightness(1); }
            50% { transform: scale(1.05); filter: brightness(1.3); }
            100% { transform: scale(1); filter: brightness(1); }
        }
        .talking-active { animation: talk-pulse 0.4s infinite ease-in-out; }

        .social-header { display: flex; justify-content: center; gap: 20px; padding: 20px; background: #111; border-bottom: 1px solid #333; }
        .social-header a { color: white; font-size: 24px; text-decoration: none; transition: 0.3s; }

        .gallery { max-width: 600px; margin: auto; padding: 20px; padding-bottom: 120px; }
        .card { background: #111; border-radius: 15px; overflow: hidden; margin-bottom: 25px; border: 1px solid #333; }
        .card img { width: 100%; display: block; }
        .card-text { padding: 15px; font-size: 14px; color: #ccc; }
        
        .ad-unit { border: 2px solid red; border-radius: 12px; padding: 15px; text-align: center; animation: rgb-glow 3s infinite linear; margin-bottom: 25px; }
        .ad-btn { background: linear-gradient(90deg, #ff0000, #ff00ff); color: white; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; }

        #chat-bubble { position: fixed; bottom: 25px; right: 25px; background: #000; border: 2px solid #fff; padding: 12px 20px; border-radius: 50px; cursor: pointer; animation: rgb-glow 4s infinite linear; z-index: 1001; display: flex; align-items: center; gap: 10px; }

        .chat-card { position: fixed; bottom: 90px; right: 25px; width: 320px; height: 480px; background: #000; border-radius: 20px; display: none; flex-direction: column; border: 2px solid #333; z-index: 1000; overflow: hidden; }
        #avatar-header { background: #111; padding: 15px; text-align: center; border-bottom: 1px solid #333; }
        
        /* Fixed Container for Avatar to prevent shaking */
        .img-container { width: 100px; height: 100px; margin: auto; position: relative; }
        #dev-img { width: 100%; height: 100%; border-radius: 50%; border: 3px solid var(--primary); object-fit: cover; }

        #chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: #050505; }
        .msg { padding: 10px 14px; border-radius: 15px; font-size: 13px; max-width: 80%; }
        .bot { background: #222; align-self: flex-start; }
        .user { background: #007bff; align-self: flex-end; }

        .input-area { padding: 12px; background: #111; display: flex; gap: 8px; }
        input { flex: 1; background: #000; border: 1px solid #444; color: #fff; padding: 10px; border-radius: 10px; outline: none; }
        .send-btn { background: var(--primary); color: #000; border: none; padding: 0 15px; border-radius: 10px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

    <div class="social-header">
        <a href="{{ config_links.FACEBOOK_LINK }}" target="_blank"><i class="fab fa-facebook"></i></a>
        <a href="{{ config_links.INSTAGRAM_LINK }}" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="{{ config_links.TELEGRAM_LINK }}" target="_blank"><i class="fab fa-telegram"></i></a>
        <a href="{{ config_links.WHATSAPP_LINK }}" target="_blank"><i class="fab fa-whatsapp"></i></a>
    </div>

    <div class="gallery">
        <h2 style="text-align: center; color: var(--primary);">RAJ DIGITAL NEWS</h2>
        {% for photo in photos %}
        <div class="card"><img src="{{ photo.url }}"><div class="card-text">{{ photo.text }}</div></div>
        <div class="ad-unit"><a href="{{ smart_link }}" target="_blank" class="ad-btn">CLICK TO VIEW</a></div>
        {% endfor %}
    </div>

    <div id="chat-bubble" onclick="toggleChat()">
        <i class="fas fa-robot"></i> <strong>Talk to Dev</strong>
    </div>

    <div class="chat-card" id="chat-window">
        <div id="avatar-header">
            <div class="img-container">
                <img id="dev-img" src="{{ avatar_n }}" alt="Dev">
            </div>
            <div style="font-size: 11px; color: var(--primary); margin-top: 5px;">● DEV MALE LIVE</div>
        </div>
        <div id="chat-box">
            <div class="msg bot">Namaste! Main Dev hoon.</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Poochiye..." onkeypress="if(event.key==='Enter') send()">
            <button class="send-btn" onclick="send()">SEND</button>
        </div>
    </div>

    <script>
        function toggleChat() {
            const win = document.getElementById('chat-window');
            win.style.display = (win.style.display === 'flex') ? 'none' : 'flex';
        }

        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            const voices = synth.getVoices();
            const img = document.getElementById('dev-img');

            let maleVoice = voices.find(v => v.lang.includes('hi') && (v.name.includes('Male') || v.name.includes('Hemant')));
            if(maleVoice) utter.voice = maleVoice;

            utter.pitch = 0.5;
            utter.rate = 0.85;

            // Start Animation
            utter.onstart = () => { img.classList.add('talking-active'); };
            // Stop Animation
            utter.onend = () => { img.classList.remove('talking-active'); };

            synth.speak(utter);
        }

        async function send() {
            const input = document.getElementById('user-input');
            const box = document.getElementById('chat-box');
            if(!input.value.trim()) return;
            
            const msg = input.value;
            box.innerHTML += `<div class="msg user">${msg}</div>`;
            input.value = '';
            box.scrollTop = box.scrollHeight;

            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            const data = await res.json();
            box.innerHTML += `<div class="msg bot">${data.reply}</div>`;
            box.scrollTop = box.scrollHeight;
            speak(data.reply);
        }
        window.speechSynthesis.onvoiceschanged = () => { window.speechSynthesis.getVoices(); };
    </script>
</body>
</html>
