from julia import CMD_HELP
import os
from julia import tbot
import datetime
from typing import List

import requests
from julia import TIME_API_KEY, MONGO_DB_URI
from julia.events import register
from telethon import types
from telethon.tl import functions
from pymongo import MongoClient

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


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"http://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                if zone["dst"] == 1:
                    daylight_saving = "Yes"
                else:
                    daylight_saving = "No"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (
            f"<b>🌍Country :</b> <code>{country_name}</code>\n"
            f"<b>⏳Zone Name :</b> <code>{country_zone}</code>\n"
            f"<b>🗺Country Code :</b> <code>{country_code}</code>\n"
            f"<b>🌞Daylight saving :</b> <code>{daylight_saving}</code>\n"
            f"<b>🌅Day :</b> <code>{current_day}</code>\n"
            f"<b>⌚Current Time :</b> <code>{current_time}</code>\n"
            f"<b>📆Current Date :</b> <code>{current_date}</code>"
        )
    except BaseException:
        result = None

    return result


@register(pattern="^/datetime ?(.*)")
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

    gay = event.pattern_match.group(1)

    try:
        query = gay
    except BaseException:
        await event.reply("Provide a country name/abbreviation/timezone to find.")
        return

    send_message = await event.reply(
        f"Finding timezone info for <b>{query}</b>", parse_mode="html"
    )

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        await send_message.edit(
            f"Timezone info not available for <b>{query}</b>", parse_mode="html"
        )
        return

    await send_message.edit(result, parse_mode="html")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /datetime <timezone>: Get the present date and time information

**You can check out this [link](https://timezonedb.com/time-zones) for the available timezones**
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
