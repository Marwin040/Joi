"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""

import random
import requests
import re
from pymongo import MongoClient
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from requests.exceptions import Timeout, RequestException
import logging

# Configuration - replace with your actual values
MONGO_DB_URL = "mongodb+srv://marwin0985:BEwJvxaADStDLScc@cluster0.oh0nk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TOKEN = "7343734756:AAFQJ1lYOgmroGBazwWfP-HC9jAMFSTGv08"
AI_API_KEY = "RBPOWF2m8z85prBQ"
AI_BID = "171092"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)

async def fetch_response(message, retries=3):
    """Fetch a response from the AI API."""
    url = f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("cnt", "I didn't get a response.")
        except Timeout:
            logger.warning("Request timed out. Retrying...")
        except RequestException as e:
            logger.error(f"Request error: {e}")
            return "There seems to be an issue with the connection. Please try again later."
    
    return "I'm still having trouble reaching my data source. Please try again later."

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""
    chat = update.effective_chat
    message = update.effective_message

    logger.info(f"Received message: {message.text}")

    # Ignore commands or special messages
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return

    try:
        # Check if message.text is a string
        if not isinstance(message.text, str):
            logger.error("Message text is not a string.")
            return
        
        chatbotdb = MongoClient(MONGO_DB_URL)
        chatbotai = chatbotdb["Word"]["WordDb"]
        logger.info("Connected to MongoDB successfully.")

        if not message.reply_to_message:
            response_texts = [x["text"] for x in chatbotai.find({"chat": chat.id, "word": message.text})]
            if response_texts:
                response = random.choice(response_texts)
            else:
                response = await fetch_response(message)

            await message.reply_text(response)
        else:
            if message.reply_to_message.from_user.id == context.bot.id:
                response_texts = [x["text"] for x in chatbotai.find({"chat": chat.id, "word": message.text})]
                if response_texts:
                    response = random.choice(response_texts)
                else:
                    response = await fetch_response(message)

                await message.reply_text(response)

    except Exception as e:
        logger.error(f"Error in log_user: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a message to the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_chat:
        await update.effective_chat.send_message("An error occurred. Please try again later.")

# Initialize the application
rani = Application.builder().token(TOKEN).build()

# Add message handler
USER_HANDLER = MessageHandler(filters.TEXT & ~filters.COMMAND, log_user)
rani.add_handler(USER_HANDLER)

# Add error handler
rani.add_error_handler(error_handler)

if __name__ == '__main__':
    logger.info("Starting the bot...")
    rani.run_polling()
