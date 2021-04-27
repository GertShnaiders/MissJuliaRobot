import csv
import json
import os
import re
import time
import uuid
from io import BytesIO
import julia.modules.sql.feds_sql as sql
from telethon import *
from telethon.tl import *
from telethon.tl.types import User
from julia import *
from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename
from julia.events import register
from pymongo import MongoClient

# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo and AyraHikari too
# Federation by MrYacha 2018-2019
# Federation rework by Mizukito Akito 2019
# Federation update v2 by Ayra Hikari 2019
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 22+ hours by @peaktogoo
# Time spended on updating version to v2 = 26+ hours by @AyraHikari
# Total spended for making this features is 68+ hours
# LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")
# ME @MissJulia_Robot has also done a lot of hard work to rewrite this in telethon so add this line as a credit. Please don't remove this if you somewhat respect me.


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
    return False


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("Pass the user's username, id or reply!")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await tbot.get_entity(user_id)
                return user_obj
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return user_obj


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@register(pattern="^/newfed ?(.*)")
async def _(event):
    chat = event.chat_id
    user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, user.id):
            pass
        else:
            return
    message = event.pattern_match.group(1)
    if not event.is_private:
        await event.reply("Federations can only be created by privately messaging me.")
        return
    fednam = message
    if not fednam:
        await event.reply("Please write the name of the federation!")
        return
    if fednam:
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        # LOGGER.info(fed_id)

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            await event.reply(
                "Can't create federation!\nPlease contact @MissJuliaRobotSupport if the problem persists."
            )
            return

        await event.reply(
            "**You have successfully created a new federation!**"
            "\nName: `{}`"
            "\nID: `{}`"
            "\n\nUse the command below to join the federation:"
            "\n`/joinfed {}`".format(fed_name, fed_id, fed_id),
            parse_mode="markdown",
        )
    else:
        await event.reply("Please write down the name of the federation")


@register(pattern="^/delfed ?(.*)")
async def _(event):
    try:
        args = event.pattern_match.group(1)
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, user.id):
                pass
            else:
                return
        message = event.message.id
        if not event.is_private:
            await event.reply(
                "Federations can only be deleted by privately messaging me."
            )
            return
        if args:
            is_fed_id = args
            getinfo = sql.get_fed_info(is_fed_id)
            if getinfo is False:
                await event.reply("This federation does not exist.")
                return
            if int(getinfo["owner"]) == int(user.id) or int(user.id) == OWNER_ID:
                fed_id = is_fed_id
            else:
                await event.reply("Only federation owners can do this!")
                return
        else:
            await event.reply("What should I delete?")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only federation owners can do this!")
            return
        await tbot.send_message(
            event.chat_id,
            "Are You sure you want to delete your federation ?\nThis cannot be reverted, you will lose your entire ban list, and '**{}**' will be permanently lost !".format(
                getinfo["fname"]
            ),
            buttons=[
                [Button.inline("⚠️ Delete Federation", data="rmfed_{}".format(fed_id))],
                [Button.inline("Cancel", data="rmfed_cancel")],
            ],
            reply_to=message,
        )
    except Exception as e:
        print(e)
        pass


@tbot.on(events.CallbackQuery(pattern=r"rmfed(\_(.*))"))
async def delete_fed(event):
    # print("1")
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split("_", 1)[1]
    print(fed_id)
    if not event.is_private:
        return
    if fed_id == "cancel":
        await event.edit("Federation deletion cancelled")
        return
    getfed = sql.get_fed_info(fed_id)
    if getfed:
        delete = sql.del_fed(fed_id)
        if delete:
            await event.edit(
                "You have removed your Federation! Now all the Groups that are connected with '**{}**' do not have a Federation.".format(
                    getfed["fname"]
                ),
                parse_mode="markdown",
            )


@register(pattern="^/renamefed ?(.*) ?(.*)")
async def _(event):
    args = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if not args:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")
    if not fedid:
        return await event.reply("usage: `/renamefed <fed_id> <newname>`")
    fed_id, newname = args, fedid
    verify_fed = sql.get_fed_info(fed_id)
    if not verify_fed:
        return await event.reply("This fed not exist in my database!")
    if is_user_fed_owner(fed_id, user.id):
        sql.rename_fed(fed_id, user.id, newname)
        await event.reply(f"Successfully renamed your fed name to {newname}!")
    else:
        await event.reply("Only federation owner can do this!")


@register(pattern="^/chatfed$")
async def _(event):
    chat = event.chat_id
    # user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    fed_id = sql.get_fed_id(chat)
    if not fed_id:
        await event.reply("This group is not in any federation!")
        return
    info = sql.get_fed_info(fed_id)
    text = "This group is part of the following federation:"
    text += "\n{} (ID: <code>{}</code>)".format(info["fname"], fed_id)
    await event.reply(text, parse_mode="html")


@tbot.on(events.NewMessage(pattern="^/joinfed ?(.*)"))
async def _(event):
    chat = event.chat_id
    user = event.sender
    args = event.pattern_match.group(1)
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return
    if not args:
        await event.reply("Where is the federation ID ?")
        return

    fed_id = sql.get_fed_id(chat)

    if user.id == OWNER_ID:
        pass
    else:
        try:
            async for userr in tbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(event.sender_id) == int(aid):
                        await event.reply("Only group creators can use this command!")
                        return
        except Exception as e:
            print(e)
    if fed_id:
        await event.reply("You cannot join two federations from one chat")
        return

    if args:
        getfed = sql.search_fed_by_id(args)
        if getfed is False:
            await event.reply("Please enter a valid federation ID")
            return

        x = sql.chat_join_fed(args, event.chat.title, chat)
        if not x:
            await event.reply(
                "Failed to join federation! Please contact @MissJuliaRobotSupport should this problem persist!"
            )
            return

        get_fedlog = sql.get_fed_log(args)
        if get_fedlog:
            try:
                await tbot.send_message(
                    int(get_fedlog),
                    "Chat **{}** has joined the federation **{}**".format(
                        event.chat.title, getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
            except Exception as e:
                print(e)
                pass
        await event.reply(
            "This group has joined the federation: **{}**".format(getfed["fname"])
        )


@register(pattern="^/leavefed$")
async def _(event):
    chat = event.chat_id
    user = event.sender
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)
    fed_info = sql.get_fed_info(fed_id)

    if user.id == OWNER_ID:
        pass
    else:
        try:
            async for userr in tbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(event.sender_id) != int(aid):
                        await event.reply("Only group creators can use this command!")
                        return
        except Exception as e:
            print(e)
    if sql.chat_leave_fed(chat) is True:
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            try:
                await tbot.send_message(
                    int(get_fedlog),
                    "Chat **{}** has left the federation **{}**".format(
                        event.chat.title, fed_info["fname"]
                    ),
                    parse_mode="markdown",
                )
            except Exception as e:
                print(e)
                pass
        await event.reply(
            "This group has left the federation **{}**".format(fed_info["fname"])
        )
    else:
        await event.reply("How can you leave a federation that you never joined ?")


@register(pattern="^/fpromote(?: |$)(.*)")
async def _(event):
    chat = event.chat_id
    args = await get_user_from_event(event)
    user = event.sender
    if args:
        pass
    else:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)

    if is_user_fed_owner(fed_id, user.id):
        userid = args
        if not userid:
            await event.reply("Reply to a message or give a entity to promote")
            return
        user_id = userid.id
        getuser = sql.search_user_in_fed(fed_id, user_id)
        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)
        get_owner = eval(info["fusers"])["owner"]
        try:
            async for userr in tbot.iter_participants(
                event.chat_id, filter=types.ChannelParticipantsAdmins
            ):
                if not isinstance(userr.participant, types.ChannelParticipantCreator):
                    aid = userr.id
                    if int(aid) == int(get_owner):
                        await event.reply("Hey that's the federation owner !")
                        return
        except Exception as e:
            print(e)
        if getuser:
            await event.reply(
                "I cannot promote users who are already federation admins! Can remove them if you want!"
            )
            return
        if int(user_id) == int(BOT_ID):
            await event.reply("I already am a federation admin in all federations!")
            return
        res = sql.user_join_fed(fed_id, user_id)
        if res:
            await event.reply("Successfully Promoted!")
        else:
            await event.reply("Failed to promote!")
    else:
        await event.reply("Only federation owners can do this!")


@register(pattern="^/fdemote(?: |$)(.*)")
async def _(event):
    chat = event.chat_id
    args = await get_user_from_event(event)
    user = event.sender
    if args:
        pass
    else:
        return

    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return

    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)

    if is_user_fed_owner(fed_id, user.id):
        userid = args
        if not userid:
            await event.reply("Reply to a message or give a entity to promote")
            return
        user_id = userid.id

        if user_id == BOT_ID:
            await event.reply("You can't demote me from a federation created by me !")
            return

        if sql.search_user_in_fed(fed_id, user_id) is False:
            await event.reply("I cannot demote people who are not federation admins!")
            return

        res = sql.user_demote_fed(fed_id, user_id)
        if res is True:
            await event.reply("Demoted from Fed Admin!")
        else:
            await event.reply("Demotion failed!")
    else:
        await event.reply("Only federation owners can do this!")
        return


def is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
    if int(user_id) in fed_admins or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@register(pattern="^/fedinfo ?(.*)")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if args:
            fed_id = args
            info = sql.get_fed_info(fed_id)
        else:
            fed_id = sql.get_fed_id(chat)
            if not fed_id:
                await event.reply("This chat is not in any federation!")
                return
            info = sql.get_fed_info(fed_id)

        if not info:
            await event.reply("Couldn't find information about that federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only a federation admin can do this!")
            return

        owner = await tbot.get_entity(int(info["owner"]))
        try:
            owner_name = owner.first_name + " " + owner.last_name
        except:
            owner_name = owner.first_name
        FEDADMIN = sql.all_fed_users(fed_id)
        TotalAdminFed = len(FEDADMIN)

        text = "<b>ℹ️ Federation Information:</b>"
        text += "\nFedID: <code>{}</code>".format(fed_id)
        text += "\nName: {}".format(info["fname"])
        text += f"\nCreator: <p><a href='tg://user?id={owner.id}'>{owner_name}</a></p>"
        text += "\nAll Admins: <code>{}</code>".format(TotalAdminFed)
        getfban = sql.get_all_fban_users(fed_id)
        text += "\nTotal banned users: <code>{}</code>".format(len(getfban))
        getfchat = sql.all_fed_chats(fed_id)
        text += "\nNumber of groups in this federation: <code>{}</code>".format(
            len(getfchat)
        )
        await event.reply(text, parse_mode="html")
    except Exception as e:
        print(e)
        pass


@register(pattern="^/fedadmins$")
async def _(event):
    try:
        chat = event.chat_id
        args = False
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if args:
            fed_id = args
            info = sql.get_fed_info(fed_id)
        else:
            fed_id = sql.get_fed_id(chat)
            if not fed_id:
                await event.reply("This chat is not in any federation!")
                return
            info = sql.get_fed_info(fed_id)

        if not info:
            await event.reply("Couldn't find information about that federation!")
            return

        # print(fed_id+"\n"+user.id)
        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        text = "<b>Federation Admin {}:</b>\n\n".format(info["fname"])
        text += "👑 Owner:\n"
        owner = await tbot.get_entity(int(info["owner"]))
        try:
            owner_name = owner.first_name + " " + owner.last_name
        except:
            owner_name = owner.first_name
        text += f" • <p><a href='tg://user?id={owner.id}'>{owner_name}</a></p>\n"

        members = sql.all_fed_members(fed_id)
        if len(members) == 0:
            text += "\n🔱 There are no admins in this federation"
        else:
            text += "\n🔱 Admin:\n"
            for x in members:
                user = await tbot.get_entity(int(x))
                unamee = user.first_name
                text += f" • <p><a href='tg://user?id={user.id}'>{unamee}</a></p>\n"

        await event.reply(text, parse_mode="html")
    except Exception as e:
        print(e)
        pass


@register(pattern="^/fban (.*)")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        info = sql.get_fed_info(fed_id)
        getfednotif = sql.user_feds_report(info["owner"])

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        if "|" in args:
            iid, reasonn = args.split("|")
        cid = iid.strip()
        reason = reasonn.strip()
        if cid.isnumeric():
            cid = int(cid)
        entity = await tbot.get_input_entity(cid)
        try:
            user_id = entity.user_id
        except Exception:
            await event.reply("Couldn't fetch that user.")
            return
        if not reason:
            await event.reply("Need a reason for fban.")
            return
        fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user_id)

        if not user_id:
            await event.reply("You don't seem to be referring to a user")
            return

        if user_id == BOT_ID:
            await event.reply("Haha you can't fban me.")
            return

        if is_user_fed_owner(fed_id, user_id) is True:
            await event.reply("You are the fed owner.\nI will not fban you !")
            return

        if is_user_fed_admin(fed_id, user_id) is True:
            await event.reply("That's a federation admin, I can't fban.")
            return

        if user_id == OWNER_ID:
            await event.reply("Haha i will never fban my owner !")
            return

        if user_id in [777000, 1087968824]:
            await event.reply("Fool! You can't attack Telegram's native tech!")
            return

        try:
            user_chat = await tbot.get_entity(user_id)
            isvalid = True
            fban_user_id = user_chat.id
            fban_user_name = user_chat.first_name
            fban_user_lname = user_chat.last_name
            fban_user_uname = user_chat.username
        except Exception as e:
            if not str(user_id).isdigit():
                await event.reply(e)
                return
            elif len(str(user_id)) != 9:
                await event.reply("That's not a user!")
                return
            isvalid = False
            fban_user_id = int(user_id)
            fban_user_name = "user({})".format(user_id)
            fban_user_lname = None
            fban_user_uname = None

        if isvalid and not isinstance(user_chat, User):
            await event.reply("That's not a user!")
            return

        if isvalid:
            user_target = (
                f"<p><a href='tg://user?id={fban_user_id}'>{fban_user_name}</a></p>"
            )
        else:
            user_target = fban_user_name

        if fban:
            fed_name = info["fname"]
            temp = sql.un_fban_user(fed_id, fban_user_id)
            if not temp:
                await event.reply("Failed to update the reason for fedban!")
                return
            x = sql.fban_user(
                fed_id,
                fban_user_id,
                fban_user_name,
                fban_user_lname,
                fban_user_uname,
                reason,
                int(time.time()),
            )
            if not x:
                await event.reply(
                    "Failed to ban from the federation! If this problem continues, contact @MissJuliaRobotSupport."
                )
                return

            fed_chats = sql.all_fed_chats(fed_id)
            # Will send to current chat
            await tbot.send_message(
                chat,
                "<b>FedBan reason updated</b>"
                "\n<b>Federation:</b> {}"
                "\n<b>Federation Admin:</b> {}"
                "\n<b>User:</b> {}"
                "\n<b>User ID:</b> <code>{}</code>"
                "\n<b>Reason:</b> {}".format(
                    fed_name,
                    f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                    user_target,
                    fban_user_id,
                    reason,
                ),
                parse_mode="html",
            )
            # Send message to owner if fednotif is enabled
            if getfednotif:
                try:
                    await tbot.send_message(
                        int(info["owner"]),
                        "<b>FedBan reason updated</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>"
                        "\n<b>Reason:</b> {}".format(
                            fed_name,
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                            reason,
                        ),
                        parse_mode="html",
                    )
                except Exception as e:
                    print(e)
                    pass
            # If fedlog is set, then send message, except fedlog is current chat
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if int(get_fedlog) != int(chat):
                    try:
                        await tbot.send_message(
                            int(get_fedlog),
                            "<b>FedBan reason updated</b>"
                            "\n<b>Federation:</b> {}"
                            "\n<b>Federation Admin:</b> {}"
                            "\n<b>User:</b> {}"
                            "\n<b>User ID:</b> <code>{}</code>"
                            "\n<b>Reason:</b> {}".format(
                                fed_name,
                                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                                user_target,
                                fban_user_id,
                                reason,
                            ),
                            parse_mode="html",
                        )
                    except Exception as e:
                        print(e)
                        pass
            for fedschat in fed_chats:
                try:
                    await tbot.kick_participant(fedschat, fban_user_id)
                except Exception as e:
                    sql.chat_leave_fed(fedschat)
                    print(e)
                    pass

            # Fban for fed subscriber
            subscriber = list(sql.get_subscriber(fed_id))
            if len(subscriber) != 0:
                for fedsid in subscriber:
                    all_fedschat = sql.all_fed_chats(fedsid)
                    for fedschat in all_fedschat:
                        try:
                            await tbot.kick_participant(fedschat, fban_user_id)
                        except Exception as e:
                            print(e)
                            continue
            return

        fed_name = info["fname"]

        x = sql.fban_user(
            fed_id,
            fban_user_id,
            fban_user_name,
            fban_user_lname,
            fban_user_uname,
            reason,
            int(time.time()),
        )
        if not x:
            await event.reply(
                "Failed to ban from the federation! If this problem continues, contact @OnePunchSupport."
            )
            return

        fed_chats = sql.all_fed_chats(fed_id)
        # Will send to current chat
        await tbot.send_message(
            chat,
            "<b>FedBan reason updated</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>Federation Admin:</b> {}"
            "\n<b>User:</b> {}"
            "\n<b>User ID:</b> <code>{}</code>"
            "\n<b>Reason:</b> {}".format(
                fed_name,
                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                user_target,
                fban_user_id,
                reason,
            ),
            parse_mode="html",
        )
        # Send message to owner if fednotif is enabled
        if getfednotif:
            try:
                await tbot.send_message(
                    int(info["owner"]),
                    "<b>FedBan reason updated</b>"
                    "\n<b>Federation:</b> {}"
                    "\n<b>Federation Admin:</b> {}"
                    "\n<b>User:</b> {}"
                    "\n<b>User ID:</b> <code>{}</code>"
                    "\n<b>Reason:</b> {}".format(
                        fed_name,
                        f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                        user_target,
                        fban_user_id,
                        reason,
                    ),
                    parse_mode="html",
                )
            except Exception as e:
                print(e)
                pass
        # If fedlog is set, then send message, except fedlog is current chat
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if int(get_fedlog) != int(chat):
                try:
                    await tbot.send_message(
                        int(get_fedlog),
                        "<b>FedBan reason updated</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>"
                        "\n<b>Reason:</b> {}".format(
                            fed_name,
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                            reason,
                        ),
                        parse_mode="html",
                    )
                except Exception as e:
                    print(e)
                    pass
        chats_in_fed = 0
        for fedschat in fed_chats:
            chats_in_fed += 1
            try:
                await tbot.kick_participant(fedschat, fban_user_id)
            except Exception as e:
                print(e)
                pass

            # Fban for fed subscriber
            subscriber = list(sql.get_subscriber(fed_id))
            if len(subscriber) != 0:
                for fedsid in subscriber:
                    all_fedschat = sql.all_fed_chats(fedsid)
                    for fedschat in all_fedschat:
                        try:
                            await tbot.kick_participant(fedschat, fban_user_id)
                        except Exception as e:
                            print(e)
                            pass
    except Exception as e:
        print(e)
        pass


@register(pattern="^/frules$")
async def _(event):
    chat = event.chat_id
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        else:
            return
    if event.is_private:
        await event.reply("This command is specific to the group, not to my pm !")
        return

    fed_id = sql.get_fed_id(chat)
    if not fed_id:
        await event.reply("This group is not in any federation!")
        return

    rules = sql.get_frules(fed_id)
    text = "**Rules for this fed:**\n\n"
    text += rules
    await event.reply(text)


@register(pattern="^/setfrules ?(.*)")
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only fed admins can do this!")
            return

        if args:
            x = sql.set_frules(fed_id, args)
            if not x:
                await event.reply(
                    "There was an error while setting federation rules!\nPlease go to @MissJuliaRobotSupport to report this."
                )
                return

            rules = sql.get_fed_info(fed_id)["frules"]
            getfed = sql.get_fed_info(fed_id)
            get_fedlog = sql.get_fed_log(fed_id)
            if get_fedlog:
                if eval(get_fedlog):
                    try:
                        await tbot.send_message(
                            int(get_fedlog),
                            "**{}** has updated federation rules for fed **{}**".format(
                                user.first_name, getfed["fname"]
                            ),
                            parse_mode="markdown",
                        )
                    except Exception as e:
                        print(e)
                        pass
            await event.reply(f"Rules have been changed to :\n\n{rules}")
        else:
            await event.reply("Please give some rules to set.")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/unfban (.*)"))
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        info = sql.get_fed_info(fed_id)
        getfednotif = sql.user_feds_report(info["owner"])

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        if args.isnumeric():
            cid = int(args)
        else:
            cid = args
        entity = await tbot.get_input_entity(cid)

        try:
            user_id = entity.user_id
        except Exception:
            await event.reply("Couldn't fetch that user.")
            return

        if not user_id:
            await event.reply("You do not seem to be referring to a user.")
            return

        try:
            user_chat = await tbot.get_entity(user_id)
            isvalid = True
            fban_user_id = user_chat.id
            fban_user_name = user_chat.first_name
            fban_user_lname = user_chat.last_name
            fban_user_uname = user_chat.username
        except Exception as e:
            if not str(user_id).isdigit():
                await event.reply(e)
                return
            elif len(str(user_id)) != 9:
                await event.reply("That's not a user!")
                return
            isvalid = False
            fban_user_id = int(user_id)
            fban_user_name = "user({})".format(user_id)
            fban_user_lname = None
            fban_user_uname = None

        if isvalid and not isinstance(user_chat, User):
            await event.reply("That's not a user!")
            return

        if isvalid:
            user_target = (
                f"<p><a href='tg://user?id={fban_user_id}'>{fban_user_name}</a></p>"
            )
        else:
            user_target = fban_user_name

        fban, fbanreason, fbantime = sql.get_fban_user(fed_id, fban_user_id)
        if fban is False:
            await event.reply("This user is not fbanned!")
            return

        chat_list = sql.all_fed_chats(fed_id)
        # Will send to current chat
        await tbot.send_message(
            chat,
            "<b>Un-FedBan</b>"
            "\n<b>Federation:</b> {}"
            "\n<b>Federation Admin:</b> {}"
            "\n<b>User:</b> {}"
            "\n<b>User ID:</b> <code>{}</code>".format(
                info["fname"],
                f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                user_target,
                fban_user_id,
            ),
            parse_mode="HTML",
        )
        # Send message to owner if fednotif is enabled
        if getfednotif:
            try:
                await tbot.send_message(
                    int(info["owner"]),
                    "<b>Un-FedBan</b>"
                    "\n<b>Federation:</b> {}"
                    "\n<b>Federation Admin:</b> {}"
                    "\n<b>User:</b> {}"
                    "\n<b>User ID:</b> <code>{}</code>".format(
                        info["fname"],
                        f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                        user_target,
                        fban_user_id,
                    ),
                    parse_mode="HTML",
                )
            except Exception as e:
                print(e)
                pass
        # If fedlog is set, then send message, except fedlog is current chat
        get_fedlog = sql.get_fed_log(fed_id)
        if get_fedlog:
            if int(get_fedlog) != int(chat):
                try:
                    await tbot.send_message(
                        int(get_fedlog),
                        "<b>Un-FedBan</b>"
                        "\n<b>Federation:</b> {}"
                        "\n<b>Federation Admin:</b> {}"
                        "\n<b>User:</b> {}"
                        "\n<b>User ID:</b> <code>{}</code>".format(
                            info["fname"],
                            f"<p><a href='tg://user?id={user.id}'>{user.first_name}</a></p>",
                            user_target,
                            fban_user_id,
                        ),
                        parse_mode="HTML",
                    )
                except Exception as e:
                    print(e)
                    pass
        unfbanned_in_chats = 0
        for fedchats in chat_list:
            unfbanned_in_chats += 1

        try:
            x = sql.un_fban_user(fed_id, user_id)
            if not x:
                await event.reply(
                    "Un-fban failed, this user may already be un-fedbanned!"
                )
                return
        except:
            pass

        if unfbanned_in_chats == 0:
            await event.reply("This person has been un-fbanned in 0 chats.")
        if unfbanned_in_chats > 0:
            await event.reply(
                "This person has been un-fbanned in {} chats.".format(
                    unfbanned_in_chats
                )
            )
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/setfedlog (.*)"))
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fedinfo = sql.get_fed_info(args)
            if not fedinfo:
                await event.reply("This Federation does not exist!")
                return
            isowner = is_user_fed_owner(args, user.id)
            if not isowner:
                await event.reply("Only federation creator can set federation logs.")
                return
            setlog = sql.set_fed_log(args, chat)
            if setlog:
                await event.reply(
                    "Federation log `{}` has been set to {}".format(
                        fedinfo["fname"], event.chat.title
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/unsetfedlog (.*)"))
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fedinfo = sql.get_fed_info(args)
            if not fedinfo:
                await event.reply("This Federation does not exist!")
                return
            isowner = is_user_fed_owner(args, user.id)
            if not isowner:
                await event.reply("Only federation creator can set federation logs.")
                return
            setlog = sql.set_fed_log(args, None)
            if setlog:
                await event.reply(
                    "Federation log `{}` has been revoked on {}".format(
                        fedinfo["fname"], event.chat.title
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/fedsubs$"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        try:
            getmy = sql.get_mysubs(fed_id)
        except:
            getmy = []

        if len(getmy) == 0:
            await event.reply(
                "Federation `{}` is not subscribing any federation.".format(
                    fedinfo["fname"]
                ),
                parse_mode="markdown",
            )
            return
        else:
            listfed = "Federation `{}` is subscribing federation:\n".format(
                fedinfo["fname"]
            )
            for x in getmy:
                listfed += "- `{}`\n".format(x)
            listfed += "\nTo get fed info `/fedinfo <fedid>`. To unsubscribe `/unsubfed <fedid>`."
            await event.reply(listfed, parse_mode="markdown")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/myfeds$"))
async def _(event):
    try:
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        fedowner = sql.get_user_owner_fed_full(user.id)
        if fedowner:
            text = "**You are owner of feds:\n\n**"
            for f in fedowner:
                text += "- **{}**: `{}`\n".format(f["fed"]["fname"], f["fed_id"])
        else:
            text = "**You don't have any feds !**"
        await event.reply(text, parse_mode="markdown")

    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/fbanlist$"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return

        getfban = sql.get_all_fban_users(fed_id)
        if len(getfban) == 0:
            await event.reply(
                "The federation ban list of {} is empty".format(info["fname"]),
                parse_mode="html",
            )
            return

        text = "<b>{} users have been banned from the federation {}:</b>\n".format(
            len(getfban), info["fname"]
        )
        for users in getfban:
            getuserinfo = sql.get_all_fban_users_target(fed_id, users)
            if getuserinfo is False:
                text = "There are no users banned from the federation {}".format(
                    info["fname"]
                )
                break
            user_name = getuserinfo["first_name"]
            if not getuserinfo["last_name"] is None:
                user_name += " " + getuserinfo["last_name"]
            text += " • {} (<code>{}</code>)\n".format(
                f"<p><a href='tg://user?id={users}'>{user_name}</a></p>", users
            )
        try:
            await event.reply(text, parse_mode="html")
        except:
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can back up data once every 30 minutes!\nYou can back up data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            cleanr = re.compile("<.*?>")
            cleantext = re.sub(cleanr, "", text)
            with BytesIO(str.encode(cleantext)) as output:
                output.name = "fbanlist.txt"
                await tbot.send_file(
                    event.chat_id,
                    file=output,
                    filename="fbanlist.txt",
                    caption="The following is a list of users who are currently fbanned in the Federation {}.".format(
                        info["fname"]
                    ),
                )
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/exportfbans$"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        chat_data = {}
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return
        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return
        getfban = sql.get_all_fban_users(fed_id)
        if len(getfban) == 0:
            await event.reply(
                "The federation ban list of {} is empty".format(info["fname"]),
                parse_mode="html",
            )
            return
        args = True
        if args:
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can backup your data once every 30 minutes!\nYou can back up data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            backups = ""
            for users in getfban:
                getuserinfo = sql.get_all_fban_users_target(fed_id, users)
                json_parser = {
                    "user_id": users,
                    "first_name": getuserinfo["first_name"],
                    "last_name": getuserinfo["last_name"],
                    "user_name": getuserinfo["user_name"],
                    "reason": getuserinfo["reason"],
                }
                backups += json.dumps(json_parser)
                backups += "\n"
            with BytesIO(str.encode(backups)) as output:
                output.name = "julia_fbanned_users.json"
                await tbot.send_file(
                    event.chat_id,
                    file=output,
                    filename="julia_fbanned_users.json",
                    caption="Total {} users are blocked by the Federation {}.".format(
                        len(getfban), info["fname"]
                    ),
                )
            return
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/subfed ?(.*)"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)
        if args == fed_id:
            await event.reply("You cannot subscribe a federation to it's own")
            return

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        if args:
            getfed = sql.search_fed_by_id(args)
            if getfed is False:
                await event.reply("Please enter a valid federation id.")
                return
            subfed = sql.subs_fed(args, fed_id)
            if subfed:
                await event.reply(
                    "Federation `{}` has subscribed the federation `{}`. Every time there is a Fedban from that federation, this federation will also ban that user.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
                get_fedlog = sql.get_fed_log(args)
                if get_fedlog:
                    if int(get_fedlog) != int(chat):
                        try:
                            await tbot.send_message(
                                int(get_fedlog),
                                "Federation `{}` has subscribed the federation `{}`".format(
                                    fedinfo["fname"], getfed["fname"]
                                ),
                                parse_mode="markdown",
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply(
                    "Federation `{}` already subscribed the federation `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/unsubfed ?(.*)"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        fedinfo = sql.get_fed_info(fed_id)
        if args == fed_id:
            await event.reply("You cannot unsubscribe a federation to it's own")
            return

        if not fed_id:
            await event.reply("This group is not in any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only fed owner can do this!")
            return

        if args:
            getfed = sql.search_fed_by_id(args)
            if getfed is False:
                await event.reply("Please enter a valid federation id.")
                return
            subfed = sql.unsubs_fed(args, fed_id)
            if subfed:
                await event.reply(
                    "Federation `{}` now unsubscribe fed `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
                get_fedlog = sql.get_fed_log(args)
                if get_fedlog:
                    if int(get_fedlog) != int(chat):
                        try:
                            await tbot.send_message(
                                int(get_fedlog),
                                "Federation `{}` has unsubscribed fed `{}`.".format(
                                    fedinfo["fname"], getfed["fname"]
                                ),
                                parse_mode="markdown",
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply(
                    "Federation `{}` is not subscribed to `{}`.".format(
                        fedinfo["fname"], getfed["fname"]
                    ),
                    parse_mode="markdown",
                )
        else:
            await event.reply("You have not provided your federated ID!")
    except Exception as e:
        print(e)
        pass


@tbot.on(events.NewMessage(pattern="^/fedbroadcast ?(.*)"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        args = event.pattern_match.group(1)
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        if args:
            fed_id = sql.get_fed_id(chat)
            fedinfo = sql.get_fed_info(fed_id)
            if is_user_fed_owner(fed_id, user.id) is False:
                await event.reply("Only federation owners can do this!")
                return
            text = args
            try:
                broadcaster = user.first_name + " " + user.last_name
            except:
                broadcaster = user.first_name
            text += f"\n\n- [{broadcaster}](tg://user?id={user.id})"
            chat_list = sql.all_fed_chats(fed_id)
            failed = 0
            for chat in chat_list:
                title = "**New broadcast from Fed {}**\n\n".format(fedinfo["fname"])
                try:
                    await tbot.send_message(
                        int(chat), title + text, parse_mode="markdown"
                    )
                except Exception as e:
                    sql.chat_leave_fed(chat)
                    failed += 1
                    print(e)
                    pass

            send_text = "The federation broadcast is complete\n"
            if failed >= 1:
                send_text += "{} groups failed to receive the message.".format(failed)
            await event.reply(send_text)
    except Exception as e:
        print(e)
        pass


@register(pattern="^/fednotif ?(.*)")
async def _(event):
    try:
        chat = event.chat_id
        args = event.pattern_match.group(1)
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        fed_id = sql.get_fed_id(chat)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if args:
            if args == "on":
                sql.set_feds_setting(user.id, True)
                await event.reply(
                    "Reporting Federation back up! Every user who is fban / unfban you will be notified via PM."
                )
            elif args == "off":
                sql.set_feds_setting(user.id, False)
                await event.reply(
                    "Reporting Federation has stopped! Every user who is fban / unfban you will not be notified via PM."
                )
            else:
                await event.reply("Please enter `on`/`off`", parse_mode="markdown")
        else:
            getreport = sql.user_feds_report(user.id)
            await event.reply(
                "Your current Federation report preferences: `{}`".format(getreport),
                parse_mode="markdown",
            )
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern="^/fedchats$"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_admin(fed_id, user.id) is False:
            await event.reply("Only federation admins can do this!")
            return

        getlist = sql.all_fed_chats(fed_id)
        if len(getlist) == 0:
            await event.reply(
                "No chats are joined to the federation **{}**".format(info["fname"]),
                parse_mode="html",
            )
            return

        text = "<b>Here is the list of chats connected to {}:</b>\n\n".format(
            info["fname"]
        )
        for chats in getlist:
            text += " • <code>{}</code>\n".format(chats)
        try:
            await event.reply(text, parse_mode="html")
        except:
            cleanr = re.compile("<.*?>")
            cleantext = re.sub(cleanr, "", text)
            with BytesIO(str.encode(cleantext)) as output:
                output.name = "fedchats.txt"
                await tbot.send_file(
                    file=output,
                    filename="fedchats.txt",
                    caption="Here is a list of all the chats that joined the federation **{}**".format(
                        info["fname"]
                    ),
                )
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern="^/importfbans$"))
async def _(event):
    try:
        chat = event.chat_id
        user = event.sender
        chat_data = {}
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        if event.is_private:
            await event.reply("This command is specific to the group, not to my pm !")
            return

        fed_id = sql.get_fed_id(chat)
        info = sql.get_fed_info(fed_id)
        getfed = sql.get_fed_info(fed_id)

        if not fed_id:
            await event.reply("This group is not a part of any federation!")
            return

        if is_user_fed_owner(fed_id, user.id) is False:
            await event.reply("Only Federation owners can do this!")
            return

        if event.reply_to_msg_id:
            op = await event.get_reply_message()
            try:
                op.media.document
            except Exception:
                await event.reply("Thats not a file.")
                return
            h = op.media
            try:
                k = h.document.attributes
            except Exception:
                await event.reply("Thats not a file.")
                return
            if not isinstance(h, MessageMediaDocument):
                await event.reply("Thats not a file.")
                return
            if not isinstance(k[0], DocumentAttributeFilename):
                await event.reply("Thats not a file.")
                return
            jam = time.time()
            new_jam = jam + 1800
            cek = get_chat(chat, chat_data)
            if cek.get("status"):
                if jam <= int(cek.get("value")):
                    waktu = time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(cek.get("value"))
                    )
                    await event.reply(
                        "You can import your data once every 30 minutes!\nYou can get data again at `{}`".format(
                            waktu
                        ),
                        parse_mode="markdown",
                    )
                    return
                else:
                    if user.id != OWNER_ID:
                        put_chat(chat, new_jam, chat_data)
            else:
                if user.id != OWNER_ID:
                    put_chat(chat, new_jam, chat_data)
            success = 0
            failed = 0
            fileformat = op.file.name.split(".")[-1]
            if fileformat == "json":
                try:
                    file_info = await tbot.download_file(op, op.file.name)
                except Exception:
                    await event.reply(
                        "Try downloading and re-uploading the file, this one seems broken!"
                    )
                    return
                multi_fed_id = []
                multi_import_userid = []
                multi_import_firstname = []
                multi_import_lastname = []
                multi_import_username = []
                multi_import_reason = []
                with open(op.file.name) as file:
                    file.seek(0)
                    reading = file.read()
                    splitting = reading.split("\n")
                    for x in splitting:
                        if x == "":
                            continue
                        try:
                            data = json.loads(x)
                        except json.decoder.JSONDecodeError as err:
                            failed += 1
                            continue
                        try:
                            import_userid = int(data["user_id"])  # Make sure it int
                            import_firstname = str(data["first_name"])
                            import_lastname = str(data["last_name"])
                            import_username = str(data["user_name"])
                            import_reason = str(data["reason"])
                        except ValueError:
                            failed += 1
                            continue
                        # Checking user
                        if int(import_userid) == BOT_ID:
                            failed += 1
                            continue
                        if is_user_fed_owner(fed_id, import_userid) is True:
                            failed += 1
                            continue
                        if is_user_fed_admin(fed_id, import_userid) is True:
                            failed += 1
                            continue
                        if str(import_userid) == str(OWNER_ID):
                            failed += 1
                            continue
                        multi_fed_id.append(fed_id)
                        multi_import_userid.append(str(import_userid))
                        multi_import_firstname.append(import_firstname)
                        multi_import_lastname.append(import_lastname)
                        multi_import_username.append(import_username)
                        multi_import_reason.append(import_reason)
                        success += 1
                    sql.multi_fban_user(
                        multi_fed_id,
                        multi_import_userid,
                        multi_import_firstname,
                        multi_import_lastname,
                        multi_import_username,
                        multi_import_reason,
                    )
                text = "Blocks were successfully imported.\n`{}` people are blocked.".format(
                    success
                )
                if failed >= 1:
                    text += " {} Failed to import.".format(failed)
                get_fedlog = sql.get_fed_log(fed_id)
                if get_fedlog:
                    if eval(get_fedlog):
                        teks = "Fed **{}** has successfully imported data.\n{} banned.".format(
                            getfed["fname"], success
                        )
                        if failed >= 1:
                            teks += " {} Failed to import.".format(failed)
                        try:
                            await tbot.send_message(
                                int(get_fedlog), teks, parse_mode="markdown"
                            )
                        except Exception as e:
                            print(e)
                            pass
            else:
                await event.reply("This file is not supported.")
                return
            await event.reply(text)
            os.remove(op.file.name)
        else:
            await event.reply("Reply to the backup(export) file to import it.")
            return
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern="^/fbanstat ?(.*)"))
async def _(event):
    try:
        # chat = event.chat_id
        user = event.sender
        if event.is_group:
            if await is_register_admin(event.input_chat, event.sender_id):
                pass
            else:
                return
        args = event.pattern_match.group(1)
        if args:
            userid = args
            if args.isdigit():
                user_idd = args
                user_iddd = await tbot.get_input_entity(int(user_idd))
                user_id = user_iddd.user_id
            else:
                user_idd = args
                user_iddd = await tbot.get_input_entity(user_idd)
                user_id = user_iddd.user_id
            if not user_id:
                await event.reply("Please enter a valid user id.")
                return
            if user_id:
                user_name, fbanlist = sql.get_user_fbanlist(str(user_id))
                if user_name == "":
                    try:
                        user_namee = await tbot.get_entity(int(user_id))
                        user_name = user_namee.first_name
                    except Exception:
                        user_name = "He/she"
                    if user_name == "" or user_name is None:
                        user_name = "He/she"
                if len(fbanlist) == 0:
                    await event.reply(
                        "**{}** is not banned in any federation!".format(user_name),
                    )
                    return
                else:
                    teks = "**{}** has been banned in these federations:\n\n".format(
                        user_name
                    )
                    for x in fbanlist:
                        teks += "- `{}`: {}\n".format(x[0], x[1][:20])
                    await event.reply(teks, parse_mode="markdown")
        else:
            await event.reply("Syntax: `/fbanstat <userid/entity>`")
            return
    except Exception as e:
        print(e)


# Temporary data
def put_chat(chat_id, value, chat_data):
    # print(chat_data)
    if value is False:
        status = False
    else:
        status = True
    chat_data[chat_id] = {"federation": {"status": status, "value": value}}


def get_chat(chat_id, chat_data):
    # print(chat_data)
    try:
        value = chat_data[chat_id]["federation"]
        return value
    except KeyError:
        return {"status": False, "value": False}


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /newfed <fed_name>: Creates a Federation, one allowed per user.
 - /renamefed <fed_id> <new_fed_name>: Renames the fed id to a new name.
 - /delfed <fed_id>: Delete a Federation, and any information related to it. 
 - /fpromote <user>: Assigns the user as a federation admin. 
 - /fdemote <user>: Drops the user from the federation admin to a normal user.
 - /subfed <fed_id>: Subscribes to a given fed ID, fedbans from that subscribed fed will also happen in your fed
 - /unsubfed <fed_id>: Unsubscribes to a given fed ID
 - /setfedlog <fed_id>: Sets the group as a fed log report base for the federation
 - /unsetfedlog <fed_id>: Removed the group as a fed log report base for the federation
 - /fbroadcast <message>: Broadcasts a messages to all groups that have joined your fed
 - /fedsubs: Shows the feds your group is subscribed to (broken rn)
 - /fban (<user>|<reason>): Fed bans a user. Syntax: `fban 12345 | testing`, `fban @MissJuliaRobot | testing`.
 - /unfban <user> <reason>: Removes a user from a fed ban.
 - /fedinfo <fed_id>: Information about the specified Federation.
 - /joinfed <fed_id>: Join the current chat to the Federation. 
 - /leavefed <fed_id>: Leave the Federation given. 
 - /setfrules <rules>: Arrange Federation rules.
 - /fedadmins: Show Federation admin.
 - /fbanlist: Displays all users who are victimized at the Federation at this time.
 - /fedchats: Get all the chats that are connected in the Federation.
 - /chatfed : See the Federation in the current chat.
 - /fbanstat: Shows if you/or the user you are replying to or their username/id is fbanned somewhere or not.
 - /fednotif <on/off>: Should the bot send notifications for fban/unfban in PM.
 - /frules: See the current federation rules.
 - /exportfbans: Returns a list of all banned users in the current federation.
 - /importfbans: Imports all fbanned uses from the export file into the current chat federation.

**NOTE**: Federation ban doesn't ban the user from the fed chats instead kicks everytime they join the chat.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
