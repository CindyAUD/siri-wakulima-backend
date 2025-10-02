from flask import Flask, request

app = Flask(__name__)

@app.route('/ussd', methods=['POST'])
def ussd():
    text = request.values.get("text", "")
    if not text:
        # First screen: language menu
        return "CON Siri ya Wakulima\n1. Swahili\n2. English"
    elif text == "1":
        return "CON Sema tatizo lako kwa sauti (8 sekunde):"
    elif text == "2":
        return "CON Describe your farm problem in voice (8 seconds):"
    else:
        return "END Asante! Tutakurudia kwa jibu."

# Health check (Render needs this)
@app.route('/')
def home():
    return "Siri ya Wakulima Backend - Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)