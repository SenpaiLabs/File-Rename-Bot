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
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path, safe_edit_message
from helper.database import senpailabs
from helper.ffmpeg import change_metadata
from config import Config

# extra imports
from asyncio import sleep
import os, time, asyncio, datetime


UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
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
        remain = int(limit) - int(used)
        used_percentage = int(used) / int(limit) * 100
        if remain < int(senpai_file.file_size):
            return await message.reply_text(f"{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\nYou have only **{humanbytes(remain)}** Data.\nPlease, Buy Premium Plan s.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]]))
         
    if await senpailabs.has_premium_access(user_id) and client.premium:
        if not Config.STRING_SESSION:
            if senpai_file.file_size > 2000 * 1024 * 1024:
                 return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")

        try:
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            print(f"Error in rename_start: {e}")
    else:
        if senpai_file.file_size > 2000 * 1024 * 1024 and client.premium:
            return await message.reply_text("If you want to rename 4GB+ files then you will have to buy premium. /plans")

        try:
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            print(f"Error in rename_start (non-premium): {e}")


@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message if msg else None
        if not file or not file.media:
            await client.send_message(message.chat.id, "Original file not found. Please send the file again and rename it.")
            try:
                await reply_message.delete()
            except Exception:
                pass
            return
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
    Unified function to upload files based on type
    - Supports both 2GB and 4GB files
    - Uses same function for all file sizes
    - Handles document, video, and audio files
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
            
        # Upload document files (2GB & 4GB)
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, senpai_processing, time.time()))
        
        # Upload video files (2GB & 4GB)  
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, senpai_processing, time.time()))
        
        # Upload audio files (2GB & 4GB)
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
        
        # Return uploaded file object
        return filw, None
        
    except Exception as e:
        # Return error if upload fails
        return None, str(e)


#@Client.on_callback_query(filters.regex("upload"))
_UPLOAD_QUEUE_RUNNERS = {}


def _upload_task_id(user_id, chat_id, message_id):
    return f"{int(user_id)}:{int(chat_id)}:{int(message_id)}"


def _safe_task_dir(task_id):
    return str(task_id).replace(":", "_").replace("/", "_")


async def _remove_empty_dir(path):
    try:
        if path and os.path.isdir(path) and not os.listdir(path):
            os.rmdir(path)
    except Exception:
        pass


async def _cleanup_upload_files(*paths, dirs=None):
    await remove_path(*paths)
    for directory in dirs or []:
        await _remove_empty_dir(directory)


def _start_upload_queue_runner(bot, user_id):
    runner = _UPLOAD_QUEUE_RUNNERS.get(int(user_id))
    if runner and not runner.done():
        return
    _UPLOAD_QUEUE_RUNNERS[int(user_id)] = asyncio.create_task(_run_upload_queue(bot, int(user_id)))


async def resume_upload_queues(bot):
    await senpailabs.reset_running_upload_tasks()
    user_ids = await senpailabs.get_upload_queue_users()
    for user_id in user_ids:
        _start_upload_queue_runner(bot, user_id)


async def upload_doc(bot, update):
    task, error = await _build_upload_task(update)
    if error:
        await safe_edit_message(update.message, error)
        return

    await senpailabs.reset_stale_upload_tasks(task['user_id'])
    added = await senpailabs.add_upload_task(task)
    if not added:
        try:
            await update.answer("This file is already in queue.", show_alert=True)
        except Exception:
            pass
        _start_upload_queue_runner(bot, task['user_id'])
        return

    queue_size = await senpailabs.count_user_upload_tasks(task['user_id'])
    try:
        await update.answer("Added to upload queue.", show_alert=False)
    except Exception:
        pass

    if queue_size > Config.UPLOAD_QUEUE_LIMIT:
        await safe_edit_message(
            update.message,
            f"`Queued...`\n\nPosition: `{queue_size}`\nOnly `{Config.UPLOAD_QUEUE_LIMIT}` files process at a time."
        )
    else:
        await safe_edit_message(update.message, "`Queued...`")

    _start_upload_queue_runner(bot, task['user_id'])


async def _build_upload_task(update):
    if not update.message:
        return None, "Upload message not found. Please send the file again."

    file = update.message.reply_to_message
    if not file or not file.media:
        return None, "Original file not found. Please send the file again and rename it."

    new_name = update.message.text
    if not new_name or ":-" not in new_name:
        return None, "File name not found. Please send the file again and enter a new name."

    new_filename = new_name.split(":-", 1)[1].strip()
    if not new_filename:
        return None, "File name is empty. Please send the file again and enter a valid name."

    upload_type = update.data.split("#", 1)[1] if "#" in update.data else None
    if upload_type not in ["document", "video", "audio"]:
        return None, "Unknown upload type. Please select a valid output format."

    user_id = int(update.from_user.id)
    chat_id = int(update.message.chat.id)
    task_id = _upload_task_id(user_id, chat_id, update.message.id)
    return {
        '_id': task_id,
        'user_id': user_id,
        'chat_id': chat_id,
        'control_message_id': int(update.message.id),
        'source_message_id': int(file.id),
        'new_filename': new_filename,
        'upload_type': upload_type,
        'status': 'queued',
        'created_at': datetime.datetime.utcnow()
    }, None


async def _run_upload_queue(bot, user_id):
    try:
        await asyncio.sleep(1)
        while True:
            tasks = await senpailabs.claim_upload_tasks(user_id, Config.UPLOAD_QUEUE_LIMIT)
            if not tasks:
                break
            await asyncio.gather(*[_process_upload_task(bot, task) for task in tasks])
    finally:
        _UPLOAD_QUEUE_RUNNERS.pop(int(user_id), None)


async def _process_upload_task(bot, task):
    try:
        return await _upload_doc(bot, task)
    except Exception as e:
        print(f"Upload queue task failed: {e}")
        try:
            message = await bot.get_messages(int(task['chat_id']), int(task['control_message_id']))
            if message:
                await safe_edit_message(message, f"Upload Error: {e}")
        except Exception:
            pass
    finally:
        await senpailabs.delete_upload_task(task['_id'])


async def _upload_doc(bot, task):
    os.makedirs("Renames", exist_ok=True)
    os.makedirs("Metadata", exist_ok=True)

    user_id = int(task['user_id'])
    chat_id = int(task['chat_id'])
    senpai_processing = await bot.get_messages(chat_id, int(task['control_message_id']))
    if not senpai_processing:
        return

    await safe_edit_message(senpai_processing, "`Processing...`")

    file = await bot.get_messages(chat_id, int(task['source_message_id']))
    if not file or not file.media:
        return await safe_edit_message(senpai_processing, "Original file not found. Please send the file again and rename it.")

    new_filename_ = task['new_filename']
    user_data = await senpailabs.get_user_data(user_id)

    try:
        # adding prefix and suffix
        prefix = user_data.get('prefix', None)
        suffix = user_data.get('suffix', None)
        new_filename = await add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await safe_edit_message(senpai_processing, f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @SenpaiLabs\nError: {e}")

    media = getattr(file, file.media.value)
    
    # File paths for download and metadata
    task_dir = _safe_task_dir(task['_id'])
    rename_dir = os.path.join("Renames", task_dir)
    metadata_dir = os.path.join("Metadata", task_dir)
    os.makedirs(rename_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    file_path = os.path.join(rename_dir, new_filename)
    metadata_path = os.path.join(metadata_dir, new_filename)
    ph_path = None

    await safe_edit_message(senpai_processing, "`Try To Download....`")
    if bot.premium and bot.uploadlimit:
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)        
        total_used = int(used) + int(media.file_size)
        await senpailabs.set_used_limit(user_id, total_used)
    
    try:            
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, senpai_processing, time.time()))                    
    except Exception as e:
        if bot.premium and bot.uploadlimit:
            await senpailabs.set_used_limit(user_id, used)
        await _cleanup_upload_files(file_path, metadata_path, dirs=[rename_dir, metadata_dir])
        return await safe_edit_message(senpai_processing, f"Download Error: {e}")

    metadata_mode = await senpailabs.get_metadata_mode(user_id)
    if metadata_mode:        
        metadata = await senpailabs.get_metadata_code(user_id)
        if metadata:
            await safe_edit_message(senpai_processing, "I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
            if await change_metadata(dl_path, metadata_path, metadata):            
                await safe_edit_message(senpai_processing, "Metadata Added.....")
                print("Metadata Added.....")
            else:
                await safe_edit_message(senpai_processing, "Failed to add metadata, uploading original file...")
                metadata_mode = False
        else:
            await safe_edit_message(senpai_processing, "No metadata found, uploading original file...")
            metadata_mode = False
    else:
        await safe_edit_message(senpai_processing, "`Try To Uploading....`")
        
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata and metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if parser:
            parser.close()
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        pass
        
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)

    if c_caption:
         try:
             # adding custom caption 
             caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
         except Exception as e:
             if bot.premium and bot.uploadlimit:
                 await senpailabs.set_used_limit(user_id, used)
             await _cleanup_upload_files(ph_path, file_path, dl_path, metadata_path, dirs=[rename_dir, metadata_dir])
             return await safe_edit_message(senpai_processing, text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
         caption = f"**{new_filename}**"
 
    if (media.thumbs or c_thumb):
         # downloading thumbnail path
         try:
             if c_thumb:
                 ph_path = await bot.download_media(c_thumb) 
             else:
                 ph_path = await bot.download_media(media.thumbs[0].file_id)
             
             if ph_path and os.path.exists(ph_path):
                 Image.open(ph_path).convert("RGB").save(ph_path)
                 img = Image.open(ph_path)
                 img.resize((320, 320))
                 img.save(ph_path, "JPEG")
         except Exception as e:
             print(f"Error processing thumbnail: {e}")
             ph_path = None

    upload_type = task['upload_type']
    
    # Use the correct file path based on metadata mode
    final_file_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    
    if media.file_size > 2000 * 1024 * 1024:
        # Upload file using unified function for large files
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, final_file_path, 
            ph_path, caption, duration, senpai_processing
        )

        if error:
            if bot.premium and bot.uploadlimit:
                await senpailabs.set_used_limit(user_id, used)
            await _cleanup_upload_files(ph_path, file_path, dl_path, metadata_path, dirs=[rename_dir, metadata_dir])
            return await safe_edit_message(senpai_processing, f"Upload Error: {error}")

        
        from_chat = filw.chat.id
        mg_id = filw.id
        await asyncio.sleep(2)
        await bot.copy_message(user_id, from_chat, mg_id)
        await bot.delete_messages(from_chat, mg_id)
        
    else:
        # Upload file using unified function for regular files
        filw, error = await upload_files(
            bot, chat_id, upload_type, final_file_path,
            ph_path, caption, duration, senpai_processing
        )
                   
        if error:
            if bot.premium and bot.uploadlimit:
                await senpailabs.set_used_limit(user_id, used)
            await _cleanup_upload_files(ph_path, file_path, dl_path, metadata_path, dirs=[rename_dir, metadata_dir])
            return await safe_edit_message(senpai_processing, f"Upload Error: {error}")

    # Clean up files
    await _cleanup_upload_files(ph_path, file_path, dl_path, metadata_path, dirs=[rename_dir, metadata_dir])
    return await safe_edit_message(senpai_processing, "Uploaded Successfully....")


# @SenpaiLabs
# ✅ Team-SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
