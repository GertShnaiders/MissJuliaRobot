from julia import tbot as borg
from julia import TEMP_DOWNLOAD_DIRECTORY as TMP_DOWNLOAD_DIRECTORY
from telethon import events
import json
import math
import os
import re
import shlex
import subprocess
import time
import eyed3
from os.path import basename
from typing import List, Optional, Tuple
import webbrowser
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import re
from telethon.tl.types import InputMessagesFilterDocument
import telethon
from telethon import Button, custom, events, functions
from pymediainfo import MediaInfo
from telethon.tl.types import MessageMediaPhoto
from typing import Union
SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
BASE_URL = "https://isubtitles.org"
import zipfile
import os
import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
headers = {"UserAgent": UserAgent().random}
import asyncio
import random
import requests
import string
from bs4 import BeautifulSoup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import hachoir
import asyncio
import os
from julia.Ok import upload_file, download_file
from pathlib import Path
from selenium import webdriver
import time
import requests
import shutil
import os
import argparse
import wget
from julia import logging
sedpath = TMP_DOWNLOAD_DIRECTORY
session = aiohttp.ClientSession()
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)

async def fetch_json(link):
    async with session.get(link) as resp:
        return await resp.json()

def get_readable_file_size(size_in_bytes: Union[int, float]) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


def get_readable_time(secs: float) -> str:
    result = ""
    (days, remainder) = divmod(secs, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
            ((str(days) + " day(s), ") if days else "")
            + ((str(hours) + " hour(s), ") if hours else "")
            + ((str(minutes) + " minute(s), ") if minutes else "")
            + ((str(seconds) + " second(s), ") if seconds else "")
            + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]

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

def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await event.reply(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                    
                )
            except:
                pass
        else:
            try:
                await event.reply("{}\n{}".format(type_of_ps, tmp))
            except:
                pass


async def convert_to_image(event, borg):
    lmao = await event.get_reply_message()
    if not (
            lmao.gif
            or lmao.audio
            or lmao.voice
            or lmao.video
            or lmao.video_note
            or lmao.photo
            or lmao.sticker
            or lmao.media
    ):
        await event.reply("`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                lmao.media,
                sedpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            j = await event.reply(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.reply("Download Unsucessfull :(")
        return
    if lmao and lmao.photo:
        lmao_final = downloaded_file_name
    elif lmao.sticker and lmao.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(sedpath, "SED.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        lmao_final = image_name20
    elif lmao.sticker and lmao.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = sedpath + "image.png"
        os.rename(pathofsticker2, image_new_path)
        if not os.path.exists(image_new_path):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = image_new_path
    elif lmao.audio:
        sed_p = downloaded_file_name
        hmmyes = sedpath + "stark.mp3"
        imgpath = sedpath + "starky.jpg"
        os.rename(sed_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(sed_p)
        if not os.path.exists(imgpath):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = imgpath
    elif lmao.gif or lmao.video or lmao.video_note:
        sed_p2 = downloaded_file_name
        jpg_file = os.path.join(sedpath, "image.jpg")
        await take_screen_shot(sed_p2, 0, jpg_file)
        os.remove(sed_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Couldn't Fetch. SS`")
            return
        lmao_final = jpg_file
    await j.edit("`Almost Completed.`")
    await j.delete()
    return lmao_final

async def crop_vid(input_vid: str, final_path: str):
    media_info = MediaInfo.parse(input_vid)
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        os.system(f'ffmpeg -i {input_vid} -vf "crop={crop_by}:{crop_by}" {final_path}')
        os.remove(input_vid)
    else:
        os.rename(input_vid, final_path)

def tgs_to_gif(sticker_path: str, quality: int = 256) -> str:                  
    dest = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "animation.gif")
    with open(dest, 'wb') as t_g:
        lottie.exporters.gif.export_gif(lottie.parsers.tgs.parse_tgs(sticker_path), t_g, quality, 1)
    os.remove(sticker_path)
    return dest
