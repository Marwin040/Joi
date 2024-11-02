"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""
import random
import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from requests.exceptions import Timeout, RequestException

from AsuX import *

USERS_GROUP = 11

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message

    # Ignore commands or special messages
    if message.text.startswith(("!", "/", "?", "@", "#")):
        return

    chatbotdb = MongoClient(MONGO_DB_URL)
    chatbotai = chatbotdb["Word"]["WordDb"]

    try:
        # Handling messages that are not replies
        if not message.reply_to_message:
            K = []
            is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
            K = [x["text"] for x in is_chat]

            if K:
                hey = random.choice(K)
                is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                Yo = is_text["check"] if is_text else None
            else:
                hey, Yo = await fetch_response(message)

            if Yo == "sticker":
                await message.reply_sticker(hey)
            else:
                await message.reply_text(hey)

        # Handling replies to the bot
        else:
            if message.reply_to_message.from_user.id == BOT_ID:
                K = []
                is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
                K = [x["text"] for x in is_chat]

                if K:
                    hey = random.choice(K)
                    is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                    Yo = is_text["check"] if is_text else None
                else:
                    hey, Yo = await fetch_response(message)

                if Yo == "sticker":
                    await message.reply_sticker(hey)
                else:
                    await message.reply_text(hey)

            elif message.reply_to_message.from_user.id != BOT_ID:
                await handle_reply_sticker(chat, message)
                await handle_reply_text(chat, message)

    except Exception as e:
        print(f"Error in log_user: {e}")

async def fetch_response(message):
    try:
        r = requests.get(
            f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}",
            timeout=5
        )
        r.raise_for_status()
        response_json = r.json()
        hey = response_json.get("cnt", "I didn't get a response.")
        return hey, None
    except Timeout:
        return "Request timed out. Please try again.", None
    except RequestException as e:
        return f"Request error: {e}.", None
    except ValueError as ve:
        return f"Failed to decode JSON response: {ve}.", None

async def handle_reply_sticker(chat, message):
    if message.sticker:
        is_chat = chatbotai.find_one({
            "chat": chat.id,
            "word": message.reply_to_message.text,
            "id": message.sticker.file_unique_id,
        })
        if not is_chat:
            chatbotai.insert_one({
                "chat": chat.id,
                "word": message.reply_to_message.text,
                "text": message.sticker.file_id,
                "check": "sticker",
                "id": message.sticker.file_unique_id,
            })

async def handle_reply_text(chat, message):
    if message.text:
        is_chat = chatbotai.find_one({
            "chat": chat.id,
            "word": message.reply_to_message.text,
            "text": message.text,
        })
        if not is_chat:
            chatbotai.insert_one({
                "chat": chat.id,
                "word": message.reply_to_message.text,
                "text": message.text,
                "check": "none",
            })

USER_HANDLER = MessageHandler(filters.ALL, log_user, block=False)
rani.add_handler(USER_HANDLER, USERS_GROUP)
