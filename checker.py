import urllib.request as urllib2
import discord
import platform
import os
from colorama import Fore
import sys
from bs4 import BeautifulSoup
import urllib.request
import datetime
import json
from discord.ext import commands

categories = open('categories.txt').read().splitlines()

x = datetime.datetime.now()

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again!")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents().all()

astral = commands.Bot(command_prefix=config["prefix"], intents=intents)


@astral.event
async def on_ready():
    print("-------------------")
    print(Fore.BLUE + (f"Logged in as {astral.user}"))
    print(Fore.RED + (f"Discord.py API version: {discord.__version__}"))
    print(Fore.CYAN + (f"Python version: {platform.python_version()}"))
    print(Fore.GREEN + (f"Running on: {platform.system()} {platform.release()} ({os.name})"))
    print("-------------------")


@astral.event
async def on_message(message):
    if message.author == astral.user or message.author.bot:
        return
    await astral.process_commands(message)


@astral.event
async def on_command_error(ctx, error):
    await ctx.send("An error has occured. Please ask the bot owner to check their command prompt for a detailed stacktrace. Sorry for the inconvenience!")
    raise error

@astral.command()
async def check(ctx):

    await ctx.message.attachments[0].save(f"{ctx.author.name}.txt")

    links = open(f"{ctx.author.name}.txt").read().splitlines()

    for url in links:

        print(url)

        requestURL = "https://archive.lightspeedsystems.com/SubmitDomain.php?Domain=" + url

        opener = urllib.request.FancyURLopener({})

        f = opener.open(requestURL)

        content = f.read()

        blocked = False
    
        with open("tempFile.txt", "w") as f:

            f.write(BeautifulSoup(str(content), 'html.parser').prettify())

            f.close()


        with open("tempFile.txt","r") as f:

            for l in f:

                for i in categories:

                    if i in l:

                        await ctx.send(f"{url} is blocked for {i}.")

                        blocked = True

                        break
            
  

            if blocked != True:

                await ctx.send(f"{url} is not blocked.")


            f.close()

            os.remove("tempFile.txt")


astral.run(config["token"])