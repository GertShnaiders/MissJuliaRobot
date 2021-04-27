from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import tbot
from julia import OWNER_ID, SUDO_USERS
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
import random
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pytz 
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from telegraph import upload_file
import time
import html
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
sedpath = "./starkgangz/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)
@register(pattern="^/(logo|blacklogo) ?(.*)")
async def yufytf(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/Blankmeisnub.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/Streamster.ttf', 220)
    image_widthz, image_heightz = img.size
    w,h = draw.textsize(text, font=font)
    h += int(h*0.21)
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 218, 135))
    file_name = "LogoBy@MeisNub.png"
    await event.delete()
    ok = sedpath + "/" + file_name
    img.save(ok, "PNG")
    await borg.send_file(event.chat_id, ok, caption="Made By Anie")
    if os.path.exists(ok):
        os.remove(ok)
@register(pattern="^/(slogo|starlogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/20201125_094030.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 380)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="yellow", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(blogo|betalogo) ?(.*)")
async def slogo(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Who Are You?")
        return
    else:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_104759_504.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 69)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="red", stroke_width=9, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(hlogo|heppylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/images (1).jpeg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 70)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="green", stroke_width=7, stroke_fill="blue")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(clogo|cyberlogo) ?(.*)")
async def slogo(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Who Are You?")
        return
    else:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_114503_069.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 89)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)-200), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2-200)
    draw.text((x, y), text, font=font, fill="orange", stroke_width=10, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await event.delete()
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(llogo|bonked) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_175652_655.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 90)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=8, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await event.delete()
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(bonk|nalogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210210_170521_219.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 90)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=8, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(klogo|skayogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_170415_437.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 200)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)-200), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2-200)
    draw.text((x, y), text, font=font, fill="white", stroke_width=8, stroke_fill="blue")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(jlogo|stardbogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/images.jpeg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 70)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="deepgreen", stroke_width=3, stroke_fill=(57, 255, 20))
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(xlogo|starsblogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.edit("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210215_223905_847.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 70)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="white", stroke_width=30, stroke_fill="black")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(oklogo|starhdalogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210216_101425_014.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 59)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill=(0,0,0,20), stroke_width=2, stroke_fill="white")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(vlogo|girlylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210216_105824_309.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 90)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)+200), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+200)
    draw.text((x, y), text, font=font, fill="orange", stroke_width=5, stroke_fill="yellow")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(dlogo|darxylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/IMG_20210216_111419_829.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Vermin Vibes V.otf", 110)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)+350), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+350)
    draw.text((x, y), text, font=font, fill="cyan", stroke_width=11, stroke_fill="lightgreen")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)
@register(pattern="^/(mlogo|multilogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    quew = event.pattern_match.group(2)
    if "|" in quew:
        iid, reasonn = quew.split("|")
    text = iid.strip()
    tt = reasonn.strip()
    await event.reply("`Processing..`")
    img = Image.open('./resources/Blankmeisnub.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Road_Rage.otf", 210)
    fuk = ImageFont.truetype("./resources/Road_Rage.otf", 90)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)-16), text, font=font, fill=(255, 255, 255))
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)-16), text, font=font, fill="red", stroke_width=4, stroke_fill="blue")
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="grey", stroke_width=6, stroke_fill="lightgreen")
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)+360), tt, font=fuk, fill=(255, 255, 255))
    draw.text(((image_widthz-w)/2, ((image_heightz-h)/2)+360), tt, font=fuk, fill="green", stroke_width=5, stroke_fill="yellow")
    draw.text((((image_widthz-w)/2)+500, ((image_heightz-h)/2)+360), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+500, ((image_heightz-h)/2)+360), tt, font=fuk, fill="pink", stroke_width=5, stroke_fill="red")
    draw.text((((image_widthz-w)/2)+150, ((image_heightz-h)/2)-450), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+150, ((image_heightz-h)/2)-450), tt, font=fuk, fill="green", stroke_width=5, stroke_fill="yellow")
    draw.text((((image_widthz-w)/2)+600, ((image_heightz-h)/2)-453), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+600, ((image_heightz-h)/2)-453), tt, font=fuk, fill="blue", stroke_width=5, stroke_fill="violet")
    draw.text((((image_widthz-w)/2)+590, ((image_heightz-h)/2)+500), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+590, ((image_heightz-h)/2)+500), tt, font=fuk, fill="grey", stroke_width=5, stroke_fill="white")
    draw.text((((image_widthz-w)/2)-590, ((image_heightz-h)/2)+500), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)-590, ((image_heightz-h)/2)+500), tt, font=fuk, fill="white", stroke_width=5, stroke_fill="red")
    draw.text((((image_widthz-w)/2)-200, ((image_heightz-h)/2)+500), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)-200, ((image_heightz-h)/2)+500), tt, font=fuk, fill="pink", stroke_width=5, stroke_fill="red")
    draw.text((((image_widthz-w)/2)+400, ((image_heightz-h)/2)-300), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+400, ((image_heightz-h)/2)-300), tt, font=fuk, fill="lightblue", stroke_width=5, stroke_fill="silver")
    draw.text((((image_widthz-w)/2)+100, ((image_heightz-h)/2)+400), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)+5, ((image_heightz-h)/2)+500), tt, font=fuk, fill="red", stroke_width=5, stroke_fill="gold")
    draw.text((((image_widthz-w)/2)-300, ((image_heightz-h)/2)-400), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)-300, ((image_heightz-h)/2)-400), tt, font=fuk, fill="yellow", stroke_width=5, stroke_fill="silver")
    draw.text((((image_widthz-w)/2)-320, ((image_heightz-h)/2)-230), tt, font=fuk, fill=(255, 255, 255))
    draw.text((((image_widthz-w)/2)-320, ((image_heightz-h)/2)-230), tt, font=fuk, fill="cyan", stroke_width=5, stroke_fill="blue")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(salalogo|darxsjylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/Blankmeisnub.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Younger than me.ttf", 200)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="magenta", stroke_width=3, stroke_fill="green")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)

@register(pattern="^/(hinlogo|darxsjwylogo) ?(.*)")
async def slogo(event):
    if event.fwd_from:
        return
    await event.reply("`Processing..`")
    text = event.pattern_match.group(2)
    img = Image.open('./resources/Blankmeisnub.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "black"
    font = ImageFont.truetype("./resources/Mangal Regular.ttf", 200)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= (image_heightz-h)/2
    draw.text((x, y), text, font=font, fill="magenta", stroke_width=3, stroke_fill="green")
    fname2 = "LogoBy@FRIDAYOT.png"
    img.save(fname2, "png")
    await borg.send_file(event.chat_id, fname2, caption="Made By Anie")
    if os.path.exists(fname2):
            os.remove(fname2)



file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /logo <Text>
 - /slogo <Text>
 - /blogo <Text>
 - /hlogo <Text>
 - /(clogo|cyberlogo) <Text>
 - /llogo <Text>
 - /klogo <Text>
 - /bonk <Bonkifies>
 - /jlogo <Text>
 - /xlogo <Text>
 - /oklogo <Text>
 - /glogo <Text>
 - /dlogo <Text>
 - /salalogo <Text>
 - /hinlogo <text>
 - /Soon...
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
