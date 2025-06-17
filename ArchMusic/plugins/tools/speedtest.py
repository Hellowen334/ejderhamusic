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
import speedtest
from pyrogram import filters
from strings import get_command
from ArchMusic import app
from ArchMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("İndirme Hızı Test Ediliyor")
        test.download()
        m = m.edit("Yükleme Hızı Test Ediliyor")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("Hız Testi Sonuçları Paylaşılıyor")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Running Speed test")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Hız Testi Sonuçları**
    
<u>**Müşteri:**</u>
**İnternet Servis Sağlayıcısı:** {result['client']['isp']}
**Ülke:** {result['client']['country']}
  
<u>**Sunucu:**</u>
**İsim:** {result['server']['name']}
**Ülke:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Gecikme:** {result['server']['latency']}  
**Ping:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
