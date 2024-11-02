"""
ᴀɴ ᴀʀᴛɪғɪᴄɪᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ ғᴏʀ ᴘᴜʙʟɪᴄ ᴜsᴇs ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛs. ʙᴀsᴇᴅ ᴏɴ ᴘᴛʙ
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""

import asyncio
import importlib
import logging
import time
import requests

from telegram import Update
from telegram.ext import Application

from AsuX.modules import ALL_MODULES
from config import MONGO_DB_URL, TOKEN

AI_API_KEY = "RBPOWF2m8z85prBQ"
AI_BID = "171092"

StartTime = time.time()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Initialize the application
rani = Application.builder().token(TOKEN).build()

async def check_api_status():
    try:
        response = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&key={AI_API_KEY}&msg=test")
        response.raise_for_status()  # Raise an error for bad responses
        logger.info("API is reachable.")
    except requests.exceptions.RequestException as e:
        logger.error(f"API is not reachable: {e}")
        return False
    return True

async def main():
    # Check the API status before initializing the bot
    api_status = await check_api_status()
    if not api_status:
        print("API check failed. Exiting...")
        return
    
    await rani.bot.initialize()
    
    BOT_ID = rani.bot.id
    BOT_USERNAME = rani.bot.username

    print("ɪɴғᴏ: ʙᴏᴛᴛɪɴɢ ʏᴏᴜʟ ᴄʟɪᴇɴᴛ")
    print("sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴏᴀᴅᴇᴅ ᴍᴏᴅᴜʟᴇs -: " + str(ALL_MODULES))
    print(f"ɪɴғᴏ: ʙᴏᴛᴛɪɴɢ ʏᴏᴜʟ ᴄʟɪᴇɴᴛ ᴀs -: {BOT_USERNAME}")

# Run the bot
if __name__ == '__main__':
    asyncio.run(main())
    
