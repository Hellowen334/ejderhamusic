import os
import re

import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaAudio,
                            InputMediaVideo, Message)

from config import (BANNED_USERS, SONG_DOWNLOAD_DURATION,
                    SONG_DOWNLOAD_DURATION_LIMIT)
from strings import get_command
from ArchMusic import YouTube, app
from ArchMusic.utils.decorators.language import language, languageCB
from ArchMusic.utils.formatters import convert_bytes
from ArchMusic.utils.inline.song import song_markup

# Command
SONG_COMMAND = get_command("SONG_COMMAND")


@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.group
    & ~BANNED_USERS
)

# Song Module


@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.private
    & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(
                    SONG_DOWNLOAD_DURATION, duration_min
                )
            )
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_back") & ~BANNED_USERS
)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_helper") & ~BANNED_USERS
)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(
                vidid, True
            )
        except:
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            check = x["format"]
            if "audio" in check:
                if x["filesize"] is None:
                    continue
                form = x["format_note"].title()
                if form not in done:
                    done.append(form)
                else:
                    continue
                sz = convert_bytes(x["filesize"])
                fom = x["format_id"]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Kalite = {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )
    else:
        try:
            formats_available, link = await YouTube.formats(
                vidid, True
            )
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        # AVC Formats Only [ ArchMusic Bot]
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            check = x["format"]
            if x["filesize"] is None:
                continue
            if int(x["format_id"]) not in done:
                continue
            sz = convert_bytes(x["filesize"])
            ap = check.split("-")[1]
            to = f"{ap} = {sz}"
            keyboard.row(
                InlineKeyboardButton(
                    text=to,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        )
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=keyboard
        )


# Downloading Songs Here


@app.on_callback_query(
    filters.regex(pattern=r"song_download") & ~BANNED_USERS
)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("İndiriliyor")
    except:
        pass
    
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    
    with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
        x = ytdl.extract_info(yturl, download=False)
    
    title = (x["title"]).title()
    title = re.sub("\W+", " ", title)
    thumb_image_path = await CallbackQuery.message.download()
    duration = x.get("duration", 0)
    
    if stype == "video":
        thumb_image_path = await CallbackQuery.message.download()
        width = CallbackQuery.message.photo.width
        height = CallbackQuery.message.photo.height
        
        try:
            file_path = await YouTube.download(
                yturl,
                mystic,
                songvideo=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))
        
        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        
        await mystic.edit_text(_["song_11"])
        
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_VIDEO,
        )
        
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        
        os.remove(file_path)
    
    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        res = (
            f"👤 Talep Eden : {CallbackQuery.from_user.mention}\n"
            f"🔮 Başlık : [{title[:23]}]({yturl})\n"
            f"⌛️ Süre : `{duration}`"
        )

        visit_button = InlineKeyboardButton(
            text="🎧 Ejderha Music", 
            url=f"https://t.me/musicarya"
        )

        visit_markup = InlineKeyboardMarkup(
            [[visit_button]]
        )
        
        med = InputMediaAudio(
            media=filename,
            caption=res,
            thumb=thumb_image_path,
            performer="@ejderhamusicbot"
        )
        
        await mystic.edit_text(_["song_11"])
        
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_AUDIO,
        )
        
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=visit_markup)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        
        rep = (
            f"👤 Talep Eden : {CallbackQuery.from_user.mention}\n"
            f"🔮 Başlık : [{title[:23]}]({yturl})\n"
            f"⌛️ Süre : `{duration}`"
        )
        
        channel_id = -1002352074297  # Önceki kanal ID'si
        
        # Arya Music kanalına gönder
        await app.send_audio(
            chat_id="@musicarya",  # Kanala kullanıcı adıyla gönder
            audio=filename,
            caption=rep,
            performer="@ejderhamusicbot",
            thumb=thumb_image_path,
        )
        
        os.remove(filename)
