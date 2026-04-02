# (c) @SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates

"""
Apache License 2.0
Copyright (c) 2022 @Senpai Labs

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

# extra imports
import math
import time
import re
import datetime
import pytz
import os
import logging
from config import Config, senpai 

# pyrogram imports
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    
    # ✅ Guard against ZeroDivisionError
    if diff < 0.1:
        return
        
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total if total > 0 else 0
        speed = current / diff if diff > 0 else 0
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000 if speed > 0 else 0
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["▣" for _ in range(math.floor(percentage / 5))]),
            ''.join(["▢" for _ in range(20 - math.floor(percentage / 5))])
        )            
        tmp = progress + senpai.SENPAI_PROGRESS.format( 
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),            
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]])                                               
            )
        except Exception:
            pass


def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] if tmp else "0 ꜱ"


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def send_log(b, u):
    if Config.LOG_CHANNEL:
        try:
            curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            log_message = (
                "**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
                f"Uꜱᴇʀ: {u.mention}\n"
                f"Iᴅ: `{u.id}`\n"
                f"Uɴ: @{u.username}\n\n"
                f"Dᴀᴛᴇ: {curr.strftime('%d %B, %Y')}\n"
                f"Tɪᴍᴇ: {curr.strftime('%I:%M:%S %p')}\n\n"
                f"By: {b.mention}"
            )
            await b.send_message(Config.LOG_CHANNEL, log_message)
        except Exception as e:
            logger.warning(f"Failed to send log: {e}")


async def get_seconds_first(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    parts = time_string.split()
    total_seconds = 0

    for i in range(0, len(parts), 2):
        if i + 1 >= len(parts):
            break
        try:
            value = int(parts[i])
        except ValueError:
            continue
        unit = parts[i+1].rstrip('s')
        total_seconds += value * conversion_factors.get(unit, 0)

    return total_seconds


async def get_seconds(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    total_seconds = 0
    pattern = r'(\d+)\s*(\w+)'
    matches = re.findall(pattern, time_string)

    for value, unit in matches:
        total_seconds += int(value) * conversion_factors.get(unit, 0)

    return total_seconds


async def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.(\w+))?$'
    match = re.search(pattern, input_string)
    
    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''
        
        prefix_str = f"{prefix} " if prefix else ""
        suffix_str = f" {suffix}" if suffix else ""
        
        return f"{prefix_str}{filename}{suffix_str}{extension}"
    else:
        return input_string


async def remove_path(*paths):
    """✅ Safe file cleanup with error handling."""
    for path in paths:
        if path and os.path.lexists(path):
            try:
                os.remove(path)
            except OSError as e:
                logger.warning(f"Failed to remove file {path}: {e}")


async def cleanup_directories():
    """✅ Startup cleanup — remove orphaned files from Renames/ and Metadata/."""
    for directory in ["Renames", "Metadata"]:
        if os.path.isdir(directory):
            count = 0
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        count += 1
                except OSError as e:
                    logger.warning(f"Cleanup failed for {filepath}: {e}")
            if count > 0:
                logger.info(f"Cleanup: Removed {count} orphaned files from {directory}/")


async def metadata_text(metadata_text_str):
    author = None
    title = None
    video_title = None
    audio_title = None
    subtitle_title = None

    flags = [i.strip() for i in metadata_text_str.split('--')]
    for f in flags:
        if f.startswith("change-author"):
            author = f[len("change-author"):].strip()
        elif f.startswith("change-video-title"):
            video_title = f[len("change-video-title"):].strip()
        elif f.startswith("change-audio-title"):
            audio_title = f[len("change-audio-title"):].strip()
        elif f.startswith("change-subtitle-title"):
            subtitle_title = f[len("change-subtitle-title"):].strip()
        elif f.startswith("change-title"):
            title = f[len("change-title"):].strip()

    return author, title, video_title, audio_title, subtitle_title


# (c) @SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
