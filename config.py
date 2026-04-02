# (c) @SenpaiLabs
# Telegram : https://t.me/THE_DRAGON_SUPPORT
# Source   : https://github.com/SenpaiLabs/File-Rename-Bot
# License  : Apache 2.0

"""
Apache License 2.0 — Copyright (c) 2022 @SenpaiLabs

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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""

from dotenv import load_dotenv
load_dotenv()

import re, os, time

id_pattern = re.compile(r'^-?\d+$')  # ✅ Fixed: was r'^.\d+$' which matched ANY char


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                     BOT CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Config:

    # ── Pyrogram Client ──────────────────────────────
    API_ID          = os.environ.get("API_ID", "")
    API_HASH        = os.environ.get("API_HASH", "")
    BOT_TOKEN       = os.environ.get("BOT_TOKEN", "")
    BOT             = None

    # ── User Session (Premium features) ─────────────
    STRING_SESSION  = os.environ.get("STRING_SESSION", "")

    # ── Database ─────────────────────────────────────
    DB_URL          = os.environ.get("DB_URL", "")
    DB_NAME         = os.environ.get("DB_NAME", "Senpai_Rename_Bot")

    # ── Bot Appearance ───────────────────────────────
    SENPAI_PIC      = os.environ.get("SENPAI_PIC", "https://files.catbox.moe/xu5jd8.jpg")
    ADMIN           = [
        int(a) if id_pattern.search(a) else a
        for a in os.environ.get("ADMIN", "6705898491").split()
    ]
    LOG_CHANNEL     = int(os.environ.get("LOG_CHANNEL", "-1002123429361"))

    # ── Upload Limits ────────────────────────────────
    FREE_UPLOAD_LIMIT   = 6 * 1024 * 1024 * 1024   # 6 GB
    UPLOAD_LIMIT_MODE   = True
    PREMIUM_MODE        = False

    # ── Force Subscribe ──────────────────────────────
    _force_sub_raw = os.environ.get("FORCE_SUB", "").strip()
    if _force_sub_raw:
        try:
            FORCE_SUB = int(_force_sub_raw)
        except ValueError:
            FORCE_SUB = _force_sub_raw  # Channel username
    else:
        FORCE_SUB = None  # ✅ Disabled when not set (was defaulting to "SenpaiLabs" and blocking ALL users)

    # ── Web Server ───────────────────────────────────
    PORT        = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME  = time.time()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                    BOT STRINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class senpai:

    # ── /start ───────────────────────────────────────
    START_TXT = """<b>ʜᴀɪ, {} 👋

ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ & ᴘᴏᴡᴇʀꜰᴜʟ ʀᴇɴᴀᴍᴇ ʙᴏᴛ.

• ʀᴇɴᴀᴍᴇ & ᴄʜᴀɴɢᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ᴀɴʏ ꜰɪʟᴇ
• ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏ ↔ ᴅᴏᴄᴜᴍᴇɴᴛ
• ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ꜱᴜᴘᴘᴏʀᴛ

ᴄʀᴇᴀᴛᴇᴅ ʙʏ : @SenpaiLabs 💞</b>"""

    # ── /about ───────────────────────────────────────
    ABOUT_TXT = """<b>╭───────────⍟
├ 🤖 ɴᴀᴍᴇ       : {}
├ 🖥️  ᴅᴇᴠᴇʟᴏᴘᴇʀ  : {}
├ 👨‍💻 ᴘʀᴏɢʀᴀᴍᴍᴇʀ : {}
├ 📕 ʟɪʙʀᴀʀʏ    : {}
├ ✏️  ʟᴀɴɢᴜᴀɢᴇ  : {}
├ 💾 ᴅᴀᴛᴀʙᴀꜱᴇ   : {}
├ 📊 ᴠᴇʀꜱɪᴏɴ    : <a href="https://github.com/SenpaiLabs/File-Rename-Bot">{}</a>
╰───────────────⍟</b>"""

    # ── /help ────────────────────────────────────────
    HELP_TXT = """<b>📖 ʜᴇʟᴘ ᴍᴇɴᴜ</b>

• /start — ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ

<b><u>✏️ ʜᴏᴡ ᴛᴏ ʀᴇɴᴀᴍᴇ ᴀ ꜰɪʟᴇ</u></b>
ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ → ᴛʏᴘᴇ ɴᴇᴡ ɴᴀᴍᴇ → ꜱᴇʟᴇᴄᴛ ꜰᴏʀᴍᴀᴛ
<code>[ document · video · audio ]</code>

ℹ️ ꜱᴜᴘᴘᴏʀᴛ : <a href="https://t.me/THE_DRAGON_SUPPORT">ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</a>"""

    # ── Premium Plans ────────────────────────────────
    UPGRADE_PREMIUM = """<b>💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ</b>

<code>ᴘʟᴀɴ       ᴅᴜʀᴀᴛɪᴏɴ    ᴘʀɪᴄᴇ</code>
🥉 ʙʀᴏɴᴢᴇ  — 3 ᴅᴀʏꜱ  —  ₹39
🥈 ꜱɪʟᴠᴇʀ  — 7 ᴅᴀʏꜱ  —  ₹59
🥇 ɢᴏʟᴅ    — 15 ᴅᴀʏꜱ —  ₹99
🏆 ᴘʟᴀᴛɪɴᴜᴍ — 1 ᴍᴏɴᴛʜ — ₹179
💎 ᴅɪᴀᴍᴏɴᴅ — 2 ᴍᴏɴᴛʜ — ₹339

✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ
🏷️ ₹9 ᴅɪꜱᴄᴏᴜɴᴛ ᴏɴ ᴀʟʟ ᴘʟᴀɴꜱ"""

    UPGRADE_PLAN = """<b>⭐ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ</b>

🔹 <b>ᴘʀᴏ</b>       — 1 ᴍᴏɴᴛʜ — ₹179 — 100 GB
🔸 <b>ᴜʟᴛʀᴀ ᴘʀᴏ</b> — 1 ᴍᴏɴᴛʜ — ₹199 — 1000 GB

🏷️ ₹9 ᴅɪꜱᴄᴏᴜɴᴛ ᴏɴ ᴀʟʟ ᴘʟᴀɴꜱ"""

    # ── Thumbnail ────────────────────────────────────
    THUMBNAIL = """<b>🌌 <u>ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴇᴛᴛɪɴɢꜱ</u></b>

• ꜱᴇɴᴅ ᴀɴʏ ᴘʜᴏᴛᴏ ᴛᴏ ꜱᴇᴛ ɪᴛ ᴀꜱ ᴛʜᴜᴍʙɴᴀɪʟ
• /del_thumb  — ᴅᴇʟᴇᴛᴇ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ
• /view_thumb — ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ"""

    # ── Custom Caption ───────────────────────────────
    CAPTION = """<b>📑 <u>ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ</u></b>

• /set_caption — ꜱᴇᴛ ᴀ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
• /see_caption — ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ
• /del_caption — ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ

<b>ᴇxᴀᴍᴘʟᴇ:</b>
<code>/set_caption 📕 ꜰɪʟᴇ: {filename}
💾 ꜱɪᴢᴇ: {filesize}
⏰ ᴅᴜʀᴀᴛɪᴏɴ: {duration}</code>"""

    # ── Bot Status ───────────────────────────────────
    BOT_STATUS = """<b>⚡ ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ ⚡</b>

⌚ ᴜᴘᴛɪᴍᴇ        : <code>{}</code>
👥 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ  : <code>{}</code>
💸 ᴘʀᴇᴍɪᴜᴍ       : <code>{}</code>
⬆️ ᴜᴘʟᴏᴀᴅ        : <code>{}</code>
⬇️ ᴅᴏᴡɴʟᴏᴀᴅ      : <code>{}</code>"""

    # ── Live Server Status ───────────────────────────
    LIVE_STATUS = """<b>⚡ ʟɪᴠᴇ ꜱᴇʀᴠᴇʀ ꜱᴛᴀᴛᴜꜱ ⚡</b>

⌚ ᴜᴘᴛɪᴍᴇ     : <code>{}</code>
🖥️  ᴄᴘᴜ        : <code>{}%</code>
🧠 ʀᴀᴍ        : <code>{}%</code>
💽 ᴛᴏᴛᴀʟ ᴅɪꜱᴋ : <code>{}</code>
📦 ᴜꜱᴇᴅ       : <code>{} — {}%</code>
📂 ꜰʀᴇᴇ       : <code>{}</code>
⬆️ ᴜᴘʟᴏᴀᴅ     : <code>{}</code>
⬇️ ᴅᴏᴡɴʟᴏᴀᴅ   : <code>{}</code>

<code>V3.0.0 [STABLE]</code>"""

    # ── Metadata ─────────────────────────────────────
    DIGITAL_METADATA = """<b>❪ ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴍᴇᴛᴀᴅᴀᴛᴀ ❫</b>

• /metadata — ꜱᴇᴛ / ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ

<b>ᴇxᴀᴍᴘʟᴇ:</b>
<code>--change-title @Senpai_Updates
--change-video-title @Senpai_Updates
--change-audio-title @Senpai_Updates
--change-subtitle-title @Senpai_Updates
--change-author @Senpai_Updates</code>

📥 ʜᴇʟᴘ: @SenpaiLabs"""

    SEND_METADATA = DIGITAL_METADATA  # alias

    # ── Custom File Name ─────────────────────────────
    CUSTOM_FILE_NAME = """<b><u>🖋️ ᴄᴜꜱᴛᴏᴍ ꜰɪʟᴇ ɴᴀᴍᴇ</u></b>

ᴀᴅᴅ ᴀ ᴘʀᴇꜰɪx ᴏʀ ꜱᴜꜰꜰɪx ᴛᴏ ʏᴏᴜʀ ꜰɪʟᴇɴᴀᴍᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.

• /set_prefix — ᴀᴅᴅ ᴘʀᴇꜰɪx ᴛᴏ ꜰɪʟᴇɴᴀᴍᴇ
• /see_prefix — ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ᴘʀᴇꜰɪx
• /del_prefix — ᴅᴇʟᴇᴛᴇ ᴘʀᴇꜰɪx
• /set_suffix — ᴀᴅᴅ ꜱᴜꜰꜰɪx ᴛᴏ ꜰɪʟᴇɴᴀᴍᴇ
• /see_suffix — ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ꜱᴜꜰꜰɪx
• /del_suffix — ᴅᴇʟᴇᴛᴇ ꜱᴜꜰꜰɪx

<b>ᴇxᴀᴍᴘʟᴇ:</b> <code>/set_suffix @SenpaiLabs</code>"""

    # ── Dev Credits ──────────────────────────────────
    DEV_TXT = """<b><u>ꜱᴘᴇᴄɪᴀʟ ᴛʜᴀɴᴋꜱ & ᴅᴇᴠᴇʟᴏᴘᴇʀꜱ</u></b>

» ꜱᴏᴜʀᴄᴇ : <a href="https://github.com/SenpaiLabs/File-Rename-Bot">File-Rename-Bot</a>

• ❣️ <a href="https://github.com/SenpaiLabs">SenpaiLabs</a>
• ❣️ <a href="https://t.me/THE_DRAGON_SUPPORT">ᴅʀᴀɢᴏɴ ᴄᴏᴍᴍᴜɴɪᴛʏ 🐉</a>
• ❣️ <a href="https://t.me/Senpai_Updates">ꜱᴇɴᴘᴀɪ ᴜᴘᴅᴀᴛᴇꜱ</a>"""

    # ── Progress Bar ─────────────────────────────────
    SENPAI_PROGRESS = """<b>

╭━━━━━━━━◉🚀◉━━━━━━━━╮
┃   ꜱᴇɴᴘᴀɪ ᴘʀᴏᴄᴇꜱꜱɪɴɢ...
┣━━━━━━━━━━━━━━━━━━━━╯
┣⪼ 📦 ꜱɪᴢᴇ  : {1} | {2}
┣⪼ 📊 ᴅᴏɴᴇ  : {0}%
┣⪼ 🚀 ꜱᴘᴇᴇᴅ : {3}/s
┣⪼ ⏰ ᴇᴛᴀ   : {4}
╰━━━━━━━━◉🔥◉━━━━━━━━╯</b>"""