"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""

import random
import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
import logging

# Configuration
MONGO_DB_URL = "mongodb+srv://marwin0985:BEwJvxaADStDLScc@cluster0.oh0nk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TOKEN = "7343734756:AAFQJ1lYOgmroGBazwWfP-HC9jAMFSTGv08"
AI_API_KEY = "RBPOWF2m8z85prBQ"
AI_BID = "171092"                # Replace with your bot ID

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

async def fetch_ai_response(message):
    """Fetch a response from the AI API."""
    try:
        response = requests.get(
            f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
        )
        response.raise_for_status()
        return response.json().get("cnt", "I didn't get a response.")
    except Exception as e:
        logger.error(f"Error fetching AI response: {e}")
        return "I'm having trouble reaching my data source. Please try again later."

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message

    # Ignore commands or special messages
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return

    try:
        chatbotdb = MongoClient(MONGO_DB_URL)
        chatbotai = chatbotdb["Word"]["WordDb"]

        if not message.reply_to_message:
            K = []
            is_chat = chatbotai.find({"chat": chat.id, "word": message.text})
            for x in is_chat:
                K.append(x["text"])

            if K:
                hey = random.choice(K)
                is_text = chatbotai.find_one({"chat": chat.id, "text": hey})
                Yo = is_text.get("check", None)
            else:
                hey = await fetch_ai_response(message)
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
                    Yo = is_text.get("check", None)
                else:
                    hey = await fetch_ai_response(message)
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
        logger.error(f"Error in log_user: {e}")

# Register message handler
USER_HANDLER = MessageHandler(filters.ALL, log_user, block=False)
rani.add_handler(USER_HANDLER, USERS_GROUP)
