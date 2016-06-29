import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO, fileIO
from collections import namedtuple, defaultdict
from datetime import datetime
from random import randint
from copy import deepcopy
from .utils import checks
from __main__ import send_cmd_help
import os
import time
import logging
import itertools

class Store:
    def __init__(self, bot, file_path):
        self.cost_settings = dataIO.load_json(file_path)
        self.bot = bot


    def _save_bank(self):
        dataIO.save_json("data/store/cost_settings.json", self.cost_settings)

    def _get_account(self, user):
        server = user.server
        try:
            return deepcopy(self.accounts[server.id][user.id])
        except KeyError:
            raise NoAccount

    @commands.command(pass_context=True, no_pm=True)
    async def test(self, ctx):
        """Play the slot machine"""
        author = ctx.message.author
        server = author.server
        result = []

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200bNo Category:'

        data = sorted(self.bot.formatter.filter_command_list(), key=category)
        for category, commands in itertools.groupby(data, key=category):
            for command in commands:
                result.append(command[0])
        await self.bot.say("{0}".format(result))

def check_folders():
    if not os.path.exists("data/store"):
        print("Creating data/store folder...")
        os.makedirs("data/store")

def check_files():

    f = "data/store/settings.json"
    if not fileIO(f, "check"):
        print("Creating default store's settings.json...")
        fileIO(f, "save", {})

    f = "data/store/cost_settings.json"
    if not fileIO(f, "check"):
        print("Creating empty cost_settings.json...")
        fileIO(f, "save", {})

def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("red.store")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/store/store.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Store(bot, "data/store/cost_settings.json"))
