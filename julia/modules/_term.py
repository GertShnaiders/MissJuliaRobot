from julia import tbot
import asyncio
from getpass import getuser
from os import remove

from julia import OWNER_ID
from julia.events import register


@register(pattern="^/term(?: |$)(.*)")
async def terminal_runner(term):
    check = term.message.sender_id
    if int(check) != int(OWNER_ID):
        return
    curruser = getuser()
    command = term.pattern_match.group(1)
    try:
        from os import geteuid

        uid = geteuid()
    except ImportError:
        uid = "This ain't it chief!"

    if term.is_channel and not term.is_group:
        await term.reply("`Term commands aren't permitted on channels!`")
        return

    if not command:
        return

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

    if len(result) > 4096:
        output = open("output.txt", "w+")
        output.write(result)
        output.close()
        await tbot.send_file(
            term.chat_id,
            "output.txt",
            reply_to=term.id,
            caption="`Output too large, sending as file`",
        )
        remove("output.txt")
        return

    if uid == 0:
        await term.reply("`" f"{curruser}:~# {command}" f"\n{result}" "`")
    else:
        await term.reply("`" f"{curruser}:~$ {command}" f"\n{result}" "`")
