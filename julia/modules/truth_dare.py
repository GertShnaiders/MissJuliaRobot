from random import randint
from PIL import ImageEnhance, ImageOps
from random import uniform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import asyncio
from julia import OWNER_ID
from julia import SUDO_USERS
import io
import os
import random
import re
import string
import nltk
import bs4
import requests
from PIL import Image
from zalgo_text import zalgo
from julia.events import register
import json
import subprocess
import textwrap
import urllib.request
from random import randrange
from typing import List
from typing import Optional
import emoji
from cowpy import cow
from fontTools.ttLib import TTFont
from PIL import ImageDraw
from PIL import ImageFont
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl.types import *
from julia import *
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
import time
from datetime import datetime
WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000


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


TRUTH = (
    "Have you ghosted someone?" "Have you ever walked in on your parents doing 'it'?",
    "Who was the last person you liked the most? Why?",
    "Have you ever been suspended from school?",
    "If you had to choose between going naked or having your thoughts appear in thought bubbles above your head for everyone to read, which would you choose?",
    "What’s the one thing you’re afraid to lose?",
    "Do you like someone as of the moment?",
    "One thing about your best friend you are jealous of?",
    "Would you cheat on your boyfriend for a rich guy?",
    "What is your biggest turn on?",
    "When’s the last time you lied to your parents and why?",
    "Describe your ideal partner.",
    "What’s the scariest thing you’ve ever done?",
    "Have you ever picked your nose and eaten it?",
    "When’s the last time you lied to your parents and why?",
    "Did you ever tried to book a girlfriend online?",
    "After watching rent a girlfriend did u also got interest im gf booking online?",
    "Have you ever lied about your age to participate in a contest?",
    "Have you ever been caught checking someone out?",
)

DARE = (
    "Show the most embarrassing photo on your phone"
    "Show the last five people you texted and what the messages said",
    "Let the rest of the group DM someone from your Instagram account",
    "Eat a raw piece of garlic",
    "Do 100 squats",
    "Keep three ice cubes in your mouth until they melt",
    "Say something dirty to the person on your leftYou've got company!",
    "Give a foot massage to the person on your right",
    "Put 10 different available liquids into a cup and drink it",
    "*Yell out the first word that comes to your mind",
    "Give a lap dance to someone of your choice",
    "Remove four items of clothing",
    "Like the first 15 posts on your Facebook newsfeed",
    "Eat a spoonful of mustard",
    "Keep your eyes closed until it's your go again",
    "Send a sext to the last person in your phonebook",
    "Show off your orgasm face",
    "Seductively eat a banana",
    "Empty out your wallet/purse and show everyone what's inside",
    "Do your best sexy crawl",
    "Pretend to be the person to your right for 10 minutes",
    "Eat a snack without using your hands",
    "Say two honest things about everyone else in the group",
    "Twerk for a minute",
    "Try and make the group laugh as quickly as possible",
    "Try to put your whole fist in your mouth",
    "Tell everyone an embarrassing story about yourself",
    "Try to lick your elbow",
    "Post the oldest selfie on your phone on Instagram Stories",
    "Tell the saddest story you know",
    "Howl like a wolf for two minutes",
    "Dance without music for two minutes",
    "Pole dance with an imaginary pole",
    "Let someone else tickle you and try not to laugh",
    "Put as many snacks into your mouth at once as you can",
    "Send your most recent selfie.",
    "Send your ugliest selfie.",
    "Send a screenshot of your facebook search history",
    "Send a screenshot of your gallery.",
    "Send a screenshot of your messenger inbox",
    "Tell something very intimate.",
    "Send a screenshot of your twitter inbox",
    "Send a screenshot of your homescreen.",
    "Send a cover of your favorite song. 🎤",
    "Do a lyric prank on someone and send proof.",
    "Confess to your current crush. ❤️",
    "Declare who is your true love.",
    "Send a screenshot of your gallery.",
    "Did you love your neighbour daughter.",
    "Set your crush’s picture as your dp.",
    "Suggest me more dares.",
)
GAND = (
    "GAND successfully Blocked🤔🤔b",
)

@register(pattern="^/truth$")
async def msg(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    await event.reply(random.choice(TRUTH))

@register(pattern="^/dare$")
async def msg(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    await event.reply(random.choice(DARE))
CC = (
    "#LIVE ◈ 5124874660020502|07|2023|830 ◈ 「Approved (͏CVV) [BlackStone",
    "#LIVE ◈ 5124874668322108|12|2022|387 ◈ 「Approved (͏CVV) [BlackStone]」 ◈",
    "#LIVE ◈ 5124874668825381|08|2022|640 ◈ 「Approved (͏CVV) [BlackStone]」 ◈",
    "#LIVE ◈ 5124874660078823|05|2025|141 ◈ 「Approved (͏CVV) [BlackStone]」 ◈",
    "#LIVE ◈ 5124874662664166|02|2025|034 ◈ 「Approved (͏CVV) [BlackStone]」 ◈",
)

@register(pattern="^/livecc$")
async def msg(event):
    if event.sender_id in SUDO_USERS:
        pass
    elif event.sender_id == OWNER_ID:
        pass
    elif event.sender_id not in SUDO_USERS:
        await event.reply("Baag Ja Mewederchod Free Cc only for SuDos😑.")
        return
    else:
        return
    await event.reply(random.choice(CC))
