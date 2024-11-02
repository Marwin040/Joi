"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""

import random
import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from AsuX import *

USERS_GROUP = 11

# Configuration
MONGO_DB_URL = "mongodb+srv://marwin0985:BEwJvxaADStDLScc@cluster0.oh0nk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TOKEN = "7343734756:AAFQJ1lYOgmroGBazwWfP-HC9jAMFSTGv08"
AI_API_KEY = "RBPOWF2m8z85prBQ"
AI_BID = "171092"

# MongoDB client setup
chatbotdb = MongoClient(MONGO_DB_URL)
chatbotai = chatbotdb["Word"]["WordDb"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI chatbot. How can I assist you today?")

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message

    # Ignore commands
    if message.text.startswith(("!", "/", "?", "@", "#")):
        return

    # Check for a reply to a message
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == BOT_ID:
            await handle_reply(chat.id, message)
    else:
        await handle_message(chat.id, message)

async def handle_message(chat_id, message):
    # Look for predefined responses
    responses = list(chatbotai.find({"chat": chat_id, "word": message.text}))
    if responses:
        reply = random.choice(responses)
        response_text = reply["text"]
        response_type = reply["check"]
    else:
        # Get response from AI
        response = requests.get(
            f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
        ).json()
        response_text = response["cnt"]
        response_type = None

    if response_type == "sticker":
        await message.reply_sticker(response_text)
    else:
        await message.reply_text(response_text)

async def handle_reply(chat_id, message):
    # Log the sticker or text response to the database
    if message.sticker:
        # Handle sticker
        chatbotai.update_one(
            {"chat": chat_id, "word": message.reply_to_message.text, "id": message.sticker.file_unique_id},
            {"$setOnInsert": {
                "text": message.sticker.file_id,
                "check": "sticker",
                "id": message.sticker.file_unique_id
            }},
            upsert=True
        )
    elif message.text:
        # Handle text
        chatbotai.update_one(
            {"chat": chat_id, "word": message.reply_to_message.text, "text": message.text},
            {"$setOnInsert": {
                "check": "none"
            }},
            upsert=True
        )

def main():
    application = ApplicationBuilder().token("your_telegram_bot_token").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_user))

    application.run_polling()

if __name__ == "__main__":
    main()
    
    USER_HANDLER = MessageHandler(filters.ALL, log_user, block=False)
rani.add_handler(USER_HANDLER, USERS_GROUP)
