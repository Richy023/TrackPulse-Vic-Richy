from calendar import c
from math import e
from numbers import Number
import operator
from shutil import ExecError
import shutil
import sqlite3
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import asyncio
import threading
from datetime import datetime
import time
import csv
import random
from typing import Literal, Optional
import typing
from re import A
import traceback
import os
from pathlib import Path
import git
import pandas as pd
import builtins

import sys

from commands.NSWsearchtrain import NSWsearchTrainCommand
from commands.logger.logqldtrain import logQLDtrain
from commands.searchPhoto import searchTrainPhoto
from commands.searchtrain import searchTrainCommand
from commands.traintimleyfetcher import getchannelstocheck, seeWhereTrainsAre, trainTimleyFetcherAdd, trainTimleyFetcherList, trainTimleyFetcherRemove
from photosubmissions.manager import addSubmission, getUserID, removeSubmission, returnQueue
from utils.alias import setWebAlias
from utils.aviationAPIs.airportdata import get_airport_data
from utils.aviationAPIs.aircraftphoto import getplaneimage
from utils.game.imageadder import acceptGuesserPhoto
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import getTotalLines_pre_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_post_munnel import getTotalLines_post_munnel
from utils.trainlogger.map.line_coordinates_log_sydney_tram_map import getTotalLines_sydney_tram
from utils.vicrailphotosapi.accepter import acceptPhoto, webAddImage
sys.stdout = sys.__stdout__ 

original_open = builtins.open

# Commands imports
from commands.help import helpCommand
from commands.logexport import logExport

# Utils imports
from utils import healthcheck, trainset
from utils.directions import getDirectionName
from utils.downloader import downloader_function
from utils.favourites.viewer import *
from utils.search import *
from utils.colors import *
from utils.stationID import nameToStopID
from utils.stats.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *

# trainlogger imports
from utils.trainlogger.achievements.check import awardAchievement, checkAchievements, checkGameAchievements, checkHangmanAchievements, getAchievementInfo
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.mapimage import compress, legend
from utils.lines_dictionaries import *
from utils.trainlogger.achievements import *
from utils.trainlogger.graph import *

from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.locationFromNumber import *
from utils.photo import *
from utils.mykipython import *
from utils.myki.savelogin import *
from utils.special.yearinreview import *
from utils.stoppingpattern import *
from utils.locationfromid import *
from utils.stationDisruptions import *
from utils.stats.stats import *
from utils.vlineTrickery import getVlineStopType
import threading

print("""TrackPulse Vic Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

async def printlog(text):
    print(text)
    if len(str(text)) < 1000:
        log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
        await log_channel.send(text)

admin_users = [1002449671224041502, 780303451980038165, 634620519500480512, 581098452327464973, 637885403101396994, int(USER_ID)]
if config['DEVS_TO_HAVE_ADMIN_ACCESS'] == 'OFF':
    admin_users = [int(USER_ID)]

os.spawnl(os.P_NOWAIT, sys.executable, 'python', 'bot.py')

@bot.command()
async def megaping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to ms
    await ctx.send(f"Pong! Backup program operational! Latency: {latency} ms")
    log_command(ctx.author.id, 'ping')

@bot.command()
async def start(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'start')
        await ctx.send(f"Starting bot")
        await printlog("Starting bot")

        os.spawnl(os.P_NOWAIT, sys.executable, 'python', 'bot.py')

        await ctx.send(f"Started")
        await printlog("Started")

    else:
        await printlog(f'{str(ctx.author.id)} tried to start the bot.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def kill(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'kill')
        await ctx.send(f"Shutting down bot (for realsies)")
        await printlog("Shutting down bot (for realsies)")
        
        await bot.close()

    else:
        await printlog(f'{str(ctx.author.id)} tried to kill the bot.')
        await ctx.send("You are not authorized to use this command.")

# important
bot.run(BOT_TOKEN)