#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.



HELP_3 = """
**ADMİN KOMUTLARI:**

**/c** komutlarını kanalda kullanabilmek için, komutların başına **c** ekleyin.

**/pause veya /dur**: Çalan akışı duraklatır.
**/resume veya /devam**: Duraklatılmış akışı devam ettirir.
**/skip veya /atla **: Çalan akışı atlar ve sıradaki parçayı çalmaya başlar.
**/kapat** veya **/son**: Sıradaki parçayı atlar ve çalan akışı sonlandırır.
**/player**: Etkileşimli bir oynatıcı paneli alır.
**/queue veya /liste**: Sıradaki parçaların listesini gösterir.
"""
HELP_4 = """
**YETKİLİ KULLANICILAR:**

**/auth veya /ver  [kullanıcı adı/kullanıcı_ID]**: Bir kullanıcıyı botun yetkili listesine ekler.
**/unauth veya /al [kullanıcı adı/kullanıcı_ID]**: Bir kullanıcıyı yetkili kullanıcılar listesinden çıkarır.
**/authusers veya /yetkili**: Yetkili kullanıcıların listesini gösterir.
"""
HELP_5 = """
**BAKIM MODU:** [Sadece süper yöneticiler için]

/logs : Botun aktivitelerinin günlüklerini alır. 📔

/logger [enable/disable] : Botun aktivitelerini günlüklemeye başlar/devre dışı bırakır.📝

/bakım [enable/disable] : Botun bakım modunu etkinleştirir/devre dışı bırakır. ⚙️

**SUDO KULLANICISI EKLE**

/addsudo : Kullanıcı ekler.
/delsudo : Kullanıcı siler.
/sudolist : Kullanıcı listesi

**AKTIF SES KONTROL**

/aktifses : Aktif ses kontrol
/aktifvideo : Aktif video kontrol


"""
HELP_6 = """
**CHAT BLACKLIST ÖZELLİĞİ:** [Sadece süper yöneticiler için]

Çöp sohbetlerinizi botumuzda kullanmayı kısıtlayın.

/blacklistchat [sohbet ID] : Bir sohbeti bot kullanımından engeller.
/whitelistchat [sohbet ID] : Kara listeye alınmış sohbeti beyaz listeye alır.
/blacklistedchat : Kara listeye alınmış sohbetlerin listesini gösterir.
"""
HELP_7 = """
**KULLANICI ENGELLEME:**

Kara listeye alınmış kullanıcıları görmezden gelmeye başlar, böylece bot komutlarını kullanamazlar.

/block [kullanıcı adı veya kullanıcıya yanıt] : Kullanıcıyı botumuzdan engeller.
/unblock [kullanıcı adı veya kullanıcıya yanıt] : Engellenmiş kullanıcının engelini kaldırır.
/blockedusers : Engellenmiş kullanıcıların listesini gösterir.
"""
HELP_8 = """
**KANAL OYNATMA KOMUTLARI:**

Kanallarda ses/video yayını yapabilirsiniz.

/cplay : Kanalın video sohbetinde istenilen ses parçasının yayınını başlatır.
/cvoynat : Kanalın video sohbetinde istenilen video parçasının yayınını başlatır.
/cplayforce veya /cvplayforce : Devam eden yayını durdurur ve istenilen parçanın yayınını başlatır.
/channelplay [sohbet kullanıcı adı veya ID] veya [devre dışı] : Kanalı bir gruba bağlar ve grup tarafından gönderilen komutlarla parçaların yayınını başlatır.
"""

HELP_9 = """
**GLOBAL BAN ÖZELLİĞİ:** [Sadece süper yöneticiler için]

/gban [kullanıcı adı veya kullanıcıya yanıt] : Tüüm sunucu sohbetlerinden kullanıcıyı global olarak engeller ve bot kullanımını ondan engeller.
/ungban [kullanıcı adı veya kullanıcıya yanıt] : Global olarak yasaklanan kullanıcının yasağını kaldırır.
/gbannedusers : Global olarak yasaklanan kullanıcıların listesini gösterir.
"""
HELP_10 = """
**LOOP STREAM:**

Ongoing yayını döngüde başlatır.

/dongu [enable/disable] : Ongoing yayın için döngüyü etkinleştirir/devre dışı bırakır.
/dongu [1, 2, 3, ...] : Verilen değer için döngüyü etkinleştirir.
"""
HELP_11 = """
**YAYIN YAPMA ÖZELLİĞİ**

**/broadcast [mesaj veya bir mesaja yanıt]**: Bir mesajı sunucu sohbetlerine yayınlar.

Yayın modları:
**-pin**: Yayınlanan mesajları sunucu sohbetlerinde sabitler.
**-pinloud**: Yayınlanan mesajları sunucu sohbetlerinde sabitler ve üyelere bildirim gönderir.
**-user**: Mesajı botunuza başlatan kullanıcılara yayınlar.
**-assistant**: Botunuzun asistan hesabından mesajı yayınlar.
**-nobot**: Mesajın yayınlanmasını engeller.

Örnek: /broadcast -user -assistant -pin Test yayını
"""
HELP_12 = """
**PING & STATS:**

/ping : Botun ping ve sistem istatistiklerini gösterir.

/stats : Botun genel istatistiklerini gösterir.
"""
HELP_13 = """
**PLAY COMMANDS:**

**v :** Video play için kullanılır.
**force :** Zorla oynatma için kullanılır.

/play , /voynat veya /oynat veya /voynat : Video sohbetinde istenilen parçayı çalmaya başlar.

/playforce veya /voynatforce : Devam eden yayını durdurur ve istenilen parçayı çalmaya başlar.

/playlist : Oynatma listenizi gösterir.
/listemisil : Oynatma listenizi siler.
"""
HELP_14 = """
**SHUFFLE QUEUE:**

/karistir : Sıradaki parçaları karıştırır.
/queue : Karıştırılmış sırayı gösterir.
"""

HELP_15 = """
**SEEK STREAM:**

/ilerisar [saniye cinsinden süre] : Yayını belirtilen süreye atlar.
/gerisar [saniye cinsinden süre] : Yayını belirtilen süre kadar geri alır.
"""
HELP_16 = """
**SONG DOWNLOAD:**

/song veya /bul [şarkı adı/YouTube URL] : YouTube'dan herhangi bir parçayı MP3 veya MP4 formatında indirir.
"""
HELP_17 = """
**SPEED COMMANDS:**

Ongoing stream'un çalma hızını kontrol edebilirsiniz. [Yalnızca yöneticiler]

/speed veya /playback : Grubun ses çalma hızını ayarlamak için.
/cspeed veya /cplayback : Kanalın ses çalma hızını ayarlamak için.
"""
