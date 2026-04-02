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
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import senpailabs
from helper.ffmpeg import change_metadata
from config import Config

# extra imports
import os
import time
import asyncio
import logging

logger = logging.getLogger(__name__)

UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)


# ✅ DRY: Extracted media info text into a reusable function
def _build_media_info_text(filename, extension_type, filesize, mime_type, dcid):
    return (
        f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n"
        f"◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n"
        f"◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n"
        f"◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n"
        f"◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n"
        f"◈ ᴅᴄ ɪᴅ: `{dcid}`\n\n"
        f"ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**"
    )


async def _send_rename_prompt(message, filename, extension_type, filesize, mime_type, dcid):
    """✅ DRY: Sends the rename prompt with retry on FloodWait."""
    media_info = _build_media_info_text(filename, extension_type, filesize, mime_type, dcid)
    try:
        await message.reply_text(
            text=media_info,
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True)
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text(
            text=media_info,
            reply_to_message_id=message.id,  
            reply_markup=ForceReply(True)
        )


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id = message.from_user.id
    senpai_file = getattr(message, message.media.value)
    filename = senpai_file.file_name
    filesize = humanbytes(senpai_file.file_size)
    mime_type = senpai_file.mime_type
    dcid = FileId.decode(senpai_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    if client.premium and client.uploadlimit:
        await senpailabs.reset_uploadlimit_access(user_id)
        user_data = await senpailabs.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        
        # ✅ Guard against ZeroDivisionError
        if int(limit) > 0:
            remain = int(limit) - int(used)
            used_percentage = int(used) / int(limit) * 100
        else:
            remain = 0
            used_percentage = 100
            
        if remain < int(senpai_file.file_size):
            return await message.reply_text(
                f"{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n"
                f" Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\n"
                f"You have only **{humanbytes(remain)}** Data.\n"
                f"Please, Buy Premium Plan s.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]])
            )
         
    if await senpailabs.has_premium_access(user_id) and client.premium:
        if not Config.STRING_SESSION:
            if senpai_file.file_size > 2000 * 1024 * 1024:
                return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")

        try:
            await _send_rename_prompt(message, filename, extension_type, filesize, mime_type, dcid)
        except Exception as e:
            logger.error(f"Error in rename_start (premium): {e}")
    else:
        if senpai_file.file_size > 2000 * 1024 * 1024 and client.premium:
            return await message.reply_text("If you want to rename 4GB+ files then you will have to buy premium. /plans")

        try:
            await _send_rename_prompt(message, filename, extension_type, filesize, mime_type, dcid)
        except Exception as e:
            logger.error(f"Error in rename_start (non-premium): {e}")


@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if media and hasattr(media, 'file_name') and media.file_name and "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload#document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload#video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload#audio")])
        await message.reply(
            text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )


async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, senpai_processing):
    """
    Unified function to upload files based on type.
    Supports both 2GB and 4GB files, handles document, video, and audio files.
    """
    try:
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
            
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, senpai_processing, time.time()))
        
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, senpai_processing, time.time()))
        
        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, senpai_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"
        
        return filw, None
        
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return None, f"FloodWait: Please try again after {e.value}s"
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return None, str(e)


async def upload_doc(bot, update):
    senpai_processing = await update.message.edit("`Processing...`")
    
    # ✅ Ensure directories exist
    os.makedirs("Metadata", exist_ok=True)
    os.makedirs("Renames", exist_ok=True)

    user_id = int(update.message.chat.id) 
    new_name = update.message.text
    new_filename_ = new_name.split(":-")[1]
    
    # ✅ Single DB call instead of multiple
    user_data = await senpailabs.get_user_data(user_id)

    try:
        prefix = user_data.get('prefix', None)
        suffix = user_data.get('suffix', None)
        new_filename = await add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await senpai_processing.edit(f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @SenpaiLabs\nError: {e}")

    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
    
    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"

    await senpai_processing.edit("`Try To Download....`")
    
    if bot.premium and bot.uploadlimit:
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)        
        total_used = int(used) + int(media.file_size)
        await senpailabs.set_used_limit(user_id, total_used)
    
    try:            
        dl_path = await bot.download_media(
            message=file, file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=(DOWNLOAD_TEXT, senpai_processing, time.time())
        )
    except Exception as e:
        if bot.premium and bot.uploadlimit:
            # ✅ Guard against negative: only subtract what was added
            used_remove = max(0, int(used))
            await senpailabs.set_used_limit(user_id, used_remove)
        return await senpai_processing.edit(f"Download Error: {e}")

    metadata_mode = user_data.get('metadata_mode', False)  # ✅ Use cached user_data
    if metadata_mode:        
        metadata_code = user_data.get('metadata_code', None)  # ✅ Use cached user_data
        if metadata_code:
            await senpai_processing.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")            
            if await change_metadata(dl_path, metadata_path, metadata_code):            
                await senpai_processing.edit("Metadata Added.....")
                logger.info("Metadata Added.")
            else:
                await senpai_processing.edit("Failed to add metadata, uploading original file...")
                metadata_mode = False
        else:
            await senpai_processing.edit("No metadata found, uploading original file...")
            metadata_mode = False
    else:
        await senpai_processing.edit("`Try To Uploading....`")
        
    duration = 0
    try:
        parser = createParser(file_path)
        if parser:
            metadata = extractMetadata(parser)
            if metadata and metadata.has("duration"):
                duration = metadata.get('duration').seconds
            parser.close()
    except Exception as e:
        logger.warning(f"Error extracting metadata: {e}")
        
    ph_path = None
    c_caption = user_data.get('caption', None)  # ✅ Use cached user_data
    c_thumb = user_data.get('file_id', None)  # ✅ Use cached user_data

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
        except Exception as e:
            if bot.premium and bot.uploadlimit:
                used_remove = max(0, int(used))
                await senpailabs.set_used_limit(user_id, used_remove)
            return await senpai_processing.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")             
    else:
        caption = f"**{new_filename}**"
 
    if (media.thumbs or c_thumb):
        try:
            if c_thumb:
                ph_path = await bot.download_media(c_thumb) 
            else:
                ph_path = await bot.download_media(media.thumbs[0].file_id)
             
            if ph_path and os.path.exists(ph_path):
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img = img.resize((320, 320))  # ✅ Fixed: capture the result of resize()
                img.save(ph_path, "JPEG")
        except Exception as e:
            logger.warning(f"Error processing thumbnail: {e}")
            ph_path = None

    upload_type = update.data.split("#")[1]
    
    # Use the correct file path based on metadata mode
    final_file_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    
    if media.file_size > 2000 * 1024 * 1024:
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, final_file_path, 
            ph_path, caption, duration, senpai_processing
        )

        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = max(0, int(used))
                await senpailabs.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await senpai_processing.edit(f"Upload Error: {error}")

        from_chat = filw.chat.id
        mg_id = filw.id
        await asyncio.sleep(2)
        await bot.copy_message(update.from_user.id, from_chat, mg_id)
        try:
            await bot.delete_messages(from_chat, mg_id)
        except Exception as e:
            logger.warning(f"Failed to delete forwarded message: {e}")
        
    else:
        filw, error = await upload_files(
            bot, update.message.chat.id, upload_type, final_file_path, 
            ph_path, caption, duration, senpai_processing
        )
                   
        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = max(0, int(used))
                await senpailabs.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await senpai_processing.edit(f"Upload Error: {error}")        

    # Clean up files
    await remove_path(ph_path, file_path, dl_path, metadata_path)
    return await senpai_processing.edit("Uploaded Successfully....")


# @SenpaiLabs
# ✅ Team-SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
