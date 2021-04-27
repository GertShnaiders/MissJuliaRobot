from julia import CMD_HELP
from bs4 import BeautifulSoup
import urllib
from julia import OWNER_ID
from julia import SUDO_USERS
from julia import tbot
import glob
import speedtest
from datetime import datetime
import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import re
from telegraph import upload_file
from telethon import events
from telethon.tl.types import MessageMediaPhoto
import cv2
import numpy as np
import PIL
from PIL import Image, ImageDraw
import pygments, os, asyncio, shutil, scapy, sys, requests, re, subprocess, urllib
from pygments.lexers import Python3Lexer
from pygments.formatters import ImageFormatter
import urllib.request
from faker import Faker as dc
import bs4
import html2text
from bing_image_downloader import downloader
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
import json
import urllib.request
from telegraph import Telegraph
import asyncio
import shutil
import argparse
import shlex
import subprocess
from typing import Tuple
from julia import *
from julia.Config import Config
from julia.events import register
import sys
from telethon import events
import asyncio
import traceback
import random
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
from telethon.errors.rpcerrorlist import YouBlockedUserError
fnt = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.change_info)

@register(pattern="^/meme")
async def _(event):

    if event.fwd_from:

        return

    f = await event.reply("Thinking... 🤔")

    await asyncio.sleep(2)

    x = random.randrange(1, 30)

    if x == 1:

        await f.edit(
            "[To your teachers on failing you in all your papers confidently, every time...](https://telegra.ph/file/431d178780f9bff353047.jpg)",
            link_preview=True,
        )

    if x == 2:

        await f.edit(
            "[A shift from the mainstream darling, sweetheart, jaanu, and what not...](https://telegra.ph/file/6bbb86a6c7d2c4a61e102.jpg)",
            link_preview=True,
        )

    if x == 3:

        await f.edit(
            "[To the guy who's friendzone-ing you...](https://telegra.ph/file/8930b05e9535e9b9b8229.jpg)",
            link_preview=True,
        )

    if x == 4:

        await f.edit(
            "[When your friend asks for his money back...](https://telegra.ph/file/2df575ab38df5ce9dbf5e.jpg)",
            link_preview=True,
        )

    if x == 5:

        await f.edit(
            "[A bad-ass reply to who do you think you are?](https://telegra.ph/file/3a35a0c37f4418da9f702.jpg)",
            link_preview=True,
        )

    if x == 6:

        await f.edit(
            "[When the traffic police stops your car and asks for documents...](https://telegra.ph/file/52612d58d6a61315a4c3a.jpg)",
            link_preview=True,
        )

    if x == 7:

        await f.edit(
            "[ When your friend asks about the food he/she just cooked and you don't want to break his/her heart...](https://telegra.ph/file/702df36088f5c26fef931.jpg)",
            link_preview=True,
        )

    if x == 8:

        await f.edit(
            "[When you're out of words...](https://telegra.ph/file/ba748a74bcab4a1135d2a.jpg)",
            link_preview=True,
        )

    if x == 9:

        await f.edit(
            "[When you realize your wallet is empty...](https://telegra.ph/file/a4508324b496d3d4580df.jpg)",
            link_preview=True,
        )

    if x == 10:

        await f.edit(
            "[When shit is about to happen...](https://telegra.ph/file/e15d9d64f9f25e8d05f19.jpg)",
            link_preview=True,
        )

    if x == 11:

        await f.edit(
            "[When that oversmart classmate shouts a wrong answer in class...](https://telegra.ph/file/1a225a2e4b7bfd7f7a809.jpg)",
            link_preview=True,
        )

    if x == 12:

        await f.edit(
            "[When things go wrong in a big fat Indian wedding...](https://telegra.ph/file/db69e17e85bb444caca32.jpg)",
            link_preview=True,
        )

    if x == 13:

        await f.edit(
            "[A perfect justification for breaking a promise...](https://telegra.ph/file/0b8fb8fb729d157844ac9.jpg)",
            link_preview=True,
        )

    if x == 14:

        await f.edit(
            "[When your friend just won't stop LOL-ing on something silly you said...](https://telegra.ph/file/247fa54106c32318797ae.jpg)",
            link_preview=True,
        )

    if x == 15:

        await f.edit(
            "[When someone makes a joke on you...](https://telegra.ph/file/2ee216651443524eaafcf.jpg)",
            link_preview=True,
        )

    if x == 16:

        await f.edit(
            "[When your professor insults you in front of the class...](https://telegra.ph/file/a2dc7317627e514a8e180.jpg)",
            link_preview=True,
        )

    if x == 17:

        await f.edit(
            "[When your job interviewer asks if you're nervous...](https://telegra.ph/file/9cc147d0bf8adbebf164b.jpg)",
            link_preview=True,
        )

    if x == 18:

        await f.edit(
            "[When you're sick of someone complaining about the heat outside...](https://telegra.ph/file/9248635263c52b968f968.jpg)",
            link_preview=True,
        )

    if x == 19:

        await f.edit(
            "[When your adda is occupied by outsiders...](https://telegra.ph/file/ef537007ba6d9d4cbd384.jpg)",
            link_preview=True,
        )

    if x == 20:

        await f.edit(
            "[When you don't have the right words to motivate somebody...](https://telegra.ph/file/2c932d769ae4c5fbed368.jpg)",
            link_preview=True,
        )

    if x == 21:

        await f.edit(
            "[When the bouncer won't let you and your group of friends in because you're all under-aged...](https://telegra.ph/file/6c8ca79f1e20ebd04391c.jpg)",
            link_preview=True,
        )

    if x == 22:

        await f.edit(
            "[To the friend who wants you to take the fall for his actions...](https://telegra.ph/file/d4171b9bc9104b5d972d9.jpg)",
            link_preview=True,
        )

    if x == 23:

        await f.edit(
            "[When that prick of a bully wouldn't take your words seriously...](https://telegra.ph/file/188d73bd24cf866d8d8d0.jpg)",
            link_preview=True,
        )

    if x == 24:

        await f.edit(
            "[ When you're forced to go shopping/watch a football match with your partner...](https://telegra.ph/file/6e129f138c99c1886cb2b.jpg)",
            link_preview=True,
        )

    if x == 25:

        await f.edit(
            "[To the large queue behind you after you get the last concert/movie ticket...](https://telegra.ph/file/2423f213dd4e4282a31ea.jpg)",
            link_preview=True,
        )

    if x == 26:

        await f.edit(
            "[When your parents thought you'd fail but you prove them wrong...](https://telegra.ph/file/39cc5098466f622bf21e3.jpg)",
            link_preview=True,
        )

    if x == 27:

        await f.edit(
            "[A justification for not voting!](https://telegra.ph/file/87d475a8f9a8350d2450e.jpg)",
            link_preview=True,
        )

    if x == 28:

        await f.edit(
            "[When your partner expects you to do too many things...](https://telegra.ph/file/68bc768d36e08862bf94e.jpg)",
            link_preview=True,
        )

    if x == 29:

        await f.edit(
            "[When your friends cancel on the plan you made at the last minute...](https://telegra.ph/file/960b58c8f625b17613307.jpg)",
            link_preview=True,
        )

    if x == 30:

        await f.edit(
            "[For that friend of yours who does not like loud music and head banging...](https://telegra.ph/file/acbce070d3c52b921b2bd.jpg)",
            link_preview=True,
        )
path = "./dcobra/"
if not os.path.isdir(path):
    os.makedirs(path)
client = tbot
@register(pattern="^/rgif")
async def _(event):
    if not event.reply_to_msg_id:
        await event.reply("Reply to any media.")
        return
    reply = await event.get_reply_message()
    download = await tbot.download_media(reply.media, path)
    img = cv2.VideoCapture(download)
    ret, frame = img.read()
    cv2.imwrite("danish.png", frame)
    danish = Image.open("danish.png")
    dark,python = danish.size
    cobra = f"""ffmpeg -f lavfi -i color=c=ffffff00:s={dark}x{python}:d=10 -loop 1 -i danish.png -filter_complex "[1]rotate=angle=PI*t:fillcolor=none:ow='hypot(iw,ih)':oh=ow[fg];[0][fg]overlay=x=(W-w)/2:y=(H-h)/2:shortest=1:format=auto,format=yuv420p" -movflags +faststart danish.mp4 -y"""                 
    m = await event.reply("```Processing ...```")
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cobra, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    await m.edit("```Uploading...```")
    await event.client.send_file(event.chat_id, "danish.mp4" , force_document=False, reply_to=event.reply_to_msg_id)
    await m.delete()
    shutil.rmtree(path)
    os.remove("danish.mp4")
    os.remove("danish.png")
from collections import deque
@register(pattern="^/momfck")
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2.0

    animation_ttl = range(0, 117)

    # input_str = event.pattern_match.group(1)

    # if input_str == "momfck":
    m = await event.reply("momfck")
    
    animation_chars = [
      "Inviting your mom for sex to my bedroom",
      "Your mom accepted.",
      "I open her saree , bra and panty",
      "fingering her pussy💦🖕🏼",
      "pressing her boobs",
      "Now she ready to be fuked",
      "Fucked.. 8%\nI open my pant's zip and ready to fuck your mom",
      "Fucked.. 20%\nAsking your mom to give me a blow job 👄👅",
      "Fucked... 25%\nNow my cock is ready for fucking your mom",
      "Fucked... 34%\nAhh!! Here this goes my to your mom's pussy...Very soft and tight💦💦",
            "Fucked... 48%\nUmm! almost there to cum inside you mom's pussy ",
            "Fucked... 56%\n Cummed inside your mom's pussy ",
            "Fucked... 64%\n Now your mom is pregnent because of my cum",
            "Fucked... 71%\n But your is not satisfied so she asked me to fuck her again",
            "Fucked... 87%\n So continue fucking her till cumming again🖕🏼🖕🏼🖕🏼🖕🏼🖕🏼🖕🏼",
            "Fucked... 93%\n Now your mom is satisfied and she started licking my cock🖕🏼🖕🏼",
            "Fucked... 100%\n█████████FUCKED!███████████ ",
            "FUCKED YOUR MOM HARD AS POSSIBLE, SHE IS NOW SATISFIED, AND YOU GOT NEW BROTHER`",
            ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await m.edit(animation_chars[i % 117])
client = tbot

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

async def fetch_audio(event, ws):
    if not event.reply_to_msg_id:
        await event.reply("Reply To A Video / Audio.")
        return
    what = await event.get_reply_message()    
    if what.audio is None  and what.video is None:
        await event.reply("Format Not Supported")
        return
    if what.video:
        await event.reply("Video Detected, Converting To Audio !")
        sed = await event.client.download_media(what.media)
        anie_cmd = f"ffmpeg -i {sed} -map 0:a anie.mp3"
        stdout, stderr = (await runcmd(anie_cmd))[:2]
        finale = "anie.mp3"
    elif what.audio:
        await event.reply("Download Started !")
        finale = await event.client.download_media(what.media)
    await event.reply("Almost Done!")    
    return finale

import string
from pathlib import Path
@register(pattern="^/shazam")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        ommhg = await event.reply("Reply To The Audio.")
        return
    if os.path.exists("anie.mp3"):
      os.remove("anie.mp3")
    credit = "By Anie"
    ommhg = await event.reply("`Downloading To Local Server.`")
    kkk = await fetch_audio(event, tbot)
    downloaded_file_name = kkk
    train = credit[3].lower()
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    Lop = "flutter's formula"
    loP = Lop[1]
    await ommhg.edit("**Searching For This Song In Anie's DataBase.**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files = f)
    if train == loP:
       await ommhg.edit("Server Has Been Crashed for Unknown Reasons")
    try:
      xo = r.json()
    except:
      return
    try:
      xo = r.json()
      xoo = xo.get("response")
      zz = xoo[1]
      zzz = zz.get("track")
      Col = zzz.get("sections")[3]
      nt = zzz.get("images")	
      image = nt.get("coverarthq")
      by = zzz.get("subtitle")
      title = zzz.get("title")
      message = f"""<b>Song Shazamed.</b>
<b>Song Name : </b>{title}
<b>Song By : </b>{by}

<u><b>Identified By Anie.</b></u> @RoseLoverX.
"""
      await event.delete()
      await tbot.send_message(
        event.chat_id,
        message,
        parse_mode="HTML",
        file=image,
        force_document=False,
        silent=True,
      )
      os.remove(downloaded_file_name)
    except:
      if xo.get("success") is False:
        errer = xo.get("error")
        ommhg = await event.reply(errer)
        os.remove(downloaded_file_name)
        return
      await ommhg.reply("Song Not Found IN Database. Please Try Again.")
      os.remove(downloaded_file_name)
      return
@register(pattern="^/upload (.*)")
async def upload_file(message):
    input_str = message.get_args()
    if not os.path.exists(input_str):
        await message.reply("File not found!")
        return
    await message.reply("Processing ...")
    caption_rts = os.path.basename(input_str)
    with open(input_str, 'rb') as f:
        await tbot.send_file(
            message.chat.id,
            f,
            caption=caption_rts,
            force_document=False,
            allow_cache=False,
            reply_to=message.message_id
        )
DANISH = "58199388-5499-4c98-b052-c679b16310f9"
from telethon.tl.types import MessageMediaPhoto
import os, urllib, requests, asyncio
@register(pattern="^/co")
async def _(event):
          
    reply = await event.get_reply_message()
    if not reply:#By @Danish_00
#Fixed By a NOOB
        return await event.reply(
           "Reply to any image or non animated sticker !"
        )
    devent = await event.reply("Downloading the file to check...")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await event.reply(
             "Reply to any image or non animated sticker !"
        )#By @Danish_00
#Fixed By a NOOB
    await devent.edit("coloring image sar...")
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": DANISH},
    )#By @Danish_00
#Fixed By a NOOB
    os.remove(media)
    if "status" in r.json():
        return await devent.edit( r.json()["status"])
    r_json = r.json()["output_url"]
    pic_id = r.json()["id"]
    
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    result = f"{r_json}"
    
    await devent.delete()
    await tbot.send_message(
        event.chat_id,
        file=result
    )

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /meme: Get Random memes
 - /rgif: Reply To a Gif To Rotate It
 - /momfck: Uff
 - /shazam: Reply To an Audio Or Video To Identify The Song
 - /Upload: Sudo Restericted Uploads A file from Bot Dir
 - /co: Colours An image Via DeepAi
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
