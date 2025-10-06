from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ====== AFRICA'S TALKING CREDENTIALS ======
# ⚠️ In production, use Render ENV VARS:
#   AT_USERNAME = os.environ.get('AT_USERNAME')
#   AT_API_KEY = os.environ.get('AT_API_KEY')
AT_USERNAME = "ai_farm_brain"  # Replace with your AT username if not sandbox
AT_API_KEY = "UKSNb5Yb9"  # ← GET THIS FROM AT DASHBOARD
VOICE_NUMBER = "+254711082396"  # ← Replace with your AT voice number

# ====== USSD ENDPOINT ======
@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    text = request.values.get("text", "")
    phone = request.values.get("phoneNumber", "")
    
    if text == "":
        # First screen: language selection
        return "CON Siri ya Wakulima\n1. Swahili\n2. English"
    
    elif text == "1":
        # Trigger voice call for Swahili
        trigger_voice_call(phone, lang="sw")
        return "END Tunakupigia simu sasa. Tazama simu yako!"
    
    elif text == "2":
        # Trigger voice call for English
        trigger_voice_call(phone, lang="en")
        return "END We are calling you now. Please answer!"
    
    else:
        return "END Asante kwa kutumia Siri ya Wakulima!"

# ====== TRIGGER OUTBOUND CALL ======
def trigger_voice_call(phone, lang="sw"):
    """Call the farmer using Africa's Talking Voice API"""
    url = "https://voice.africastalking.com/call"
    payload = {
        "username": AT_USERNAME,
        "from": VOICE_NUMBER,
        "to": phone,
        "clientRequestId": f"farm_call_{phone}"
    }
    headers = {"apiKey": AT_API_KEY}
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"📞 Calling {phone} | AT Response: {response.text}")
    except Exception as e:
        print(f"❌ Call failed: {str(e)}")

# ====== HANDLE INCOMING CALL (VOICE XML) ======
@app.route('/voice_handler', methods=['POST'])
def voice_handler():
    """Play message + record when AT calls the farmer"""
    isActive = request.values.get('isActive') == '1'
    
    if isActive:
        # VoiceXML response: speak + record
        response = '''<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="man" language="en-KE">Sema tatizo lako la shamba kwa sauti. You have 8 seconds.</Say>
            <Record maxLength="8" finishOnKey="#" callbackUrl="https://siri-wakulima.onrender.com/recorded" />
        </Response>'''
        return response, 200, {'Content-Type': 'text/xml'}
    else:
        return "Call ended", 200

# ====== HANDLE RECORDED AUDIO ======
@app.route('/recorded', methods=['POST'])
def recorded():
    """Receive recording URL from AT and send to AI"""
    audio_url = request.values.get('recordingUrl')
    phone = request.values.get('phoneNumber')
    
    if not audio_url:
        return "No recording", 400
    
    print(f"🎧 Received recording from {phone}: {audio_url}")
    
    # Send to your Colab AI (replace with your ngrok URL)
    try:
        ai_response = requests.post(
            "https://YOUR_NGROK_HERE.ngrok.io/process",  # ← REPLACE THIS!
            json={"audio_url": audio_url, "phone": phone},
            timeout=30
        )
        result = ai_response.json()
        advice = result.get("advice", "Asante kwa subira.")
        lang = result.get("lang", "sw")
        print(f"✅ AI Advice: {advice}")
        
        # TODO: Call back with advice (Day 4)
        return "OK", 200
        
    except Exception as e:
        print(f"❌ AI Processing failed: {str(e)}")
        return "Error", 500

# ====== HEALTH CHECK ======
@app.route('/')
def home():
    return "Siri ya Wakulima Backend - OK"

# ====== RUN LOCALLY ONLY ======
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)