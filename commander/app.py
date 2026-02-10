# FILE: /home/martin/ansible/commander/app.py
import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import ollama
import config # Registry now comes from here

app = Flask(__name__)

def route_command(body):
    """Route incoming message using registries defined in config.py"""
    
    # Check prefix commands (addtv, addmovies)
    for prefix, handler in config.PREFIX_COMMANDS.items():
        if body.startswith(f"{prefix} "):
            argument = body.replace(f"{prefix} ", "", 1).strip()
            return handler(argument)
    
    # Check keyword commands (weather, disk, fleet)
    for cmd_name, (handler, keywords) in config.KEYWORD_COMMANDS.items():
        if any(keyword in body for keyword in keywords):
            if cmd_name == 'seed':
                return handler(body)
            return handler()
    
    return None

def get_ai_fallback(body):
    """AI Response Logic"""
    try:
        prompt = "You are Minty, a chill home-lab commander. Start with 'Minty: '."
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{'role': 'system', 'content': prompt}, {'role': 'user', 'content': body}]
        )
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ollama error: {e}")
        return "Minty: Brain fog... 🧠"

@app.route("/webhook", methods=['POST'])
def whatsapp_bot():
    body = (request.values.get('Body') or '').strip().lower()
    reply_text = route_command(body) or get_ai_fallback(body)
    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)

if __name__ == "__main__":
    # Binding to 0.0.0.0:5000 for tunnel access
    app.run(host='0.0.0.0', port=5000)

########## EXPLANATION ##########
# 1. config.py now acts as the 'Control Plane'. If you want to 
#    add a new command (e.g., 'reboot'), you add it to the 
#    dictionary in config.py without ever touching app.py.
# 2. app.py remains purely the 'Data Plane'. It handles the 
#    HTTP lifecycle, Twilio XML, and AI fallback.
# 3. This structure prevents 'ImportErrors' because config.py 
#    is already being imported by app.py, keeping the 
#    dependency tree flat.
