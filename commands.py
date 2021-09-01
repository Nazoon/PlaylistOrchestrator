"""
Defines this bot's commands.
"""

import discord
from random import choice
import playlist_service
import logging


COMMAND_PREFIX = '$'


async def ping(message: discord.Message, _):
    await message.channel.send('Pong!')


async def echo(message: discord.Message, args):
    await message.channel.send(' '.join(args[1:]))


async def list_playlists(message: discord.Message, _):
    playlists = playlist_service.get_all_playlists()
    if playlists == []:
        await message.channel.send('No playlists currently stored.')
    else:
        await message.channel.send('\n'.join(map(str, playlists)))


async def add_playlist(message: discord.Message, args):
    if len(args) < 3:
        await message.channel.send(f'Usage: {COMMAND_PREFIX}{args[0]} <Playlist Name> <Criteria>')
        return
    cmd, name, criteria = args
    updated = playlist_service.Playlist(name=name, link=criteria).save_to_db()
    action = 'Updated' if updated else 'Added'
    await message.channel.send(f'{action} playlist {name}.')
    logging.info(f'{message.author} {action.lower()} a playlist: {name} ({criteria})')


async def del_playlist(message: discord.Message, args):
    if len(args) != 2:
        await message.channel.send(f'Usage: {COMMAND_PREFIX}{args[0]} <Playlist Name>')
        return
    playlist_name = ' '.join(args[1:])
    deleted_count = playlist_service.delete_playlist_by_name(playlist_name)
    if deleted_count == 0:
        await message.channel.send(f'Playlist {playlist_name} does not exist. No action taken.')
    else:
        await message.channel.send(f'Playlist {playlist_name} deleted.')
        logging.info(f'Playlist {playlist_name} deleted by user {message.author}')


CONDEMNATIONS = [
    'Sayonara.',
    'I sure hope that\'s not permanent.',
    'You probably knew what you were doing.',
    'No going back now.',
    'To undo, build a time machine.',
]


async def delete_all(message: discord.Message, _):
    num_deleted = playlist_service.delete_all_playlists()
    if num_deleted == 0:
        obituary = 'No playlists to delete.'
    else:
        obituary = f':boom: Deleted {num_deleted} playlists. ' + choice(CONDEMNATIONS)
        logging.info(f'{message.author} deleted all playlists.')
    await message.channel.send(obituary)


async def play_playlist(message: discord.Message, args):
    if len(args) < 2:
        await message.channel.send(f'Usage: {COMMAND_PREFIX}{args[0]} <Playlist Name>')
        return
    name = ' '.join(args[1:])
    playlist = playlist_service.get_playlist(name)
    if playlist is None:
        await message.channel.send(f'I couldn\'t find a playlist named {name}.')
        return
    await message.channel.send('Not implemented yet.')
    logging.info(f'{message.author} played a playlist: {playlist}')


COMMANDS = {
    'ping': ping,
    'echo': echo,
    'playlists': list_playlists,
    'ps': list_playlists,
    'addPlaylist': add_playlist,
    'add': add_playlist,
    'delPlaylist': del_playlist,
    'del': del_playlist,
    'deleteAllPlaylistsYesImCompletelySure': delete_all,
    'play': play_playlist,
    'p': play_playlist
}
