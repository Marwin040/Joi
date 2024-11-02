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
        if not message.reply_to_message:
            K = []
            is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
            for x in is_chat:
                K.append(x["text"])

            if K:
                hey = random.choice(K)
                is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                Yo = is_text["check"]
            else:
                try:
                    r = requests.get(
                        f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}",
                        timeout=5  # Set a timeout for the request
                    )
                    r.raise_for_status()  # Raise an error for bad responses
                    
                    response_json = r.json()
                    hey = response_json.get("cnt", "I didn't get a response.")
                except Timeout:
                    hey = "Request timed out. Please try again."
                except RequestException as e:
                    hey = f"Request error: {e}. Response content: {r.text if r else 'No response'}"
                except ValueError as ve:
                    hey = f"Failed to decode JSON response: {ve}. Response content: {r.text}"

                Yo = None

            if Yo == "sticker":
                await message.reply_sticker(hey)
            else:
                await message.reply_text(hey)

        else:  # Handling replies to messages
            if message.reply_to_message.from_user.id == BOT_ID:
                K = []
                is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
                for x in is_chat:
                    K.append(x["text"])

                if K:
                    hey = random.choice(K)
                    is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                    Yo = is_text["check"]
                else:
                    try:
                        r = requests.get(
                            f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}",
                            timeout=5  # Set a timeout for the request
                        )
                        r.raise_for_status()

                        response_json = r.json()
                        hey = response_json.get("cnt", "I didn't get a response.")
                    except Timeout:
                        hey = "Request timed out. Please try again."
                    except RequestException as e:
                        hey = f"Request error: {e}. Response content: {r.text if r else 'No response'}"
                    except ValueError as ve:
                        hey = f"Failed to decode JSON response: {ve}. Response content: {r.text}"

                    Yo = None

                if Yo == "sticker":
                    await message.reply_sticker(hey)
                else:
                    await message.reply_text(hey)

            elif message.reply_to_message.from_user.id != BOT_ID:
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

    except Exception as e:
        print(f"Error in log_user: {e}")

USER_HANDLER = MessageHandler(filters.ALL, log_user, block=False)
rani.add_handler(USER_HANDLER, USERS_GROUP)
