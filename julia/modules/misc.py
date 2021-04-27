from julia import tbot
from julia.events import register

from telethon import version
from math import ceil
import json
import random
import re
from telethon import events, errors, custom
import io
from platform import python_version, uname 
import os
import time
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins




@register(pattern="^/wish (.*)")
async def wish_check(event):
    wishtxt = event.pattern_match.group(1)
    chance = random.randint(0, 100)
    if wishtxt:
        reslt = f"**Your wish **__{wishtxt}__ **has been cast.** ✨\
              \n\n__Chance of success :__ **{chance}%**"
    else:
        if event.is_reply:
            reslt = f"**Your wish has been cast. **✨\
                  \n\n__Chance of success :__ **{chance}%**"
        else:
            reslt = f"Make A Wish."
    await event.reply(reslt)
