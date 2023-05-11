import requests
from os import getenv

TOKEN = getenv('TELEGRAM_BOT_TOKEN')

def send_message(chat_id, text):
    """
    Function that sends post request to the telegram API method "sendMessage".
    After that sending message to the user from our bot.
    """
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    return requests.post(bot_url, json=data)

def send_chat_action(chat_id, action):
    """
    Function that sends post request to the telegram API method "sendChatAction".
    After that showing chat action to the user from our bot.
    """
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
    data = {"chat_id": chat_id, "action": action}
    return requests.post(bot_url, json=data)

def set_webhook(server_url):
    """
    Function that is setting a webhook between
    telegram bot API and python web server.
    """
    bot_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": server_url}
    return requests.post(bot_url, json=data)
