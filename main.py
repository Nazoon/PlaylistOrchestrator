"""
Defines the bot's event listeners.
"""

import os
import discord
import shlex
from commands import COMMANDS, COMMAND_PREFIX


client = discord.Client()
bot_token = os.environ['bot_token']


def parse_command_args(message: discord.Message) -> list:
    """
    Given a discord message, split it into arg values.
    The first argument is always the command word, excluding the prefix.
    Arguments are split by quoted regions first, then by spaces.
    """
    assert message.content.startswith(COMMAND_PREFIX)
    return shlex.split(message.content[1:])


@client.event
async def on_ready():
    print(f'I am logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if not message.content.startswith(COMMAND_PREFIX):
        return
    args = parse_command_args(message)
    if args[0] in COMMANDS:
        await COMMANDS[args[0]](message, args)


if __name__ == '__main__':
    client.run(bot_token)
