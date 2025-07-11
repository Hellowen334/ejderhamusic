#
# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >.
#
# This file is part of < https://github.com/ArchBots/ArchMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/ArchBots/ArchMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
from random import randint

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message, InlineKeyboardMarkup, InlineKeyboardButton

import config
from config import BANNED_USERS
from strings import get_command
from ArchMusic import app
from ArchMusic.misc import db
from ArchMusic.utils import (ArchMusicbin, get_channeplayCB,
                              seconds_to_min)
from ArchMusic.utils.database import (get_cmode, is_active_chat,
                                       is_music_playing)
from ArchMusic.utils.decorators.language import language, languageCB
from ArchMusic.utils.inline import queue_back_markup, queue_markup

###Commands
QUEUE_COMMAND = get_command("QUEUE_COMMAND")

basic = {}


def get_image(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"
    else:
        return config.YOUTUBE_IMG_URL


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "Unknown"
    else:
        return "Inline"


@app.on_message(
    filters.command(QUEUE_COMMAND) 
    & filters.group 
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except:
            return await message.reply_text(_["cplay_4"])
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    got = db.get(chat_id)
    if not got:
        return await message.reply_text(_["queue_2"])
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "**⌛️Süre:** Bilinmeyen Süre Akışı\n\nTüm sıralanmış listeyi almak için aşağıdaki düğmeye tıklayın."
        if DUR == "Unknown"
        else "\nTüm sıralanmış listeyi almak için aşağıdaki butona tıklayın."
    )
    cap = f"""**{config.MUSIC_BOT_NAME} Player**

🎥**Oynatılıyor:** {title}

🔗**Yayın Türü:** {typo}
🙍‍♂️**Talep eden:** {user}
{send}"""
    upl = (
        queue_markup(_, DUR, "c" if cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            "c" if cplay else "g",
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True
    mystic = await message.reply_photo(
        IMAGE, caption=cap, reply_markup=upl
    )
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _,
                                    DUR,
                                    "c" if cplay else "g",
                                    videoid,
                                    seconds_to_min(
                                        db[chat_id][0]["played"]
                                    ),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(
                                    reply_markup=buttons
                                )
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except:
            return


@app.on_callback_query(filters.regex("GetTimer") & ~BANNED_USERS)
async def quite_timer(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass


@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
@languageCB
async def queued_tracks(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id, channel = await get_channeplayCB(
            _, what, CallbackQuery
        )
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(
            _["general_6"], show_alert=True
        )
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer(
            _["queue_2"], show_alert=True
        )
    if len(got) == 1:
        return await CallbackQuery.answer(
            _["queue_5"], show_alert=True
        )
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(_, what)
    
    # Kapat butonu ekle
    buttons.append(
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], callback_data="close"
            )
        ]
    )
    
    # Albüm kapağını al
    if videoid != "None":
        try:
            from ArchMusic.platforms import YouTube
            img = await YouTube.thumbnail(videoid, True)
        except:
            img = "https://telegra.ph//file/6f7d35131f69951c74ee5.jpg"
    else:
        img = "https://telegra.ph//file/6f7d35131f69951c74ee5.jpg"
    
    med = InputMediaPhoto(
        media=img,
        caption=_["queue_1"],
    )
    await CallbackQuery.edit_message_media(media=med)
    j = 0
    msg = ""
    for x in got:
        j += 1
        if j == 1:
            msg += f'Şu anda oynatılıyor:\n\n🏷Başlık: {x["title"]}\nSüre: {x["dur"]}\nTalep Eden: {x["by"]}\n\n'
        elif j == 2:
            msg += f'Sıradaki:\n\n🏷Başlık: {x["title"]}\nSüre: {x["dur"]}\nTalep Eden: {x["by"]}\n\n'
        else:
            msg += f'🏷Başlık: {x["title"]}\nSüre: {x["dur"]}\nTalep Eden: {x["by"]}\n\n'
    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(
                msg, reply_markup=buttons
            )
        if "🏷" in msg:
            msg = msg.replace("🏷", "")
        link = await ArchMusicbin(msg)
        med = InputMediaPhoto(
            media=link, caption=_["queue_3"].format(link)
        )
        await CallbackQuery.edit_message_media(
            media=med, reply_markup=buttons
        )
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(
            msg, reply_markup=buttons
        )


@app.on_callback_query(
    filters.regex("queue_back_timer") & ~BANNED_USERS
)
@languageCB
async def queue_back(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplayCB(
            _, cplay, CallbackQuery
        )
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(
            _["general_6"], show_alert=True
        )
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer(
            _["queue_2"], show_alert=True
        )
    await CallbackQuery.answer(_["set_cb_8"], show_alert=True)
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "**⌛️Süre:**Bilinmeyen Süre Akışı\n\nTüm sıralanmış listeyi almak için aşağıdaki düğmeye tıklayın."
        if DUR == "Unknown"
        else "\nTüm sıralanmış listeyi almak için aşağıdaki butona tıklayın."
    )
    cap = f"""**{config.MUSIC_BOT_NAME} Player**

🎥**Oynatılıyor:** {title}

🔗**Yayın Türü:** {typo}
🙍‍♂️**Talep eden:** {user}
{send}"""
    
    # Kapat butonu ekle
    if DUR == "Unknown":
        upl_copy = queue_markup(_, DUR, cplay, videoid)
    else:
        upl_copy = queue_markup(
            _,
            DUR,
            cplay,
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    
    upl_copy.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], callback_data="close"
            )
        ]
    )
    
    basic[videoid] = True

    med = InputMediaPhoto(media=IMAGE, caption=cap)
    mystic = await CallbackQuery.edit_message_media(
        media=med, reply_markup=upl_copy
    )
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _,
                                    DUR,
                                    cplay,
                                    videoid,
                                    seconds_to_min(
                                        db[chat_id][0]["played"]
                                    ),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(
                                    reply_markup=buttons
                                )
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except:
            return

    position = len(db.get(chat_id)) - 1
    
    # Sıradaki parça için albüm kapağını al
    img = get_image(videoid)
    
    buttons = [
        [
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], callback_data="close"
            )
        ]
    ]
    
    await app.send_photo(
        chat_id,
        photo=img,
        caption=_["queue_4"].format(
            position, title, DUR, user
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
