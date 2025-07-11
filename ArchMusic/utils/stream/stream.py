import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
from ArchMusic import Carbon, YouTube, app
from ArchMusic.core.call import ArchMusic
from ArchMusic.misc import db
from ArchMusic.utils.database import (add_active_chat,
                                       add_active_video_chat,
                                       is_active_chat,
                                       is_video_allowed, music_on)
from ArchMusic.utils.exceptions import AssistantErr
from ArchMusic.utils.inline.play import (stream_markup,
                                          telegram_markup)
from ArchMusic.utils.inline.playlist import close_markup
from ArchMusic.utils.pastebin import ArchMusicbin
from ArchMusic.utils.stream.queue import put_queue, put_queue_index



async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if video:
        if not await is_video_allowed(chat_id):
            raise AssistantErr(_["play_7"])
    if forceplay:
        await ArchMusic.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = f"{_['playlist_16']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    vidid,
                ) = await YouTube.details(
                    search, False if spotify else True
                )
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}- {title[:70]}\n"
                msg += f"{_['playlist_17']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(
                        vidid, mystic, video=status, videoid=True
                    )
                except:
                    raise AssistantErr(_["play_16"])
                await ArchMusic.join_call(
                    chat_id, original_chat_id, file_path, video=status
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                img = None
                button = stream_markup(_, vidid, chat_id)
                run = await app.send_message(
                original_chat_id,
                text=_["stream_1"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        else:
            link = await ArchMusicbin(msg)
            lines = msg.count("\n")
            if lines >= 17:
                car = os.linesep.join(msg.split(os.linesep)[:17])
            else:
                car = msg
            carbon = await Carbon.generate(
                car, randint(100, 10000000)
            )
            upl = close_markup(_)
            return await app.send_message(
                original_chat_id,
                text=_["playlist_18"].format(link, position),
                reply_markup=upl,
            )
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(
                vidid, mystic, videoid=True, video=status
            )
        except:
            raise AssistantErr(_["play_16"])
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            
            # Sıradaki parça için albüm kapağını al
            img = await YouTube.thumbnail(vidid, True)
            
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_["CLOSEMENU_BUTTON"], callback_data="close"
                    )
                ]
            ]
            
            await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["queue_4"].format(
                    position, title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id, original_chat_id, file_path, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await YouTube.thumbnail(vidid, True)
            button = stream_markup(_, vidid, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )
            position = len(db.get(chat_id)) - 1
            
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_["CLOSEMENU_BUTTON"], callback_data="close"
                    )
                ]
            ]
            
            await app.send_photo(
                original_chat_id,
                photo="assets/audio.png",
                caption=_["queue_4"].format(
                    position, title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id, original_chat_id, file_path, video=None
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
                forceplay=forceplay,
            )
            button = telegram_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo="assets/audio.png",
                caption=_["stream_3"].format(
                    title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_["CLOSEMENU_BUTTON"], callback_data="close"
                    )
                ]
            ]
            
            await app.send_photo(
                original_chat_id,
                photo="assets/telegram.png",
                caption=_["queue_4"].format(
                    position, title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id, original_chat_id, file_path, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)
            button = telegram_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo="assets/telegram.png",
                caption=_["stream_4"].format(
                    title, link, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = "Live Track"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            
            # Canlı yayın için albüm kapağını al
            img = await YouTube.thumbnail(vidid, True)
            
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_["CLOSEMENU_BUTTON"], callback_data="close"
                    )
                ]
            ]
            
            await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["queue_4"].format(
                    position, title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr(_["str_3"])
            await ArchMusic.join_call(
                chat_id, original_chat_id, file_path, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)
            img = await YouTube.thumbnail(vidid, True)
            button = telegram_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_5"].format(
                    title, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "URL stream"
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_["CLOSEMENU_BUTTON"], callback_data="close"
                    )
                ]
            ]
            
            await app.send_photo(
                original_chat_id,
                photo="assets/stream.png",
                caption=_["queue_4"].format(
                    position, title, duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id,
                original_chat_id,
                link,
                video=True if video else None,
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = telegram_markup(_, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo="assets/stream.png",
                caption=_["stream_2"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
                
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
