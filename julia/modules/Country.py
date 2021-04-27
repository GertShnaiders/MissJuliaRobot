
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
from countryinfo import CountryInfo
import flag
import html
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve

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

@register(pattern="^/country (.*)")
async def msg(event):
    if event.fwd_from:
        return
    start = datetime.now()
    try:
        input_str = event.pattern_match.group(1)
        lol = input_str
        country = CountryInfo(lol)
        a = country.info()
    except:
     await event.reply("Country Not Avaiable Currently")
    name = a.get("name")
    bb= a.get("altSpellings")
    hu = ''
    for p in bb:
     hu += p+",  "
    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
     borders += fk+",  "
 
    call = "" 
    WhAt = a.get("callingCodes")
    for what in WhAt:
     call+= what+"  "
 
    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
     currencies += FKer+",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR= PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
      po = iSo.get(hitler)
      iso += po+",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag.flag(nox)

    languages = a.get("languages")
    lMAO=""
    for lmao in languages:
     lMAO += lmao+",  "

    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom =""
    for jerry in tik:
     tom+=jerry+",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
     lanester+=targaryen+",   "

    wiki = a.get("wiki")
    caption = f"""<b><u>information gathered successfully</b></u>
<b>
Country Name:- {name}
Alternative Spellings:- {hu}
Country Area:- {area} square kilometers
Borders:- {borders}
Calling Codes:- {call}
Country's Capital:- {capital}
Country's currency:- {currencies}
Country's Flag:- {okie}
Demonym:- {HmM}
Country Type:- {EsCoBaR}
ISO Names:- {iso}
Languages:- {lMAO}
Native Name:- {nonive}
population:- {waste}
Region:- {reg}
Sub Region:- {sub}
Time Zones:- {tom}
Top Level Domain:- {lanester}
"""
    await tbot.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )
    
    await event.delete()
import logging
import asyncio
from telethon import TelegramClient, events
@register(pattern="^/frwd")
async def frwder(event):
    if event.is_private:
        await event.reply("I work in groups!")
        return
    ok = await tbot(GetFullUserRequest(event.sender_id))
    txt = event.text.split(" ", maxsplit=2)
    try:
        chat = txt[1]
        msg = txt[2]
        if msg is None:
            await event.reply("No message provided!\n\nFormat - `/frwd <chat id/username> <message/reply to message>`")
            return
        if chat.startswith('@'):
            try:
                temp = await tbot.get_entity(chat)
                chat = temp.id
            except UsernameNotOccupiedError as e:
                await event.reply(str(e))
                return
        try:
            sent = await tbot.send_message(chat, msg)
            await sent.reply(f"Message from [{ok.user.first_name}](tg://user?id={event.sender_id})")
            temp = await event.reply("Done!")
            await asyncio.sleep(10)
            #await event.delete()
            await temp.delete()
        except Exception as e:
            await event.reply(f"Bot not in the group 🤔\n\n{str(e)}")
    except UsernameNotOccupiedError as e:
        await event.reply(str(e))
        return
    except Exception as e:
        await event.reply(f"Format - `/frwd <chat id/username> <message/reply to message>`\n\n{str(e)}")
        return
    
    
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /country: Enter a Country Name To get its Details.
 - /frwd: Forward a message From One Group To Another
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
