from flask import Flask, request, jsonify
from bot2 import handle_telegram_message  # import z Twojego pliku

app = Flask(__name__)

@app.route('/handle-message', methods=['POST'])
def handle_message():
    try:
        data = request.json
        message_text = data.get('message', '')
        response_text = handle_telegram_message(message_text)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)