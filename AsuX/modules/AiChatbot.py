"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""

import random
import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ContextTypes

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message

    # Check if message starts with command prefixes
    if any(message.text.startswith(prefix) for prefix in ["!", "/", "?", "@", "#"]):
        return

    chatbotdb = MongoClient(MONGO_DB_URL)
    chatbotai = chatbotdb["Word"]["WordDb"]

    K = []
    is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
    for x in is_chat:
        K.append(x["text"])

    if not message.reply_to_message:
        if K:
            hey = random.choice(K)
            is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
            Yo = is_text["check"]
        else:
            hey, Yo = await get_chatbot_response(message)

        if Yo == "sticker":
            await message.reply_sticker(hey)
        else:
            await message.reply_text(hey)

    else:  # If the message is a reply
        if message.reply_to_message.from_user.id == BOT_ID:
            if K:
                hey = random.choice(K)
                is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                Yo = is_text["check"]
            else:
                hey, Yo = await get_chatbot_response(message)

            if Yo == "sticker":
                await message.reply_sticker(hey)
            else:
                await message.reply_text(hey)

        else:
            await handle_sticker_or_text_response(message, chat, chatbotai)

async def get_chatbot_response(message):
    r = requests.get(
        f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
    )
    
    try:
        r.raise_for_status()  # Raise an error for bad responses
        hey = r.json().get("cnt", "No response")  # Use .get for safety
        return hey, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Error occurred while getting response.", None
    except ValueError:
        print("Response content is not valid JSON:", r.text)
        return "Invalid response from server.", None

async def handle_sticker_or_text_response(message, chat, chatbotai):
    if message.sticker:
        is_chat = chatbotai.find_one(
            {
                "chat": chat.id,
                "word": message.reply_to_message.text,
                "id": message.sticker.file_unique_id,
            }
        )
        if not is_chat:
            chatbotai.insert_one(
                {
                    "chat": chat.id,
                    "word": message.reply_to_message.text,
                    "text": message.sticker.file_id,
                    "check": "sticker",
                    "id": message.sticker.file_unique_id,
                }
            )

    if message.text:
        is_chat = chatbotai.find_one(
            {
                "chat": chat.id,
                "word": message.reply_to_message.text,
                "text": message.text,
            }
        )
        if not is_chat:
            chatbotai.insert_one(
                {
                    "chat": chat.id,
                    "word": message.reply_to_message.text,
                    "text": message.text,
                    "check": "none",
                }
        )
            


USER_HANDLER = MessageHandler(filters.ALL, log_user, block=False)
rani.add_handler(USER_HANDLER, USERS_GROUP)
