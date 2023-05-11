import requests
from os import getenv

TOKEN = getenv('TELEGRAM_BOT_TOKEN')

def send_message(chat_id, text):
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    return requests.post(bot_url, json=data)

def send_chat_action(chat_id, action):
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
    data = {"chat_id": chat_id, "action": action}
    return requests.post(bot_url, json=data)

def set_webhook(server_url):
    bot_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": server_url}
    return requests.post(bot_url, json=data)
