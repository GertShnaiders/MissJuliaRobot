#made by RoseLoverX Jo Kang Kiya Wo Mera beta Ho
from random import uniform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import asyncio
import random
import re
import string
from julia.events import register
import json
import subprocess
import textwrap
import urllib.request
from random import randrange
from typing import List
from typing import Optional
from julia import OWNER_ID
from julia import SUDO_USERS
from fontTools.ttLib import TTFont
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from julia import *
from julia.Config import Config
import traceback
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
import os
from datetime import datetime
import requests
import io
import sys
import traceback

@register(pattern="^/exec (.*)")
async def msg(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("This is an owner restricted command. You do not have permissions to run this.")
        return
    else:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    await event.reply(f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
)
