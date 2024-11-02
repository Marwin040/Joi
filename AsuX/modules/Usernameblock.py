"""
ɢɪᴛʜᴜʙ -Abishnoi69
ᴛᴇʟᴇɢʀᴀᴍ @Abishnoi1M / @Abishnoi_bots 

"""
import re

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from AsuX import rani


async def stop_chat_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat
    message = update.effective_message
    users = update.effective_user
    
    # Check if message.text is a string
    if not isinstance(message.text, str):
        return  # Exit if message.text is not a valid string

    links = re.findall(r"@[^\s]+", message.text)
    if not links:
        return
    
    chat_admins = await bot.getChatAdministrators(chat.id)
    admin_list = [x.user.id for x in chat_admins]
    
    if users.id in admin_list:
        return
    
    if (await chat.get_member(bot.id)).can_delete_messages:
        for link in links:
            try:
                user = await bot.get_chat(link)
                print(user.id)
                if len(str(user.id)) > 12:
                    await message.reply_text(
                        f"{users.first_name}, ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴀs ʜɪᴅᴅᴇɴ, ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ."
                    )
                    await message.delete()
            except Exception as e:
                print(f"Error: {e}")
                return



USER = 110
DEL_USERNAME = MessageHandler(
    filters.ALL & filters.ChatType.GROUPS,
    stop_chat_username,
    block=False,
)
rani.add_handler(DEL_USERNAME, USER)
