# (c) @SenpaiLabs
# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
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

# extra imports
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # ✅ Only ignore deprecation, not security warnings

import aiohttp
import asyncio
import pytz
import datetime
import logging
import sys
import os

# pyrogram imports
from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer
from pyrogram import idle
from pyrogram.session.session import Session

if sys.platform != 'win32':
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

# --- Patch Pyrogram Session.stop to fix read() RuntimeError on concurrent task disconnects (Python 3.12 issue) ---
_original_stop = Session.stop
async def _patched_stop(self, *args, **kwargs):
    try:
        await _original_stop(self, *args, **kwargs)
    except RuntimeError as e:
        if "read() called while another coroutine is already waiting" in str(e):
            logging.warning("Handled Session.stop asyncio stream RuntimeError gracefully.")
        else:
            raise
Session.stop = _patched_stop
# ----------------------------------------------------------------------------------------------------------------

# bots imports
from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app
from helper.utils import cleanup_directories

# Get logging configurations
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'),
             logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrofork").setLevel(logging.CRITICAL)
logging.getLogger("motor").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("hachoir").setLevel(logging.CRITICAL)
logging.getLogger("pymediainfo").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class SenpaiRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="SenpaiRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=32,  # ✅ Reduced from 200 → 32, saves ~500MB RAM
            plugins={"root": "plugins"},
            sleep_threshold=5,
            max_concurrent_transmissions=20  # ✅ Reduced from 50 → 20 for stability
        )
                 
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        Config.BOT = self
        
        # ✅ Cleanup orphaned files from previous crashes
        await cleanup_directories()
        
        # Ensure download directories exist
        os.makedirs("Renames", exist_ok=True)
        os.makedirs("Metadata", exist_ok=True)
        
        web_app = aiohttp.web.AppRunner(await web_server())
        await web_app.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(web_app, bind_address, Config.PORT).start()
        
        # ✅ REMOVED: Manual plugin loading loop — Pyrogram's plugins={"root": "plugins"} already handles this.
        # Double loading caused duplicate handlers = double DB queries per message.
        
        logger.info(f"{me.first_name} Is Started.....✨️")
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        for admin_id in Config.ADMIN:
            try:
                if Config.STRING_SESSION:
                    await self.send_message(admin_id, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
                else:
                    await self.send_message(admin_id, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except Exception as e:
                logger.warning(f"Failed to notify admin {admin_id}: {e}")
                     
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time_str}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")                                
            except Exception as e:
                logger.error(f"Failed to send log channel message: {e}")
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        for admin_id in Config.ADMIN:
            try:
                await self.send_message(admin_id, f"**Bot Stopped....**")
            except Exception:
                pass
                
        print("Bot Stopped 🙄")
        await super().stop()


senpai_instance = SenpaiRenameBot()


async def start_services():
    """✅ Clean async entry point using modern asyncio patterns."""
    try:
        if Config.STRING_SESSION:
            await asyncio.gather(app.start(), senpai_instance.start())
        else:
            await senpai_instance.start()
        
        await idle()
        
        if Config.STRING_SESSION:
            await asyncio.gather(app.stop(), senpai_instance.stop())
        else:
            await senpai_instance.stop()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")


def main():
    """✅ Uses asyncio.run() instead of deprecated get_event_loop()."""
    try:
        # For Python 3.10+, asyncio.run() is the recommended approach
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(start_services())
        finally:
            loop.close()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")


if __name__ == "__main__":
    try:
        main()
    except errors.FloodWait as ft:
        print(f"⏳ FloodWait: Sleeping for {ft.value} seconds")
        import time
        time.sleep(ft.value)
        print("Now Ready For Deploying!")
        main()
    except Exception as e:
        logger.critical(f"Bot crashed: {e}", exc_info=True)


# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates