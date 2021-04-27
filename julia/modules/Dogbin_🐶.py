from datetime import datetime
import os
import requests
from julia.events import register
from julia import tbot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from telethon.tl import functions
from telethon.tl import types
from pymongo import MongoClient
from julia import MONGO_DB_URI

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

BASE_URL = "https://del.dog"

@register(pattern="^/paste ?(.*)")
async def _(event):
    if event.fwd_from:
        return
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
    start = datetime.now()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `/paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await tbot.download_media(
                previous_message,
                TMP_DOWNLOAD_DIRECTORY)
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `/paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.reply("Dogged to {} in {} seconds\nGoTo Original URL: {}".format(url, ms, nurl))
    else:
        await event.reply("Dogged to {} in {} seconds".format(url, ms), link_preview=False)
       
    
@register(pattern="^/getpaste ?(.*)")
async def _(event):
    args = event.pattern_match.group(1)
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

    if len(args) >= 1:
        key=args
    else:
        await event.reply("Please supply a paste key!")
        return

    format_normal = f"{BASE_URL}/"
    format_view = f"{BASE_URL}/v/"

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f"{BASE_URL}/raw/{key}")

    if r.status_code != 200:
        try:
            res = r.json()
            await event.reply(res["message"])
        except Exception:
            if r.status_code == 404:
                await event.reply("Failed to reach dogbin")
            else:
                await event.reply("Unknown error occured")
        r.raise_for_status()

    await event.reply("```" + r.text+ "```", parse_mode="markdown", link_preview=False)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
 - /paste: Create a paste or a shortened url using del.dog
 - /getpaste <key>: Get the content of a paste or shortened url from del.dog
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
