from flask import Flask, request

app = Flask(__name__)

@app.route('/ussd', methods=['GET', 'POST'])  # ← MUST include both!
def ussd():
    # Africa's Talking sends data as form-encoded POST
    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "")
    phone = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")  # This is the user's input

    if text == "":
        # First request: show menu
        response = "CON Siri ya Wakulima\n"
        response += "1. Swahili\n"
        response += "2. English"
        return response
    
    elif text == "1":
        return "CON Sema tatizo lako kwa sauti (8 sekunde):"
    
    elif text == "2":
        return "CON Describe your farm problem in voice (8 seconds):"
    
    else:
        return "END Asante! Tutakurudia kwa jibu."

# Health check
@app.route('/')
def home():
    return "OK"