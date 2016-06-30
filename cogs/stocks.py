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

default_stocks = {'NNTDO':40, 'NASLAQ':40, 'SNRLX':40, 'WTCHR':40,
                  'DSCRD':40, 'PYTHN':40, 'CRBDBX':40, '':40, }

class Stocks:
    def __init__(self, bot, file_path):
        self.stocks = dataIO.load_json(file_path)
        self.settings = dataIO.load_json('data/stocks/settings.json')
        self.bot = bot

    @commands.group(name="stocks", pass_context=True)
    async def _stocks(self, ctx):
        """Bank operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_stocks.command(pass_context=True, no_pm=True)
    async def buy(self, ctx, stock_name, amount):
        """Buy *amount* shares of *stock_name* stock"""
        user = ctx.message.author
        economy = self.bot.get_cog("Economy")
        bank = economy.bank if economy is not None

    @_stocks.command(pass_context=True, no_pm=True)
    async def sell(self, ctx, stock_name, amount):
        """Sell *amount* shares of *stock_name* stock"""
        user = ctx.message.author
        economy = self.bot.get_cog("Economy")
        bank = economy.bank if economy is not None

    def update_stock_prices(self):
        for key, value in default_stocks.items():
            default_stocks[key] = value#TODO


def check_folders():
    if not os.path.exists("data/economy"):
        print("Creating data/economy folder...")
        os.makedirs("data/economy")

def check_files():

    f = "data/economy/settings.json"
    if not fileIO(f, "check"):
        print("Creating default economy's settings.json...")
        fileIO(f, "save", {})

    f = "data/economy/bank.json"
    if not fileIO(f, "check"):
        print("Creating empty bank.json...")
        fileIO(f, "save", {})

def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("red.economy")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/economy/economy.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Economy(bot))
