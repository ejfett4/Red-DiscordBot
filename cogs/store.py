import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO, fileIO
from collections import namedtuple, defaultdict
from datetime import datetime
from random import randint
from copy import deepcopy
from .view import StringView
from .utils import checks
from __main__ import send_cmd_help
import os
import time
import logging
import itertools

class Store:
    def __init__(self, bot, file_path):
        self.costs = dataIO.load_json(file_path)
        self.settings = fileIO("data/store/settings.json", "load")
        self.bot = bot
        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200bNo Category:'

        data = sorted(self.bot.formatter.filter_command_list(), key=category)
        for category, commands in itertools.groupby(data, key=category):
            for command in commands:
                if command[0] not in self.costs:
                    self.costs[command[0]] = 0
        self._save_store()

    def _save_store(self):
        dataIO.save_json("data/store/costs.json", self.costs)

    @commands.group(name="store", pass_context=True)
    async def _store(self, ctx):
        """Store operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_store.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def setcost(self, ctx, cmd : str, sum : int):
        author = ctx.message.author
        server = author.server
        if cmd in self.costs:
            if sum > -1:
                self.costs[cmd] = sum
                self._save_store()
        else:
            await self.bot.say("{0} is not a command in the store!".format(cmd))

    @_store.command()
    async def getcost(self, ctx, cmd : str):
        if cmd in self.costs:
            await self.bot.say("{0} costs {1}".format(cmd, self.costs[cmd]))
        else:
            await self.bot.say("{0} is not a command in the store!".format(cmd))

@bot.check
def has_moneys(ctx):
    economy = ctx.bot.get_cog("economy")
    bank = economy.bank
    message = ctx.message
    author = message.author
    prefix = ctx.bot.command_prefix
    cmd_and_prefix = message.content.strip().split(' ')[0]
    cmd = cmd_and_prefix.replace(prefix, "")
    if bank.account_exists(author):
        if cmd in self.costs:
            cost = self.costs[cmd]
            return bank.can_spend(author, cost)
        else:
            return False
    else:
        return False

@bot.listen
async def on_command(command, ctx):
    economy = ctx.bot.get_cog("economy")
    author = ctx.message.author
    server = author.server
    cmd = command.name
    if cmd in self.costs:
        economy.bank.withdraw_credits(author, cmd)

def check_folders():
    if not os.path.exists("data/store"):
        print("Creating data/store folder...")
        os.makedirs("data/store")

def check_files():

    f = "data/store/settings.json"
    if not fileIO(f, "check"):
        print("Creating default store's settings.json...")
        fileIO(f, "save", {})

    f = "data/store/costs.json"
    if not fileIO(f, "check"):
        print("Creating empty costs.json...")
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
    bot.add_cog(Store(bot, "data/store/costs.json"))
