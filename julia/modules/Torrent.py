from julia import tbot, CMD_HELP
import os
import requests, json
from pymongo import MongoClient
from telethon import *
from telethon import events
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from julia import *
from julia.events import register

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
    if isinstance(chat, types.InputPeerUser):          
        return True


@tbot.on(events.NewMessage(pattern="^/torrent (.*)"))
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    sender = event.sender_id
    search = event.pattern_match.group(1)
    index = 0
    chatid = event.chat_id
    msg = await tbot.send_message(chatid, "Loading ...")
    msgid = msg.id
    await tbot.edit_message(
        chatid,
        msgid,
        "Click on the below button to read the torrents 👇",
        buttons=[
            [
                Button.inline(
                    "▶️", data=f"torrent-{sender}|{search}|{index}|{chatid}|{msgid}"
                )
            ],
            [Button.inline("❌", data=f"torrentstop-{sender}|{chatid}|{msgid}")],
        ],
    )


@tbot.on(events.CallbackQuery(pattern=r"torrent(\-(.*))"))
async def paginate_news(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split("-", 1)[1]
    # print(meta)
    if "|" in meta:
        sender, search, index, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    if not event.sender_id == sender:
        await event.answer("You haven't send that command !")
        return
    search = search.strip()
    index = int(index.strip())
    num = index
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    url = f"https://api.sumanjay.cf/torrent/?query={search}"
    try:
        results = requests.get(url).json()
    except Exception as e:
        await event.reply("Sorry, either the server is down or no results found for your query.")
        print(e)
        return
    # print(results)
    age = results[int(num)].get("age")
    leech = results[int(num)].get("leecher")
    mag = results[int(num)].get("magnet")
    name = results[int(num)].get("name")
    seed = results[int(num)].get("seeder")
    size = results[int(num)].get("size")
    typ = results[int(num)].get("type")
    header = f"**#{num} **"
    lastisthis = f"{header} **Name:** {name}\n**Uploaded:** {age} ago\n**Seeders:** {seed}\n**Leechers:** {leech}\n**Size:** {size}\n**Type:** {typ}\n**Magnet Link:** `{mag}`"
    await tbot.edit_message(
        chatid,
        msgid,
        lastisthis,
        link_preview=False,
        buttons=[
            [
                Button.inline(
                    "◀️", data=f"prevtorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
                Button.inline("❌", data=f"torrentstop-{sender}|{chatid}|{msgid}"),
                Button.inline(
                    "▶️", data=f"nexttorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
            ],
            [
                Button.inline(
                    "Refresh 🔁", data=f"newtorrent-{sender}|{search}|{chatid}|{msgid}"
                )
            ],
        ],
    )


@tbot.on(events.CallbackQuery(pattern=r"prevtorrent(\-(.*))"))
async def paginate_prevtorrent(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split("-", 1)[1]
    # print(meta)
    if "|" in meta:
        sender, search, index, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    if not event.sender_id == sender:
        await event.answer("You haven't send that command !")
        return
    search = search.strip()
    index = int(index.strip())
    num = index - 1
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    url = f"https://api.sumanjay.cf/torrent/?query={search}"
    try:
        results = requests.get(url).json()
    except Exception as e:
        await event.reply("Sorry, either the server is down or no results found for your query.")
        print(e)
        return
    vector = len(results)
    if num < 0:
        num = vector - 1
    # print(results)
    age = results[int(num)].get("age")
    leech = results[int(num)].get("leecher")
    mag = results[int(num)].get("magnet")
    name = results[int(num)].get("name")
    seed = results[int(num)].get("seeder")
    size = results[int(num)].get("size")
    typ = results[int(num)].get("type")
    header = f"**#{num} **"
    lastisthis = f"{header} **Name:** {name}\n**Uploaded:** {age} ago\n**Seeders:** {seed}\n**Leechers:** {leech}\n**Size:** {size}\n**Type:** {typ}\n**Magnet Link:** `{mag}`"
    await tbot.edit_message(
        chatid,
        msgid,
        lastisthis,
        link_preview=False,
        buttons=[
            [
                Button.inline(
                    "◀️", data=f"prevtorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
                Button.inline("❌", data=f"torrentstop-{sender}|{chatid}|{msgid}"),
                Button.inline(
                    "▶️", data=f"nexttorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
            ],
            [
                Button.inline(
                    "Refresh 🔁", data=f"newtorrent-{sender}|{search}|{chatid}|{msgid}"
                )
            ],
        ],
    )


@tbot.on(events.CallbackQuery(pattern=r"nexttorrent(\-(.*))"))
async def paginate_nexttorrent(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split("-", 1)[1]
    # print(meta)
    if "|" in meta:
        sender, search, index, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    if not event.sender_id == sender:
        await event.answer("You haven't send that command !")
        return
    search = search.strip()
    index = int(index.strip())
    num = index + 1
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    url = f"https://api.sumanjay.cf/torrent/?query={search}"
    try:
        results = requests.get(url).json()
    except Exception as e:
        await event.reply("Sorry, either the server is down or no results found for your query.")
        print(e)
        return
    vector = len(results)
    if num > vector - 1:
        num = 0
    # print(results)
    age = results[int(num)].get("age")
    leech = results[int(num)].get("leecher")
    mag = results[int(num)].get("magnet")
    name = results[int(num)].get("name")
    seed = results[int(num)].get("seeder")
    size = results[int(num)].get("size")
    typ = results[int(num)].get("type")
    header = f"**#{num} **"
    lastisthis = f"{header} **Name:** {name}\n**Uploaded:** {age} ago\n**Seeders:** {seed}\n**Leechers:** {leech}\n**Size:** {size}\n**Type:** {typ}\n**Magnet Link:** `{mag}`"
    await tbot.edit_message(
        chatid,
        msgid,
        lastisthis,
        link_preview=False,
        buttons=[
            [
                Button.inline(
                    "◀️", data=f"prevtorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
                Button.inline("❌", data=f"torrentstop-{sender}|{chatid}|{msgid}"),
                Button.inline(
                    "▶️", data=f"nexttorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
            ],
            [
                Button.inline(
                    "Refresh 🔁", data=f"newtorrent-{sender}|{search}|{chatid}|{msgid}"
                )
            ],
        ],
    )


@tbot.on(events.CallbackQuery(pattern=r"torrentstop(\-(.*))"))
async def torrentstop(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split("-", 1)[1]
    # print(meta)
    if "|" in meta:
        sender, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    if not event.sender_id == sender:
        await event.answer("You haven't send that command !")
        return
    await tbot.edit_message(
        chatid,
        msgid,
        "Thanks for using.\n❤️ from [Julia](t.me/MissJuliaRobot) !",
        link_preview=False,
    )


@tbot.on(events.CallbackQuery(pattern=r"newtorrent(\-(.*))"))
async def paginate_nexttorrent(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    meta = data.split("-", 1)[1]
    # print(meta)
    if "|" in meta:
        sender, search, chatid, msgid = meta.split("|")
    sender = int(sender.strip())
    if not event.sender_id == sender:
        await event.answer("You haven't send that command !")
        return
    search = search.strip()
    num = 0
    chatid = int(chatid.strip())
    msgid = int(msgid.strip())
    url = f"https://api.sumanjay.cf/torrent/?query={search}"
    try:
        results = requests.get(url).json()
    except Exception as e:
        await event.reply("Sorry, either the server is down or no results found for your query.")
        print(e)
        return
    vector = len(results)
    if num > vector - 1:
        num = 0
    # print(results)
    age = results[int(num)].get("age")
    leech = results[int(num)].get("leecher")
    mag = results[int(num)].get("magnet")
    name = results[int(num)].get("name")
    seed = results[int(num)].get("seeder")
    size = results[int(num)].get("size")
    typ = results[int(num)].get("type")
    header = f"**#{num} **"
    lastisthis = f"{header} **Name:** {name}\n**Uploaded:** {age} ago\n**Seeders:** {seed}\n**Leechers:** {leech}\n**Size:** {size}\n**Type:** {typ}\n**Magnet Link:** `{mag}`"
    await tbot.edit_message(
        chatid,
        msgid,
        lastisthis,
        link_preview=False,
        buttons=[
            [
                Button.inline(
                    "◀️", data=f"prevtorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
                Button.inline("❌", data=f"torrentstop-{sender}|{chatid}|{msgid}"),
                Button.inline(
                    "▶️", data=f"nexttorrent-{sender}|{search}|{num}|{chatid}|{msgid}"
                ),
            ],
            [
                Button.inline(
                    "Refresh 🔁", data=f"newtorrent-{sender}|{search}|{chatid}|{msgid}"
                )
            ],
        ],
    )


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /torrent <item>: Returns torrent links for the item.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
