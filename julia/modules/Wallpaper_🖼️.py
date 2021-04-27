from julia import CMD_HELP
import os
from julia import tbot
from random import randint

import requests as r

from julia import WALL_API

from julia.events import register

from pymongo import MongoClient
from julia import MONGO_DB_URI
from telethon import types
from telethon.tl import functions

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern="^/wall (.*)")
async def wallpaper(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    chat_id = event.chat_id
    args = event.pattern_match.group(1)
    if not args:
        await event.reply("Please enter some argument!")
        return
    caption = args
    term = args.replace(" ", "%20")
    json_rep = r.get(
        f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
    ).json()
    if not json_rep.get("success"):
        await event.reply("An error occurred! Report this at @MissJuliaRobotSupport")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await event.reply("No results found! Refine your search.")
            return
        index = randint(0, len(wallpapers) - 1)
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        await tbot.send_file(
            chat_id,
            file=wallpaper,
            caption=args,
            reply_to=event.id,
        )

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /wall <topic>: Searches best wallpaper on the given topic and returns them
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
