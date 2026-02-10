import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import config

app = Flask(__name__)

# Single Groq client instance
groq_client = Groq(api_key=config.GROQ_API_KEY)


def route_command(body_raw: str):
    """
    Route incoming message using registries defined in config.py.
    - Lowercase is used ONLY for matching
    - Raw text is preserved for arguments
    """
    body = body_raw.lower().strip()

    # Prefix commands (e.g. "ssh host", "ping 1.2.3.4")
    for prefix, handler in config.PREFIX_COMMANDS.items():
        token = f"{prefix} "
        if body.startswith(token):
            arg = body_raw.strip()[len(token):].strip()
            return handler(arg)

    # Keyword commands (status / hints)
    for _, (handler, keywords) in config.KEYWORD_COMMANDS.items():
        if any(k in body for k in keywords):
            return handler()

    return None


def get_ai_fallback(body_raw: str):
    """
    Groq llama-3.3-70b-versatile fallback.
    Used only when no command matches.
    Command-suggesting, not chatty.
    """
    try:
        system_prompt = (
            "You are Minty, a netops WhatsApp assistant. "
            "Be concise. Prefer suggesting commands like: "
            "ssh <host>, ping <host>, tailping <node>, tail. "
            "Do not explain unless asked."
        )

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": body_raw}
            ],
            temperature=0.2,
            max_tokens=120,
        )

        reply = completion.choices[0].message.content.strip()
        return f"Minty: {reply}"

    except Exception as e:
        logging.error(f"Groq error: {e}")
        return "Minty: Brain fog… 🧠"


@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    body_raw = (request.values.get("Body") or "").strip()
    from_number = request.values.get("From", "").replace("whatsapp:", "")

    # Allowlist enforcement
    if config.ALLOWED_NUMBERS and from_number not in config.ALLOWED_NUMBERS:
        logging.warning(f"Blocked message from unauthorized number: {from_number}")
        twiml = MessagingResponse()
        twiml.message("⛔ Not authorised")
        return str(twiml)

    reply_text = route_command(body_raw) or get_ai_fallback(body_raw)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)


if __name__ == "__main__":
    # Bind for tunnel access (Tailscale / SSH port forward)
    app.run(host="0.0.0.0", port=5000)

import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import config

app = Flask(__name__)

# Single Groq client instance
groq_client = Groq(api_key=config.GROQ_API_KEY)


def route_command(body_raw: str):
    """
    Route incoming message using registries defined in config.py.
    - Lowercase is used ONLY for matching
    - Raw text is preserved for arguments
    """
    body = body_raw.lower().strip()

    # Prefix commands (e.g. "ssh host", "ping 1.2.3.4")
    for prefix, handler in config.PREFIX_COMMANDS.items():
        token = f"{prefix} "
        if body.startswith(token):
            arg = body_raw.strip()[len(token):].strip()
            return handler(arg)

    # Keyword commands (status / hints)
    for _, (handler, keywords) in config.KEYWORD_COMMANDS.items():
        if any(k in body for k in keywords):
            return handler()

    return None


def get_ai_fallback(body_raw: str):
    """
    Groq llama-3.3-70b-versatile fallback.
    Used only when no command matches.
    Command-suggesting, not chatty.
    """
    try:
        system_prompt = (
            "You are Minty, a netops WhatsApp assistant. "
            "Be concise. Prefer suggesting commands like: "
            "ssh <host>, ping <host>, tailping <node>, tail. "
            "Do not explain unless asked."
        )

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": body_raw}
            ],
            temperature=0.2,
            max_tokens=120,
        )

        reply = completion.choices[0].message.content.strip()
        return f"Minty: {reply}"

    except Exception as e:
        logging.error(f"Groq error: {e}")
        return "Minty: Brain fog… 🧠"


@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    body_raw = (request.values.get("Body") or "").strip()
    from_number = request.values.get("From", "").replace("whatsapp:", "")

    # Allowlist enforcement
    if config.ALLOWED_NUMBERS and from_number not in config.ALLOWED_NUMBERS:
        logging.warning(f"Blocked message from unauthorized number: {from_number}")
        twiml = MessagingResponse()
        twiml.message("⛔ Not authorised")
        return str(twiml)

    reply_text = route_command(body_raw) or get_ai_fallback(body_raw)

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)


if __name__ == "__main__":
    # Bind for tunnel access (Tailscale / SSH port forward)
    app.run(host="0.0.0.0", port=5000)

