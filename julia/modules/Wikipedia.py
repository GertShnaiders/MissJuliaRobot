import wikipedia
from julia import *
from wikipedia.exceptions import DisambiguationError, PageError
from pymongo import MongoClient
from telethon import *
from telethon.tl import *
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


@register(pattern="^/wiki ?(.*)")
async def _(event):
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
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.reply("Please provide some input.")
        return
    res = ""
    search = input_str
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        await event.reply(
            "Disambiguated pages found! Adjust your query accordingly.\n<i>{}</i>".format(e),
            parse_mode="html",
        )
    except PageError as e:
        await event.reply(
            "<code>{}</code>".format(e), parse_mode="html"
        )
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Read more...</a>"""
        if len(result) > 4000:
            with open("result.txt", "w") as f:
                f.write(f"{result}")
            with open("result.txt", "rb") as f:
                await tbot.send_file(
                    chat_id=event.chat_id,
                    file=f,
                    filename=f.name,
                    reply_to=event,                    
                    parse_mode="html",
                )
        else:
            await event.reply(
                result, parse_mode="html", link_preview=False
            )

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /wiki <search>: Find results for search in wikipedia and return it.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
