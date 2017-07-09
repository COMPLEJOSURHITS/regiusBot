import asyncio
import statistics
from time import gmtime, strftime

import discord
from discord import Game, Server, Member

import functions
import SECRETS
import STATICS
from commands import cmd_start, cmd_restart, cmd_invite, cmd_google, cmd_log, cmd_dev, cmd_test, cmd_prefix, cmd_dnd, \
    cmd_github, cmd_say, cmd_pmbc


client = discord.Client()

cmdmap = {
            "lmgtfy": cmd_google,
            "invite": cmd_invite,
            "log": cmd_log,
            "restart": cmd_restart,
            "start": cmd_start,
            "dev": cmd_dev,
            "prefix": cmd_prefix,
            "dnd": cmd_dnd,
            "afk": cmd_dnd,
            "github": cmd_github,
            "git": cmd_github,
            "say": cmd_say,
            "test": cmd_test,
            "pmbc": cmd_pmbc,
        }


# LISTENER

@client.event
@asyncio.coroutine
def on_ready():
    print("BOT STARTED\n-----------------")
    yield from client.change_presence(game=Game(name=functions.get_members_msg(client)))
    statistics.server = list(client.servers)[0]
    statistics.start()


@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.change_presence(game=Game(name=functions.get_members_msg(client)))
    yield from functions.send_join_pm(member, client)


@client.event
@asyncio.coroutine
def on_member_remove(member):
    yield from client.change_presence(game=Game(name=functions.get_members_msg(client)))


@client.event
@asyncio.coroutine
def on_member_update(before, after):
    yield from client.change_presence(game=Game(name=functions.get_members_msg(client)))
    yield from cmd_dnd.check_status(before, after, client)


@client.event
@asyncio.coroutine
def on_message(message):
    yield from cmd_dnd.test(message, client)
    if message.content.startswith(STATICS.PREFIX):
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        invoke = message.content.split(" ")[0].replace(STATICS.PREFIX, "", 1)
        command_string = ""
        if invoke == "help":
            for s in cmdmap.keys():
                command_string += ":white_small_square:  **" + s + "**  -  `" + cmdmap.get(s).description + "`\n"
            yield from client.send_message(message.author, STATICS.helpText + command_string)
        else:
            yield from cmdmap.get(invoke).ex(message, client)


client.run(SECRETS.token)
