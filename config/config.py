import re

import sys

from os import getenv

from dotenv import load_dotenv

from pyrogram import filters

load_dotenv()

# Get it from my.telegram.org

API_ID = int(getenv("API_ID", "4290257"))

API_HASH = getenv("API_HASH", "4f1f9a2b8f811b7d5593af8a1b8f8fb7")

## Get it from @Botfather in Telegram.

BOT_TOKEN = getenv("BOT_TOKEN", "7850456492:AAEoynWlvFIMU-Hq01aG-nlx6ikSNjXnPW4")

# Database to save your chats and stats.

MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://gamerzone47:hepitosgamer47@gamerzone.0df9rbt.mongodb.net/?retryWrites=true&w=majority&appName=Gamerzone")

# Custom max audio(music) duration for voice chat. set DURATION_LIMIT in variables with your own time(mins), Default to 60 mins.

DURATION_LIMIT_MIN = int(

    getenv("DURATION_LIMIT", "760")

)  # Remember to give value in Minutes

# Duration Limit for downloading Songs in MP3 or MP4 format from bot

SONG_DOWNLOAD_DURATION = int(

    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "360")

)  # Remember to give value in Minutes

# You'll need a Private Group ID for this.

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002522096977"))

# A name for your Music bot.

MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME","GameZoneBot")

# Your User ID.

OWNER_ID = list(

    map(int, getenv("OWNER_ID", "8183419163").split())

)  # Input type must be interger

# Get it from http://dashboard.heroku.com/account

HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

# You have to Enter the app name which you gave to identify your  Music Bot in Heroku.

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)

# For customized or modified Repository

UPSTREAM_REPO = getenv(

    "UPSTREAM_REPO",

    "https://github.com/Hellowen334/ejderhamusic",

)

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

# GIT TOKEN ( if your edited repo is private)

GIT_TOKEN = getenv("GIT_TOKEN", None)

# Only  Links formats are  accepted for this Var value.

SUPPORT_CHANNEL = getenv(

    "SUPPORT_CHANNEL", "https://t.me/ejderhamusicduyuru") 
    
SUPPORT_GROUP = getenv(

    "SUPPORT_GROUP", "https://t.me/Gamerzonesohbet")  

# Set it in True if you want to leave your assistant after a certain amount of time. [Set time via AUTO_LEAVE_ASSISTANT_TIME]

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "false")

# Time after which you're assistant account will leave chats automatically.

AUTO_LEAVE_ASSISTANT_TIME = int(

    getenv("ASSISTANT_LEAVE_TIME", "5400")

)  # Remember to give value in Seconds

# Time after which bot will suggest random chats about bot commands.

AUTO_SUGGESTION_TIME = int(

    getenv("AUTO_SUGGESTION_TIME", "5400")

)  # Remember to give value in Seconds

# Set it True if you want to delete downloads after the music playout ends from your downloads folder

AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", None)

# Set it True if you want to bot to suggest about bot commands to random chats of your bots.

AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", None)

# Set it true if you want your bot to be private only [You'll need to allow CHAT_ID via /authorise command then only your bot will play music in that chat.]

PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

# Time sleep duration For Youtube Downloader

YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "3"))

# Time sleep duration For Telegram Downloader

TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", "5"))

# Your Github Repo.. Will be shown on /start Command

GITHUB_REPO = getenv("GITHUB_REPO", "https://github.com/Hellowen334/ejderhamusic") 

# Spotify Client.. Get it from https://developer.spotify.com/dashboard

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "2041df9cbcd142cba804578a2cf85939")

SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "80ffd296320e49299830e80b11e3bf73")

# Maximum number of video calls allowed on bot. You can later set it via /set_video_limit on telegram

VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "10"))

# Maximum Limit Allowed for users to save playlists on bot's server

SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "100"))

# MaximuM limit for fetching playlist's track from youtube, spotify, apple links.

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "50"))

# Cleanmode time after which bot will delete its old messages from chats

CLEANMODE_DELETE_MINS = int(

    getenv("CLEANMODE_MINS", "600")

)  # Remember to give value in Seconds

# Telegram audio  and video file size limit

TG_AUDIO_FILESIZE_LIMIT = int(

    getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600")

)  # Remember to give value in bytes

TG_VIDEO_FILESIZE_LIMIT = int(

    getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824")

)  # Remember to give value in bytes

# Chceckout https://www.gbmb.org/mb-to-bytes  for converting mb to bytes

# If you want your bot to setup the commands automatically in the bot's menu set it to true.

# Refer to https://i.postimg.cc/Bbg3LQTG/image.png

SET_CMDS = getenv("SET_CMDS", False)

# You'll need a Pyrogram String Session for these vars. Generate String from our session generator bot @YukkiStringBot

STRING1 = getenv("STRING_SESSION", "BAE6wAMAhYoEKH06cNH4r9U6RhrPSEQiA19H4UPgZF0vPwgedFY8PbqFg0PM9Gvy4vRTltB8VCWyBWAdUgJkieO8YFmqzZLCjDndKs9F1tE2hhKETis0lwOkncNfVy7OGtNO7UxRZtj67EGT8TUoK4O4hJj_CZtSYLxQbOJZyHWpswOLjKltw6PlIIbsCGM2rWQwgRMzT8IxgpBSJnCX-Sj76ZKJqWSsbmIsFxx1iH573IzYc80j2thvzta8BOwSN2xCPdw0L-zTru8OzjqXKUF0E87orGAXz7RqfaPmDAAJnjipX2HAEqCa4BqSBQwgQyrzoNhDztvbjJVo7Gc78hLppX-MxgAAAAHbTXvLAA")

STRING2 = getenv("STRING_SESSION2", None)

STRING3 = getenv("STRING_SESSION3", None)

STRING4 = getenv("STRING_SESSION4", None)

STRING5 = getenv("STRING_SESSION5", None)

### DONT TOUCH or EDIT codes after this line

BANNED_USERS = filters.user()

YTDOWNLOADER = 1

LOG = 2

LOG_FILE_NAME = "ArchMusiclogs.txt"

adminlist = {}

lyrical = {}

chatstats = {}

userstats = {}

clean = {}

votemode = {}

confirmer = {}

autoclean = []

# Images

START_IMG_URL = getenv(
     "START_IMG_URL", 
     "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",
     

)

PING_IMG_URL = getenv(

    "PING_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

PLAYLIST_IMG_URL = getenv(

    "PLAYLIST_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

GLOBAL_IMG_URL = getenv(

    "GLOBAL_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

STATS_IMG_URL = getenv(

    "STATS_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

TELEGRAM_AUDIO_URL = getenv(

    "TELEGRAM_AUDIO_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

TELEGRAM_VIDEO_URL = getenv(

    "TELEGRAM_VIDEO_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

STREAM_IMG_URL = getenv(

    "STREAM_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

SOUNCLOUD_IMG_URL = getenv(

    "SOUNCLOUD_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

YOUTUBE_IMG_URL = getenv(

    "YOUTUBE_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

SPOTIFY_ARTIST_IMG_URL = getenv(

    "SPOTIFY_ARTIST_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

SPOTIFY_ALBUM_IMG_URL = getenv(

    "SPOTIFY_ALBUM_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

SPOTIFY_PLAYLIST_IMG_URL = getenv(

    "SPOTIFY_PLAYLIST_IMG_URL",

    "https://pbs.twimg.com/media/GqbPKSwWEAAfGgj?format=jpg&name=small",

)

def time_to_seconds(time):

    stringt = str(time)

    return sum(

        int(x) * 60**i

        for i, x in enumerate(reversed(stringt.split(":")))

    )

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

SONG_DOWNLOAD_DURATION_LIMIT = int(

    time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00")

)

if SUPPORT_CHANNEL:

    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):

        print(

            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"

        )

        sys.exit()

if SUPPORT_GROUP:

    if not re.match("(?:http|https)://", SUPPORT_GROUP):

        print(

            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"

        )

        sys.exit()

if UPSTREAM_REPO:

    if not re.match("(?:http|https)://", UPSTREAM_REPO):

        print(

            "[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://"

        )

        sys.exit()

if GITHUB_REPO:

    if not re.match("(?:http|https)://", GITHUB_REPO):

        print(

            "[ERROR] - Your GITHUB_REPO url is wrong. Please ensure that it starts with https://"

        )

        sys.exit()

if PING_IMG_URL:

    if PING_IMG_URL != "assets/Ping.jpeg":

        if not re.match("(?:http|https)://", PING_IMG_URL):

            print(

                "[ERROR] - Your PING_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if PLAYLIST_IMG_URL:

    if PLAYLIST_IMG_URL != "assets/Playlist.jpeg":

        if not re.match("(?:http|https)://", PLAYLIST_IMG_URL):

            print(

                "[ERROR] - Your PLAYLIST_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if GLOBAL_IMG_URL:

    if GLOBAL_IMG_URL != "assets/Global.jpeg":

        if not re.match("(?:http|https)://", GLOBAL_IMG_URL):

            print(

                "[ERROR] - Your GLOBAL_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if STATS_IMG_URL:

    if STATS_IMG_URL != "assets/Stats.jpeg":

        if not re.match("(?:http|https)://", STATS_IMG_URL):

            print(

                "[ERROR] - Your STATS_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if TELEGRAM_AUDIO_URL:

    if TELEGRAM_AUDIO_URL != "assets/Audio.jpeg":

        if not re.match("(?:http|https)://", TELEGRAM_AUDIO_URL):

            print(

                "[ERROR] - Your TELEGRAM_AUDIO_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if STREAM_IMG_URL:

    if STREAM_IMG_URL != "assets/Stream.jpeg":

        if not re.match("(?:http|https)://", STREAM_IMG_URL):

            print(

                "[ERROR] - Your STREAM_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if SOUNCLOUD_IMG_URL:

    if SOUNCLOUD_IMG_URL != "assets/Soundcloud.jpeg":

        if not re.match("(?:http|https)://", SOUNCLOUD_IMG_URL):

            print(

                "[ERROR] - Your SOUNCLOUD_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if YOUTUBE_IMG_URL:

    if YOUTUBE_IMG_URL != "assets/Youtube.jpeg":

        if not re.match("(?:http|https)://", YOUTUBE_IMG_URL):

            print(

                "[ERROR] - Your YOUTUBE_IMG_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if TELEGRAM_VIDEO_URL:

    if TELEGRAM_VIDEO_URL != "assets/Video.jpeg":

        if not re.match("(?:http|https)://", TELEGRAM_VIDEO_URL):

            print(

                "[ERROR] - Your TELEGRAM_VIDEO_URL url is wrong. Please ensure that it starts with https://"

            )

            sys.exit()

if not MUSIC_BOT_NAME.isascii():

    print(

        "[ERROR] - You've defined MUSIC_BOT_NAME wrong. Please don't use any special characters or Special font for this... Keep it simple and small."

    )

    sys.exit()
