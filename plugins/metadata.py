# (c) @SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
"""
Apache License 2.0
Copyright (c) 2022 @SenpaiLabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Telegram Link : https://t.me/THE_DRAGON_SUPPORT
Repo Link : https://github.com/SenpaiLabs/File-Rename-Bot
License Link : https://github.com/SenpaiLabs/File-Rename-Bot/blob/main/LICENSE
"""

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, MessageNotModified
import asyncio

# extra imports
import logging
from helper.database import senpailabs
from config import Config, senpai

logger = logging.getLogger(__name__)

TRUE = [[InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ ᴏɴ', callback_data='metadata_1'),
       InlineKeyboardButton('✅', callback_data='metadata_1')
       ],[
       InlineKeyboardButton('Sᴇᴛ Cᴜsᴛᴏᴍ Mᴇᴛᴀᴅᴀᴛᴀ', callback_data='cutom_metadata')]]
FALSE = [[InlineKeyboardButton('ᴍᴇᴛᴀᴅᴀᴛᴀ ᴏғғ', callback_data='metadata_0'),
        InlineKeyboardButton('❌', callback_data='metadata_0')
       ],[
       InlineKeyboardButton('Sᴇᴛ Cᴜsᴛᴏᴍ Mᴇᴛᴀᴅᴀᴛᴀ', callback_data='cutom_metadata')]]


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):
    senpai_msg = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    bool_metadata = await senpailabs.get_metadata_mode(message.from_user.id)
    user_metadata = await senpailabs.get_metadata_code(message.from_user.id)

    await senpai_msg.edit(
        f"Your Current Metadata:-\n\n➜ `{user_metadata}`",
        reply_markup=InlineKeyboardMarkup(TRUE if bool_metadata else FALSE)
    )


@Client.on_callback_query(filters.regex('.*?(custom_metadata|metadata).*?'))
async def query_metadata(bot: Client, query: CallbackQuery):
    data = query.data
    if data.startswith('metadata_'):
        # ✅ SECURITY FIX: Replaced dangerous eval() with safe int() conversion
        try:
            _bool_str = data.split('_')[1]
            bool_meta = bool(int(_bool_str))  # ✅ Safe: only converts "0" or "1"
        except (ValueError, IndexError):
            logger.warning(f"Invalid metadata callback data: {data}")
            return
            
        user_metadata = await senpailabs.get_metadata_code(query.from_user.id)
        await senpailabs.set_metadata_mode(query.from_user.id, bool_meta=not bool_meta)
        await query.message.edit(
            f"Your Current Metadata:-\n\n➜ `{user_metadata}`",
            reply_markup=InlineKeyboardMarkup(FALSE if bool_meta else TRUE)
        )
           
    elif data == 'cutom_metadata':
        await query.message.delete()
        try:
            metadata = await bot.ask(
                text=senpai.SEND_METADATA, 
                chat_id=query.from_user.id, 
                filters=filters.text, 
                timeout=30, 
                disable_web_page_preview=True
            )
            senpai_msg = await query.message.reply_text("**Please Wait...**", reply_to_message_id=metadata.id)
            await senpailabs.set_metadata_code(query.from_user.id, metadata_code=metadata.text)
            await senpai_msg.edit("**Your Metadata Code Set Successfully ✅**")
        except Exception as e:
            if type(e).__name__ == "ListenerTimeout" or isinstance(e, asyncio.TimeoutError):
                await query.message.reply_text(
                    "⚠️ Error!!\n\n**Request timed out.**\nRestart by using /metadata",
                    reply_to_message_id=query.message.id
                )
            else:
                logger.error(f"Metadata set error: {e}")


# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
