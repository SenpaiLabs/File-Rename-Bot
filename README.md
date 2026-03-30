<div align="center">

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<img src="https://readme-typing-svg.herokuapp.com/?font=Orbitron&size=28&duration=3000&pause=500&color=4169E1&center=true&vCenter=true&width=700&lines=𓆩+SENPAI+RENAME+BOT+𓆪;Powered+By+SenpaiLabs+⚡" alt="Typing SVG" />

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<br>

<p align="center">
  <img src="https://files.catbox.moe/xu5jd8.jpg" alt="Senpai Rename Bot Banner" width="600" style="border-radius: 12px;">
</p>

<br>

<p align="center">
  <a href="https://github.com/SenpaiLabs/File-Rename-Bot/stargazers">
    <img src="https://img.shields.io/github/stars/SenpaiLabs/File-Rename-Bot?color=4169E1&style=for-the-badge&logo=github&label=STARS" />
  </a>
  <a href="https://github.com/SenpaiLabs/File-Rename-Bot/network/members">
    <img src="https://img.shields.io/github/forks/SenpaiLabs/File-Rename-Bot?color=00d4ff&style=for-the-badge&logo=github&label=FORKS" />
  </a>
  <a href="https://github.com/SenpaiLabs/File-Rename-Bot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/SenpaiLabs/File-Rename-Bot?color=purple&style=for-the-badge&label=LICENSE" />
  </a>
  <a href="https://github.com/SenpaiLabs/File-Rename-Bot/issues">
    <img src="https://img.shields.io/github/issues/SenpaiLabs/File-Rename-Bot?color=ff4444&style=for-the-badge&label=ISSUES" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Pyrogram-2.x-4169E1?style=flat-square" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-green?style=flat-square&logo=mongodb" />
  <img src="https://img.shields.io/badge/FFmpeg-Required-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Maintained-Yes-success?style=flat-square" />
</p>

</div>

---

## 𓆩 Oꜰꜰɪᴄɪᴀʟ Bᴏᴛꜱ 𓆪

<div align="center">

| Bot | Link |
|:---:|:---:|
| ⚡ Baka File Rename | [@BakaFileRename_bot](https://t.me/BakaFileRename_bot) |

</div>

---

## ✨ Fᴇᴀᴛᴜʀᴇꜱ

```
➥ ⚡ Ultra-Fast Renaming       — Zero lag, instant file processing
➥ 🖼️ Permanent Thumbnail       — Set once, applied forever
➥ 🔒 Force Subscribe           — Channel join enforcement built-in
➥ 📢 Smart Broadcast           — Rate-limited mass messaging
➥ ✏️ Custom Caption            — Dynamic placeholders supported
➥ 🔤 Prefix & Suffix           — Auto-append to every filename
➥ 🎬 Metadata Injection        — Title, Author, Stream tags via FFmpeg
➥ 👑 Premium System            — Tiers, trials, auto-expiry
➥ 🚫 Ban / Unban Members       — Admin-controlled user management
➥ 📊 Bot Statistics            — Live status & usage analytics
➥ ∞  Unlimited Concurrent Jobs — Process multiple files at once
➥ 🔁 Auto Restart              — Self-recovery with user broadcast
```

---

## ⚙️ Cᴏɴꜰɪɢᴜʀᴀᴛɪᴏɴ

### 🔴 Required Variables

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Get from [@BotFather](https://t.me/BotFather) |
| `API_ID` | From [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | From [my.telegram.org](https://my.telegram.org) |
| `ADMIN` | Your Telegram User ID (space-separated for multiple) |
| `DB_URL` | MongoDB Atlas URI from [cloud.mongodb.com](https://cloud.mongodb.com) |

### 🟡 Optional Variables

| Variable | Default | Description |
|---|---|---|
| `DB_NAME` | `Senpai_Rename_Bot` | MongoDB database name |
| `FORCE_SUB` | `None` | Channel username (without @) for force subscribe |
| `LOG_CHANNEL` | `None` | Channel ID for bot logs |
| `SENPAI_PIC` | `None` | Custom welcome image URL |

---

## 🚀 Dᴇᴘʟᴏʏ

<details>
<summary>📌 Deploy to VPS (Recommended)</summary>

```bash
# Step 1 — Install dependencies
sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git screen

# Step 2 — Clone the repo
git clone https://github.com/SenpaiLabs/File-Rename-Bot.git
cd File-Rename-Bot

# Step 3 — Configure environment
cp .env.example .env
nano .env   # Fill your credentials

# Step 4 — Install Python packages
pip3 install -r requirements.txt

# Step 5 — Run in background
python3 bot.py
# Press CTRL+A then D to detach
```

</details>

<details>
<summary>📌 Deploy to Heroku</summary>

<br>

<a href="https://heroku.com/deploy?template=https://github.com/SenpaiLabs/File-Rename-Bot">
  <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" width="220">
</a>

</details>

<details>
<summary>📌 Deploy to Koyeb</summary>

<br>

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/SenpaiLabs/File-Rename-Bot&env[BOT_TOKEN]&env[API_ID]&env[API_HASH]&env[ADMIN]&env[DB_URL]&env[DB_NAME]=Senpai_Rename_Bot&env[FORCE_SUB]&env[LOG_CHANNEL]&run_command=python%20bot.py&branch=main&name=senpai-rename)

</details>

<details>
<summary>📌 Deploy to Railway</summary>

<br>

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/SenpaiLabs/File-Rename-Bot)

</details>

<details>
<summary>📌 Deploy to Render</summary>

<br>

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SenpaiLabs/File-Rename-Bot)

</details>

---

## 📋 BotFather Commands

```
start          — Check if bot is alive
plans          — View premium plans
myplan         — Check your current plan
view_thumb     — See your saved thumbnail
del_thumb      — Delete saved thumbnail
set_caption    — Set a custom caption
see_caption    — View current caption
del_caption    — Delete custom caption
metadata       — Configure metadata tags
set_prefix     — Set filename prefix
see_prefix     — View current prefix
del_prefix     — Remove prefix
set_suffix     — Set filename suffix
see_suffix     — View current suffix
del_suffix     — Remove suffix

— Admin Only —
status         — Bot status & statistics
logs           — View bot logs
broadcast      — Message all users
addpremium     — Grant premium access
remove_premium — Revoke premium access
ban            — Ban a user
unban          — Unban a user
banned_users   — List all banned users
restart        — Restart bot + notify users
```

---

## 📞 Sᴜᴘᴘᴏʀᴛ

<div align="center">

| Platform | Link |
|:---:|:---:|
| 💬 Support Group | [@THE_DRAGON_SUPPORT](https://t.me/THE_DRAGON_SUPPORT) |
| 📢 Updates Channel | [@Senpai_Updates](https://t.me/Senpai_Updates) |

</div>

---

## ⚠️ Nᴏᴛᴇ

- Fork the repo, **do not import directly**
- **Do not remove credits** from any file
- Report bugs in our [support group](https://t.me/THE_DRAGON_SUPPORT)
- Unauthorized redistribution without credits is strictly prohibited

---

## ❣️ Cʀᴇᴅɪᴛꜱ

<div align="center">

**Built with 🖤 by [SenpaiLabs](https://github.com/SenpaiLabs)**

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

</div>