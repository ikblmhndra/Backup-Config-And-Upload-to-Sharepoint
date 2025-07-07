import requests
import os
from dotenv import load_dotenv

load_dotenv()


def simpleChat(chat_id, text, channel_id):
    tele_token = os.getenv('TELEBOT_TOKEN')

    tele_url = "https://api.telegram.org/bot"+tele_token+"/sendMessage"
    headers = {
        "Content-type" : "application/json"
    }
    payload ={
        "chat_id" : chat_id,
        "text" : text,
        "message_thread_id" : channel_id,
        "parse_mode" : "Markdown",
    }

    req = requests.request("POST", tele_url, headers=headers, json=payload)
    print(req.status_code)
    return 