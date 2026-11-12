<a href="https://t.me/Myp_KANTI"><img src="https://img.shields.io/badge/My Telegram-KANTI-blue?logo=Telegram"></a>

**YouTube MP3 Download User Bot** 🎵

The script connects to a Telegram account and sends audio from **YouTube** videos. How it works:

- 👂 Listens for commands from the user
- 📥 Downloads the video from YouTube via pytubefix
- 🎧 Converts it to MP3
- 📥 Sends it to your chat

<img onerror="error banner" src="https://avatars.mds.yandex.net/i?id=5d8b757e262b191c9c9ac2d58326213a_l-12184902-images-thumbs&n=13">

## Available Commands

- ℹ️ `/help` — list of available commands
- 📥 `/do [YouTube URL]` or `/download_mp3 [YouTube URL]` — download audio
- 📊 `/status` — show statistics and statuses
- 🗑 `/clear_cache` — clear the cache
- 🗑 `/clear_count` — reset the counter
- 📨 `/send_log` — send logs to the chat
- 🎵 `/list_music` — list all downloaded tracks

## Compatibility (personally tested)

| OS          | Status |
|-------------|--------|
| Windows 11  | ✅     |
| Windows 10  | ✅     |
| Debian      | ✅     |

## ⚙️ Universal Installation
This installation works for:

- 🪟 Windows
- 🍏 iSH
- 📱 Termux

```bash
git clone https://github.com/MypKANTI/youtube_mp3_userbot.git

cd youtube_mp3_userbot

pip install -r requirements.txt

python main.py # Run

## 🚀 Installing uv
For macOS or Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 📖 [Official uv documentation](https://github.com/astral-sh/uv)

### ⚡Installation via uv

First install uv (see the "Installing uv" section above).

Suitable for most Linux distributions:
Debian, Ubuntu, Kali Linux, Parrot OS, Arch Linux, Nyarch Linux, NixOS, and others.


```bash
git clone https://github.com/MypKANTI/youtube_mp3_userbot.git

cd youtube_mp3_userbot

uv sync

uv run python main.py # Запуск
```

### 💬 Author's note
```
I originally wrote this program mostly for myself, and once it became genuinely
useful I decided to release it publicly.
I love listening to music from YouTube, but I don't have a subscription to
listen with the app minimized. It's also inconvenient that you can't just
download audio without a subscription — you had to go to some website, search
"download youtube video mp3", find a decent one, and watch ads every single
time. I got tired of it, so I wrote this simple project, which also became part
of my portfolio.
```

# 🍀 Good luck :) 🍀
