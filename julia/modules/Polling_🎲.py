from julia import CMD_HELP, BOT_ID
import os
from julia import tbot
from telethon import *
from telethon.tl import *
from julia.events import register
from pymongo import MongoClient
from julia import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
dbb = client["missjuliarobot"]
poll_id = dbb.pollid


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


@register(pattern="^/poll (.*)")
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
    try:
        quew = event.pattern_match.group(1)
    except Exception:
        await event.reply("Where is the question ?")
        return
    if "|" in quew:
        secrets, quess, options = quew.split("|")
    secret = secrets.strip()

    if not secret:
        await event.reply("I need a poll id of 5 digits to make a poll")
        return

    try:
        secret = str(secret)
    except ValueError:
        await event.reply("Poll id should contain only numbers")
        return

    # print(secret)

    if len(secret) != 5:
        await event.reply("Poll id should be an integer of 5 digits")
        return

    allpoll = poll_id.find({})
    # print(secret)
    for c in allpoll:
        if event.sender_id == c["user"]:
            await event.reply("Please stop the previous poll before creating a new one !")
            return
    poll_id.insert_one({"user": event.sender_id, "pollid": secret})

    ques = quess.strip()
    option = options.strip()
    quiz = option.split(" ")[1 - 1]
    if "True" in quiz:
        quizy = True
        if "@" in quiz:
            one, two = quiz.split("@")
            rightone = two.strip()
        else:
            await event.reply(
                "You need to select the right answer with question number like True@1, True@3 etc.."
            )
            return

        quizoptionss = []
        try:
            ab = option.split(" ")[4 - 1]
            cd = option.split(" ")[5 - 1]
            quizoptionss.append(types.PollAnswer(ab, b"1"))
            quizoptionss.append(types.PollAnswer(cd, b"2"))
        except Exception:
            await event.reply("At least need two options to create a poll")
            return
        try:
            ef = option.split(" ")[6 - 1]
            quizoptionss.append(types.PollAnswer(ef, b"3"))
        except Exception:
            ef = None
        try:
            gh = option.split(" ")[7 - 1]
            quizoptionss.append(types.PollAnswer(gh, b"4"))
        except Exception:
            gh = None
        try:
            ij = option.split(" ")[8 - 1]
            quizoptionss.append(types.PollAnswer(ij, b"5"))
        except Exception:
            ij = None
        try:
            kl = option.split(" ")[9 - 1]
            quizoptionss.append(types.PollAnswer(kl, b"6"))
        except Exception:
            kl = None
        try:
            mn = option.split(" ")[10 - 1]
            quizoptionss.append(types.PollAnswer(mn, b"7"))
        except Exception:
            mn = None
        try:
            op = option.split(" ")[11 - 1]
            quizoptionss.append(types.PollAnswer(op, b"8"))
        except Exception:
            op = None
        try:
            qr = option.split(" ")[12 - 1]
            quizoptionss.append(types.PollAnswer(qr, b"9"))
        except Exception:
            qr = None
        try:
            st = option.split(" ")[13 - 1]
            quizoptionss.append(types.PollAnswer(st, b"10"))
        except Exception:
            st = None

    elif "False" in quiz:
        quizy = False
    else:
        await event.reply("Wrong arguments provided !")
        return

    pvote = option.split(" ")[2 - 1]
    if "True" in pvote:
        pvoty = True
    elif "False" in pvote:
        pvoty = False
    else:
        await event.reply("Wrong arguments provided !")
        return
    mchoice = option.split(" ")[3 - 1]
    if "True" in mchoice:
        mchoicee = True
    elif "False" in mchoice:
        mchoicee = False
    else:
        await event.reply("Wrong arguments provided !")
        return
    optionss = []
    try:
        ab = option.split(" ")[4 - 1]
        cd = option.split(" ")[5 - 1]
        optionss.append(types.PollAnswer(ab, b"1"))
        optionss.append(types.PollAnswer(cd, b"2"))
    except Exception:
        await event.reply("At least need two options to create a poll")
        return
    try:
        ef = option.split(" ")[6 - 1]
        optionss.append(types.PollAnswer(ef, b"3"))
    except Exception:
        ef = None
    try:
        gh = option.split(" ")[7 - 1]
        optionss.append(types.PollAnswer(gh, b"4"))
    except Exception:
        gh = None
    try:
        ij = option.split(" ")[8 - 1]
        optionss.append(types.PollAnswer(ij, b"5"))
    except Exception:
        ij = None
    try:
        kl = option.split(" ")[9 - 1]
        optionss.append(types.PollAnswer(kl, b"6"))
    except Exception:
        kl = None
    try:
        mn = option.split(" ")[10 - 1]
        optionss.append(types.PollAnswer(mn, b"7"))
    except Exception:
        mn = None
    try:
        op = option.split(" ")[11 - 1]
        optionss.append(types.PollAnswer(op, b"8"))
    except Exception:
        op = None
    try:
        qr = option.split(" ")[12 - 1]
        optionss.append(types.PollAnswer(qr, b"9"))
    except Exception:
        qr = None
    try:
        st = option.split(" ")[13 - 1]
        optionss.append(types.PollAnswer(st, b"10"))
    except Exception:
        st = None

    if pvoty is False and quizy is False and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(id=12345, question=ques, answers=optionss, quiz=False)
            ),
        )

    if pvoty is True and quizy is False and mchoicee is True:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=True,
                    public_voters=True,
                )
            ),
        )

    if pvoty is False and quizy is False and mchoicee is True:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=True,
                    public_voters=False,
                )
            ),
        )

    if pvoty is True and quizy is False and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=optionss,
                    quiz=False,
                    multiple_choice=False,
                    public_voters=True,
                )
            ),
        )

    if pvoty is False and quizy is True and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345, question=ques, answers=quizoptionss, quiz=True
                ),
                correct_answers=[f"{rightone}"],
            ),
        )

    if pvoty is True and quizy is True and mchoicee is False:
        await tbot.send_file(
            event.chat_id,
            types.InputMediaPoll(
                poll=types.Poll(
                    id=12345,
                    question=ques,
                    answers=quizoptionss,
                    quiz=True,
                    public_voters=True,
                ),
                correct_answers=[f"{rightone}"],
            ),
        )

    if pvoty is True and quizy is True and mchoicee is True:
        await event.reply("You can't use multiple voting with quiz mode")
        return
    if pvoty is False and quizy is True and mchoicee is True:
        await event.reply("You can't use multiple voting with quiz mode")
        return


@register(pattern="^/stoppoll(?: |$)(.*)")
async def stop(event):
    secret = event.pattern_match.group(1)
    # print(secret)
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

    if not event.reply_to_msg_id:
        await event.reply("Please reply to a poll to stop it")
        return

    if input is None:
        await event.reply("Where is the poll id ?")
        return

    try:
        secret = str(secret)
    except ValueError:
        await event.reply("Poll id should contain only numbers")
        return

    if len(secret) != 5:
        await event.reply("Poll id should be an integer of 5 digits")
        return

    msg = await event.get_reply_message()

    if str(msg.sender_id) != str(BOT_ID):
        await event.reply(
            "I can't do this operation on this poll.\nProbably it's not created by me"
        )
        return
    print(secret)
    if msg.poll:
        allpoll = poll_id.find({})
        for c in allpoll:
            if not event.sender_id == c["user"] and not secret == c["pollid"]:
                await event.reply("Oops, either you haven't created this poll or you have given wrong poll id")
                return
        if msg.poll.poll.closed:
            await event.reply("Oops, the poll is already closed.")
            return
        poll_id.delete_one({"user": event.sender_id})
        pollid = msg.poll.poll.id
        await msg.edit(
            file=types.InputMediaPoll(
                poll=types.Poll(
                    id=pollid, question="", answers=[], closed=True
                )
            )
        )
        await event.reply("Successfully stopped the poll")
    else:
        await event.reply("This isn't a poll")


@register(pattern="^/forgotpollid$")
async def stop(event):
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
    allpoll = poll_id.find({})
    for c in allpoll:
        if event.sender_id == c["user"]:
            try:
                poll_id.delete_one({"user": event.sender_id})
                await event.reply("Done you can now create a new poll.")
            except Exception:
                await event.reply("Seems like you haven't created any poll yet !")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
You can now send polls anonymously with Julia

Here is how you can do it:

**Parameters** -
 ▪️ poll-id - a poll id consists of an 5 digit random integer, this id is automatically removed from the system when you stop your previous poll
 ▪️ question - the question you wanna ask
 ▪️ <True@optionnumber/False>(1) - quiz mode, you must state the correct answer with `@` eg: `True@1` or `True@2`
 ▪️ <True/False>(2) - public votes
 ▪️ <True/False>(3) - multiple choice

**Syntax** -
`/poll <poll-id> <question> | <True@optionnumber/False> <True/False> <True/False> <option1> <option2> ... upto <option10>`

**Examples** -
`/poll 12345 | am i cool? | False False False yes no`
`/poll 12345 | am i cool? | True@1 False False yes no`

**To stop a poll**
Reply to the poll with `/stoppoll <poll-id>` to stop the poll

**NOTE**
If you have forgotten your poll id or deleted the poll so that you can't stop the previous poll type `/forgotpollid`, this will reset the poll id, you will have no access to the previous poll !
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
