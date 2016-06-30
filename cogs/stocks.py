import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO, fileIO
from collections import namedtuple, defaultdict
from datetime import datetime
from random import randint, random
from copy import deepcopy
from .utils import checks
from __main__ import send_cmd_help
import os
import time
import logging

default_stocks = {'NNTDO': {'price':40, 'bought':0, 'sold':0},
                  'NASLAQ':{'price':40, 'bought':0, 'sold':0},
                  'SNRLX': {'price':40, 'bought':0, 'sold':0},
                  'WTCHR': {'price':40, 'bought':0, 'sold':0},
                  'DSCRD': {'price':40, 'bought':0, 'sold':0},
                  'PYTHN': {'price':40, 'bought':0, 'sold':0},
                  'CRBDBX':{'price':40, 'bought':0, 'sold':0},
                  'SNY':   {'price':40, 'bought':0, 'sold':0},
                  'CSHMNY':{'price':40, 'bought':0, 'sold':0},
                  'MCRSFT':{'price':40, 'bought':0, 'sold':0},
                  'SNK':   {'price':40, 'bought':0, 'sold':0},
                  'DRG':   {'price':40, 'bought':0, 'sold':0}}

class Stocks:
    def __init__(self, bot):
        self.stocks = dataIO.load_json('data/stocks/stocks.json')
        if not self.stocks:
            self.stocks = default_stocks
        self.portfolios = dataIO.load_json('data/stocks/portfolios.json')
        self.bot = bot

    @commands.group(name="stocks", pass_context=True)
    async def _stocks(self, ctx):
        """Stock operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_stocks.command(pass_context=True, no_pm=True)
    async def buy(self, ctx, stock_name, amount):
        """Buy *amount* shares of *stock_name* stock"""
        user = ctx.message.author
        economy = self.bot.get_cog("Economy")
        if economy is not None:
            bank = economy.bank
            if user.id not in self.portfolios:
                self.portfolios[user.id] = {}
            if stock_name in self.stocks:
                if amount > 0:
                    cost = self.stocks[stock_name]['price'] * amount
                    if bank.can_spend(user, cost):
                        bank.withdraw_credits(user, cost)
                        self.portfolios[user.id][stock_name] += amount
                        dataIO.save_json('data/stocks/portfolios.json', self.portfolios)
                    else:
                        await self.bot.say("You don't have enough bank credits to purchase {0} of {1}".format(amount, stock_name))
                else:
                    await self.bot.say("You know better than to try to trick me")
            else:
                await self.bot.say("{0} isn't a valid stock".format(stock_name))
        else:
            await self.bot.say("Couldn't find the Economy cog, please load it before trying to use Stocks")


    @_stocks.command(pass_context=True, no_pm=True)
    async def sell(self, ctx, stock_name, amount):
        """Sell *amount* shares of *stock_name* stock"""
        user = ctx.message.author
        economy = self.bot.get_cog("Economy")
        if economy is not None:
            bank = economy.bank
            if user.id not in self.portfolios:
                self.portfolios[user.id] = {}
            if stock_name in self.stocks and stock_name in self.portfolios[user.id]:
                if amount > 0:
                    if self.portfolios[user.id][stock_name] >= amount:
                        price = self.stocks[stock_name]['price'] * amount
                        bank.deposit_credits(user, price)
                        self.portfolios[user.id][stock_name] -= amount
                        dataIO.save_json('data/stocks/portfolios.json', self.portfolios)
                    else:
                        await self.bot.say("You don't have enough {0} stocks to sell {1}".format(stock_name, amount))
                else:
                    await self.bot.say("You know better than to try to trick me")
            else:
                await self.bot.say("{0} isn't a valid stock or you don't have any".format(stock_name))
        else:
            await self.bot.say("Couldn't find the Economy cog, please load it before trying to use Stocks")

    @_stocks.command()
    @checks.admin_or_permissions(manage_server=True)
    async def update(self):
        """Force update stock prices"""
        self.update_stock_prices()

    def update_stock_prices(self):
        for key, value in stocks.items():
            self.stocks[key]['price'] = self.new_price(self.stocks[key])
        dataIO.save_json('data/stocks/stocks.json', self.stocks)

    def new_price(self, stock):
        net = (stock['bought'] - stock['sold'])
        total = stock['bought'] + stock['sold']
        if total == 0:
            total = net
        purchase_factor = (net / total) + 0.5
        random_factor = (random() + 0.5) / 2.0
        result_price = int(price * random_factor * purchase_factor)
        result_price = (random() * (result_price / 80)) > 0.95 ? 40 : result_price
        return result_price

    async def check_update_prices(self):
        while "Stocks" in self.bot.cogs:
            if datetime.now().time().hour == 8:
                self.update_stock_prices()
            await asyncio.sleep(3600)


def check_folders():
    if not os.path.exists("data/stocks"):
        print("Creating data/stocks folder...")
        os.makedirs("data/stocks")

def check_files():
    f = "'data/stocks/portfolios.json'"
    if not fileIO(f, "check"):
        print("Creating empty portfolios.json...")
        fileIO(f, "save", {})

    f = "data/stocks/stocks.json"
    if not fileIO(f, "check"):
        print("Creating empty stocks.json...")
        fileIO(f, "save", {})

def setup(bot):
    global logger
    check_folders()
    check_files()
    stockmarket = Stocks(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(stockmarket.check_update_prices())
    bot.add_cog(stockmarket)
