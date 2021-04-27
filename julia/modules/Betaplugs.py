from julia import CMD_HELP
from bs4 import BeautifulSoup
import urllib
from julia import OWNER_ID
from julia import SUDO_USERS
from julia import tbot
import glob
import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import re
import urllib.request
from faker import Faker	
from faker.providers import internet	
import bs4
import html2text
import requests
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
import shlex
from typing import Tuple
from julia import *
from julia.Config import Config
from julia.events import register
import sys
from telethon import events
import asyncio
import traceback
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
edit_time = 1
@register(pattern="^/iplookup (.*)")
async def _(event):
    if event.is_group:
        pass
    else:
        return
    input_str = event.pattern_match.group(1)

    adress = input_str

    token = "19e7f2b6fe27deb566140aae134dec6b"

    api = "http://api.ipstack.com/" + adress + "?access_key=" + token + "&format=1"

    result = urllib.request.urlopen(api).read()
    result = result.decode()

    result = json.loads(result)
    a = result["type"]
    b = result["country_code"]
    c = result["region_name"]
    d = result["city"]
    e = result["zip"]
    f = result["latitude"]
    g = result["longitude"]
    await event.reply(
        f"<b><u>INFORMATION GATHERED SUCCESSFULLY</b></u>\n<b>IP:-</b><code>{input_str}</code>\n\n<b>Ip type :-</b><code>{a}</code>\n<b>Country code:- </b> <code>{b}</code>\n<b>State name :-</b><code>{c}</code>\n<b>City name :- </b><code>{d}</code>\n<b>zip :-</b><code>{e}</code>\n<b>Latitude:- </b> <code>{f}</code>\n<b>Longitude :- </b><code>{g}</code>\n",
        parse_mode="HTML",
    )
    
@register(pattern="^/memify (.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Usage:- memify upper text ; lower text")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("Reply to a image/sticker.")
        return
    file = await tbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
    a = await event.reply("Memifying this image! (」ﾟﾛﾟ)｣ ")
    text = str(event.pattern_match.group(1)).strip()
    if len(text) < 1:
        return await a.reply("Usage:- memify upper text ; lower text")
    meme = await drawText(file, text)
    await event.client.send_file(event.chat_id, file=meme, force_document=False)
    os.remove(meme)
    await event.delete()
    await a.delete()

async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-Bold.ttf"
    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    image_name = "memify.webp"
    webp_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, image_name)
    img.save(webp_file, "webp")
    return webp_file

@register(pattern="^/echo (.*)")
async def _(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    else:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    await event.reply(f"{input_str}")
    await event.delete()

@register(pattern="^/ftoimg")
async def on_file_to_photo(event):
    await event.reply("processing.....")
    await asyncio.sleep(2)
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  # This isn't an image
    if image.mime_type == 'image/webp':
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise

    file = await tbot.download_media(target, file=BytesIO())
    file.seek(0)
    img = await tbot.upload_file(file)
    img.name = 'image.png'

    try:
        await tbot(SendMediaRequest(
            peer=await event.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return

@register(pattern="^/bin (.*)")
async def _(event):
    if event.fwd_from:
        return
    try:
        tfsir = await event.reply("Wait Fetching Bin Info")
        kek = event.pattern_match.group(1)
        url = f"https://lookup.binlist.net/{kek}"
        midhunkm = requests.get(url=url).json()
        kekvro = midhunkm["country"]
        data_is = (
            f"<b><u>Bin</u></b> ➠ <code>{kek}</code> \n"
            f"<b><u>Type</u></b> ➠ <code>{midhunkm['type']}</code> \n"
            f"<b><u>Scheme</u></b> ➠ <code>{midhunkm['scheme']}</code> \n"
            f"<b><u>Brand</u></b> ➠ <code>{midhunkm['brand']}</code> \n"
            f"<b><u>Country</u></b> ➠ <code>{kekvro['name']} {kekvro['emoji']}</code> \n"
        )
        await tfsir.edit(data_is, parse_mode="HTML")
    except:
        await tfsir.edit("Not a Valid Bin Or Don't Have Enough Info.")


@register(pattern="^/rmeme")
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    hmm_s = 'https://some-random-api.ml/meme'
    r = requests.get(url=hmm_s).json()
    image_s = r['image']
    await tbot.send_file(event.chat_id, file=image_s, caption=r['caption'])
    
@register(pattern="^/fake")
async def hi(event):	
    if event.fwd_from:	
        return	
    fake = Faker()	
    print("FAKE DETAILS GENERATED\n")	
    name = str(fake.name())	
    fake.add_provider(internet)	
    address = str(fake.address())	
    ip = fake.ipv4_private()	
    cc = fake.credit_card_full()	
    email = fake.ascii_free_email()	
    job = fake.job()	
    android = fake.android_platform_token()	
    pc = fake.chrome()	
    h = await event.reply("Getting Fake Info...")
    await asyncio.sleep(3)
    await h.edit(	
        f"<b><u> Fake Information Generated</b></u>\n<b>Name :-</b><code>{name}</code>\n<b>Address:-</b><code>{address}</code>\n<b>IP ADDRESS:-</b><code>{ip}</code>\n<b>credit card:-</b><code>{cc}</code>\n<b>Email Id:-</b><code>{email}</code>\n<b>Job:-</b><code>{job}</code>\n<b>android user agent:-</b><code>{android}</code>\n<b>Pc user agent:-</b><code>{pc}</code>",	
        parse_mode="HTML",	
    )

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /iplookup: Get INfo About an ipadress
 - /memify: Memifies A Sticker Or a Pic
 - /echo: Sudo Res. U k The Use??.
 - /ftoimg: Converts Image In FIle Format TO Noral Pic
 - /bin: Gathers Details ABout The Given BIn
 - /rmeme: Send Random Memes
 - /fake: Generates Fake Info
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
