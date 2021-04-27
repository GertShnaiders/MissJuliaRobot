from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import tbot
from julia import OWNER_ID, SUDO_USERS
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
import wget
from shutil import rmtree
import cv2
import cv2 as cv
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
from julia.Ok import upload_file
DELTA = "https://telegra.ph/file/099688f61c26bc1867bac.jpg"
from julia.func import convert_to_image, crop_vid, runcmd, tgs_to_gif
DANISH = "58199388-5499-4c98-b052-c679b16310f9"
@register(pattern="^/nfsw")
async def hmm(event):
    if event.fwd_from:
        return
    life = DANISH
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    headers = {"api-key": life}
    hmm = await event.reply("Detecting..")
    await event.get_reply_message()
    img = await convert_to_image(event, borg)
    img_file = {
        "image": open(img, "rb"),
    }
    url = "https://api.deepai.org/api/nsfw-detector"
    r = requests.post(url=url, files=img_file, headers=headers).json()
    sedcopy = r["output"]
    hmmyes = sedcopy["detections"]
    game = sedcopy["nsfw_score"]
    await hmm.delete()
    final = f"**IMG RESULT** \n**Detections :** `{hmmyes}` \n**NSFW SCORE :** `{game}`"
    await borg.send_message(event.chat_id, final)
    await hmm.delete()
    if os.path.exists(img):
        os.remove(img)

@register(pattern="^/thug")
async def iamthug(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    hmm = await event.reply("`Converting To thug Image..`")
    await event.get_reply_message()
    img = await convert_to_image(event, borg)
    imagePath = img
    maskPath = "./resources/thuglife/mask.png"
    cascPath = "./resources/thuglife/face_regex.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.15)
    background = Image.open(imagePath)
    for (x, y, w, h) in faces:
        mask = Image.open(maskPath)
        mask = mask.resize((w, h), Image.ANTIALIAS)
        offset = (x, y)
        background.paste(mask, offset, mask=mask)
    file_name = "fridaythug.png"
    ok = sedpath + "/" + file_name
    background.save(ok, "PNG")
    await borg.send_file(event.chat_id, ok)
    await hmm.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)
