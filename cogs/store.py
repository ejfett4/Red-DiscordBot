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
    def __init__(self, bot):
        self.bot = bot
        self.costs = dataIO.load_json('data/store/costs.json')
        self.settings = fileIO("data/store/settings.json", "load")

    def _save_store(self):
        dataIO.save_json("data/store/costs.json", self.costs)

    def getcosts(self):
        return self.costs

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
        if sum > -1:
            self.costs[cmd] = sum
            self._save_store()
            await self.bot.say("{0} now costs {1}".format(cmd, self.costs[cmd]))
        else:
            await self.bot.say("{0} can't be negative".format(sum))

    @_store.command()
    async def getcost(self, cmd : str):
        if cmd in self.costs:
            await self.bot.say("{0} costs {1}".format(cmd, self.costs[cmd]))
        else:
            await self.bot.say("{0} is not a command in the store!".format(cmd))

def has_moneys(ctx):
    economy = ctx.bot.get_cog("Economy")
    store = ctx.bot.get_cog("Store")
    bank = economy.bank
    message = ctx.message
    author = message.author
    prefix = ctx.bot.command_prefix
    cmd_and_prefix = message.content.strip().split(' ')[0]
    cmd = cmd_and_prefix.replace(prefix[0], "")
    if store is not None:
        if bank.account_exists(author):
            if cmd in store.getcosts():
                cost = store.getcosts()[cmd]
                return bank.can_spend(author, cost)
    else:
        return True

async def on_command(command, ctx):
    economy = ctx.bot.get_cog("Economy")
    store = ctx.bot.get_cog("Store")
    author = ctx.message.author
    server = author.server
    cmd = command.name
    if store is not None:
        if cmd in store.getcosts():
            economy.bank.withdraw_credits(author, store.getcosts()[cmd])
    pass

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
    #bot.add_check(has_moneys)
    bot.add_listener(on_command)
    bot.add_cog(Store(bot))
