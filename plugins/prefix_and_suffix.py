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

# imports
from pyrogram import Client, filters, enums
from helper.database import senpailabs

# prefix commond ✨
@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_prefix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @SenpaiLabs`**")
    prefix = message.text.split(" ", 1)[1]
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await senpailabs.set_prefix(message.from_user.id, prefix)
    await senpai.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")

@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await senpailabs.get_prefix(message.from_user.id)
    if not prefix:
        return await senpai.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await senpailabs.set_prefix(message.from_user.id, None)
    await senpai.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_prefix(client, message):
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await senpailabs.get_prefix(message.from_user.id)
    if prefix:
        await senpai.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`")
    else:
        await senpai.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")

# SUFFIX COMMOND ✨
@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_suffix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @SenpaiLabs`**")
    suffix = message.text.split(" ", 1)[1]
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await senpailabs.set_suffix(message.from_user.id, suffix)
    await senpai.edit("__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__")

@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await senpailabs.get_suffix(message.from_user.id)
    if not suffix:
        return await senpai.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
    await senpailabs.set_suffix(message.from_user.id, None)
    await senpai.edit("__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_suffix(client, message):
    senpai = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await senpailabs.get_suffix(message.from_user.id)
    if suffix:
        await senpai.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await senpai.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")

# SenpaiLabs Developer 
# Don't Remove Credit 😔
# Telegram Channel @Senpai_Updates & @THE_DRAGON_SUPPORT
# Developer @SenpaiLabs
# Update Channel @THE_DRAGON_SUPPORT & @Senpai_Updates
