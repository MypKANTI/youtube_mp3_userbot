[English](docs/REDME_en.md])

<a href="https://t.me/Myp_KANTI"><img src="https://img.shields.io/badge/Мой Telegram-KANTI-blue?logo=Telegram"></a>

**User bot Download MP3 YouTube** 🎵

скрипт подключается к telegram аккаунту для отправки аудио из видео c **YouTube** работает так:

- 👂 Слушает пользователя на команды /
- 📥 Скачивает видео с ютуба через pytubefix
- 🎧 Конвертирует его в mp3
- 📥 Отправляет вам в чат

<img onerror="error banner" src="https://avatars.mds.yandex.net/i?id=5d8b757e262b191c9c9ac2d58326213a_l-12184902-images-thumbs&n=13">

## Доступные команды

- ℹ️ /help - список доступных команд
- 📥 /do [url YouTube] или /download_mp3 [url YouTube]
- 📊 /status - покажет статистику и статусы
- 🗑 /clear_cache - очистит кеш
- 🗑 /clear_count - очистка счётчика
- 📨 /send_log - отправка логов в чат
- 🎵 /list_music - список всей музыки

## Совместимо с (проверено лично)
| OS         | Статус  |
|------------|---------|
| Windows 11 | ✅       |
| Windows 10 | ✅       |
| Debian     | ✅       |

## ⚙️ Универсальная установка
Данная установка подойдёт для

- 🪟 Windows
- 🍏 iSH
- 📱 Termux

```bash
git clone https://github.com/MypKANTI/youtube_mp3_userbot.git

cd youtube_mp3_userbot

pip install -r requirements.txt

python main.py # Запуск
```

## 🚀 Установка uv
Для macOS или Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Для Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 📖 [Официальная документация uv](https://github.com/astral-sh/uv)

### ⚡ Установка через uv

Сначала установите uv (см. раздел «Установка uv» выше)

Подойдёт для большинства Linux-дистрибутивов:
Debian, Ubuntu, Kali Linux, Parrot OS, Arch Linux, Nyarch Linux, NixOS и других

```bash
git clone https://github.com/MypKANTI/youtube_mp3_userbot.git

cd youtube_mp3_userbot

uv sync

uv run python main.py # Запуск
```

### 💬 Комментарий автора
```
Данную программу я писал скорее для себя, а когда она стала реально полезной — решил выложить в открытый доступ.
Я люблю слушать музыку с ютуба, но подписки у меня нету, чтобы слушать музыку со свёрнутым приложением.
Также неудобно, что нельзя скачать нормально без подписки: приходилось лезть на сайты, писать в браузере что-то такое
«скачать видео с ютуба в формате mp3», и после находить нормальный сайт и при каждом скачивании смотреть рекламу.
Мне это надоело, и вот я написал такой простенький проект, который пошёл в моё портфолио.
```

# 🍀 Удачи :) 🍀
