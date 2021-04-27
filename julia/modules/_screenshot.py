from random import randint
#made by RoseLoverX Jo Kang Kiya Wo Mera beta Ho
from PIL import ImageEnhance, ImageOps
from random import uniform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import asyncio
import io
import os
import random
import re
import string
import nltk
from PIL import Image
from zalgo_text import zalgo
from julia.events import register
import json
import subprocess
import textwrap
import urllib.request
from random import randrange
from typing import List
from typing import Optional
import emoji
from cowpy import cow
from fontTools.ttLib import TTFont
from PIL import ImageDraw
from PIL import ImageFont
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from julia import *
from julia.Config import Config
import traceback
from datetime import datetime
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None

@register(pattern="^/sshot (.*)")
async def msg(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    else:
        return
        await event.reply("Painting web-page..")
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location=GOOGLE_CHROME_BIN
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        imp = "anie"
        driver.get(input_str)
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        driver.close()
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        with io.BytesIO(im_png) as out_file:
            out_file.name = "Anie.sshot.PNG"
            await tbot.send_file(
                event.chat_id,
                out_file,
                caption=imp,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"Done in {ms} seconds")
    except Exception:
        await event.edit(traceback.format_exc())

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /sshot: Get Screenshot Of a Website
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
