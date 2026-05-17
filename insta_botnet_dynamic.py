from flask import Flask, request, jsonify, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

# --- నీ టెలిగ్రామ్ డీటెయిల్స్ ---
TELEGRAM_BOT_TOKEN = "8167370627:AAGH7p_JywwgVEs4mpLwC9N9QFh9DL-76dI"
TELEGRAM_CHAT_IDS = ["6722230049", "6513585290"]

# --- పూర్తి ఫీచర్స్ ఉన్న UI (HTML & JS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GramRakshak Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Animations */
        @keyframes pulse-ring {
            0% { transform: scale(0.8); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(220, 38, 38, 0); }
            100% { transform: scale(0.8); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
        }
        .sos-pulse { animation: pulse-ring 2s infinite; }
        .tap-effect { transition: transform 0.1s; }
        .tap-effect:active { transform: scale(0.92); }
        .glass-panel { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
</head>
<body class="bg-gray-950 text-white font-sans min-h-screen">

    <!-- 1. PERMISSION OVERLAY (ముందు పర్మిషన్లు ఇస్తేనే యాప్ ఓపెన్ అవుతుంది) -->
    <div id="permission-screen" class="fixed inset-0 bg-gray-900 z-[100] flex flex-col items-center justify-center p-6 text-center">
        <div class="w-24 h-24 bg-red-600 rounded-full flex items-center justify-center mb-6 sos-pulse">
            <i class="fas fa-shield-halved text-4xl text-white"></i>
        </div>
        <h2 class="text-2xl font-black mb-2 text-white">GramRakshak <span class="text-red-500">PRO</span></h2>
        <p class="text-gray-400 text-sm mb-8 px-4">ఈ యాప్ మీ గ్రామ భద్రత కోసం పనిచేస్తుంది. దయచేసి Camera మరియు Location పర్మిషన్లు ఇవ్వండి.</p>
        <button onclick="requestPermissions()" class="bg-red-600 hover:bg-red-700 text-white w-full py-4 rounded-2xl font-bold text-lg shadow-lg shadow-red-900/50 tap-effect">
            <i class="fas fa-check-circle mr-2"></i> ALLOW PERMISSIONS
        </button>
    </div>

    <!-- MAIN APP SCREEN -->
    <div id="main-app" class="hidden">
        <!-- Header -->
        <header class="p-5 flex justify-between items-center glass-panel sticky top-0 z-50">
            <div>
                <h1 class="text-xl font-black italic tracking-wider text-red-500">GRAMRAKSHAK</h1>
                <p class="text-[10px] text-gray-400 uppercase tracking-widest">Village Security System</p>
            </div>
            <button onclick="alert('Admin Panel Secured.')" class="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center text-gray-300 tap-effect border border-gray-700">
                <i class="fas fa-user-lock"></i>
            </button>
        </header>

        <!-- Emergency SOS Grid -->
        <div class="p-5 mt-2">
            <h2 class="text-xs font-bold text-gray-500 mb-4 tracking-widest uppercase text-center flex items-center justify-center gap-2">
                <i class="fas fa-exclamation-triangle text-red-500"></i> Tap to Alert Authorities
            </h2>
            <div class="grid grid-cols-2 gap-4">
                <button onclick="sendAlert('POLICE')" class="tap-effect h-36 bg-gradient-to-br from-blue-600 to-blue-900 rounded-3xl flex flex-col items-center justify-center shadow-lg shadow-blue-900/50 border border-blue-500/50 relative overflow-hidden">
                    <i class="fas fa-building-shield text-4xl mb-2 text-white"></i>
                    <span class="font-bold tracking-widest text-sm text-white">POLICE</span>
                </button>
                
                <button onclick="sendAlert('MEDICAL')" class="tap-effect h-36 bg-gradient-to-br from-green-500 to-green-800 rounded-3xl flex flex-col items-center justify-center shadow-lg shadow-green-900/50 border border-green-500/50">
                    <i class="fas fa-truck-medical text-4xl mb-2 text-white"></i>
                    <span class="font-bold tracking-widest text-sm text-white">MEDICAL</span>
                </button>

                <button onclick="sendAlert('FIRE DEPT')" class="tap-effect h-36 bg-gradient-to-br from-orange-500 to-orange-800 rounded-3xl flex flex-col items-center justify-center shadow-lg shadow-orange-900/50 border border-orange-500/50">
                    <i class="fas fa-fire-extinguisher text-4xl mb-2 text-white"></i>
                    <span class="font-bold tracking-widest text-sm text-white">FIRE</span>
                </button>

                <button onclick="sendAlert('WOMEN SAFETY')" class="tap-effect h-36 bg-gradient-to-br from-pink-500 to-pink-800 rounded-3xl flex flex-col items-center justify-center shadow-lg shadow-pink-900/50 border border-pink-500/50">
                    <i class="fas fa-person-breastfeeding text-4xl mb-2 text-white"></i>
                    <span class="font-bold tracking-widest text-sm text-white">SAFETY</span>
                </button>
            </div>
        </div>

        <!-- AI Assistant & Services -->
        <div class="p-5">
            <div class="glass-panel rounded-3xl p-5 border border-gray-800">
                <h3 class="text-xs font-bold text-red-500 tracking-widest mb-3 uppercase"><i class="fas fa-robot mr-1"></i> Gram AI Chat</h3>
                <div id="ai-chat" class="h-20 overflow-y-auto text-xs text-gray-400 mb-3 space-y-1">
                    <div><span class="text-green-400 font-bold">AI:</span> Hello! How can I secure the village today?</div>
                </div>
                <div class="flex gap-2">
                    <input id="ai-msg" type="text" class="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-red-500" placeholder="Type message...">
                    <button onclick="chatAI()" class="bg-red-600 px-4 rounded-xl text-white tap-effect"><i class="fas fa-paper-plane"></i></button>
                </div>
            </div>
        </div>
    </div>

    <!-- Loading Screen (అలర్ట్ వెళ్లేటప్పుడు) -->
    <div id="loader" class="hidden fixed inset-0 bg-gray-950/90 z-[200] flex flex-col items-center justify-center">
        <div class="w-16 h-16 border-4 border-gray-700 border-t-red-600 rounded-full animate-spin mb-4"></div>
        <p class="font-bold tracking-widest text-red-500 animate-pulse">SENDING ALERT...</p>
    </div>

    <script>
        // 1. Get Camera and Location Permissions Together
        async function requestPermissions() {
            try {
                // Request Camera First
                await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                
                // Then Request Location
                navigator.geolocation.getCurrentPosition((pos) => {
                    // Both successful! Hide overlay, show app.
                    document.getElementById('permission-screen').classList.add('hidden');
                    document.getElementById('main-app').classList.remove('hidden');
                }, (err) => {
                    alert("Location Permission is required for emergency SOS!");
                });
            } catch (err) {
                alert("Camera Permission is required!");
            }
        }

        // 2. Reliable SOS Alert Function
        function sendAlert(type) {
            if(!confirm(type + " కి అలర్ట్ పంపించాలా?")) return;
            
            document.getElementById('loader').classList.remove('hidden');

            // High Accuracy Location
            navigator.geolocation.getCurrentPosition(async (pos) => {
                const payload = {
                    type: type,
                    lat: pos.coords.latitude,
                    lng: pos.coords.longitude
                };

                try {
                    const response = await fetch('/api/sos', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });

                    if(response.ok) {
                        alert("✅ " + type + " Alert Sent Successfully!");
                    } else {
                        alert("❌ Server Error. Please try again.");
                    }
                } catch(e) {
                    alert("❌ Network Error. Make sure you have internet.");
                } finally {
                    document.getElementById('loader').classList.add('hidden');
                }

            }, (err) => {
                alert("Location Error! దయచేసి మొబైల్ GPS/Location ఆన్ చేయండి.");
                document.getElementById('loader').classList.add('hidden');
            }, { enableHighAccuracy: true, timeout: 10000 });
        }

        // 3. AI Chatbot
        function chatAI() {
            const input = document.getElementById('ai-msg');
            const chat = document.getElementById('ai-chat');
            if(!input.value) return;
            
            chat.innerHTML += `<div><span class="text-gray-300 font-bold">You:</span> ${input.value}</div>`;
            chat.innerHTML += `<div><span class="text-red-400 font-bold">AI:</span> Request noted. Monitoring situation...</div>`;
            chat.scrollTop = chat.scrollHeight;
            input.value = "";
        }
    </script>
</body>
</html>
"""

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template_string(HTML_UI)

@app.route('/api/sos', methods=['POST'])
def handle_sos():
    data = request.json
    sos_type = data.get('type', 'UNKNOWN')
    lat = data.get('lat')
    lng = data.get('lng')
    
    map_url = f"https://www.google.com/maps?q={lat},{lng}"
    time_now = datetime.now().strftime('%d-%m-%Y %I:%M %p')

    message = f"🚨 <b>GRAMRAKSHAK EMERGENCY</b> 🚨\n\n" \
              f"🆘 <b>Service Needed:</b> {sos_type}\n" \
              f"📍 <b>Live Location:</b> <a href='{map_url}'>Click here for Map</a>\n" \
              f"⏰ <b>Time:</b> {time_now}\n" \
              f"👤 <b>Sender:</b> GramRakshak App User"

    # టెలిగ్రామ్ కి కచ్చితంగా వెళ్లేలా Loop
    success_count = 0
    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            res = requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=10)
            if res.status_code == 200:
                success_count += 1
        except Exception as e:
            print(f"Failed to send to {chat_id}: {e}")
            pass

    if success_count > 0:
        return jsonify({"status": "success", "message": "Alert sent"}), 200
    else:
        return jsonify({"status": "error", "message": "Telegram failed"}), 500
