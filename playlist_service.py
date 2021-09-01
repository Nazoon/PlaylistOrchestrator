"""
Handles playlist querying, saving, and deletion.
"""

import os
import pymongo
from typing import List, Optional

SERVERS = 'Servers'
PLAYLISTS = 'Playlists'

_db_conn_str = os.environ['mongodb_conn_str']
_db_name = os.environ['mongodb_name']
_db = pymongo.MongoClient(_db_conn_str)[_db_name]

_playlists_collection = _db[PLAYLISTS]


class Playlist:
    name: str
    link: str

    def __init__(self, name: str = None, link: str = None):
        self.name = name
        self.link = link

    def _to_dict(self):
        d = vars(self)
        d['_id'] = _resolve_id(self)
        return d

    def __repr__(self):
        return f'Name: {self.name}\tLink: {self.link}'

    def __str__(self):
        return repr(self)

    def save_to_db(self):
        """
        Insert or update database to include this Playlist.
        """
        p = get_playlist(self.name)
        if p is None:
            _playlists_collection.insert_one(self._to_dict())
        else:
            _playlists_collection.update_one({'name': self.name}, {'$set': self._to_dict()})


def _resolve_id(playlist: Playlist) -> str:
    return playlist.name


def _dict_to_playlist(d: dict) -> Playlist:
    if '_id' in d:
        del d['_id']
    p = Playlist()
    p.__dict__.update(**d)
    return p


def get_playlist(name: str) -> Optional[Playlist]:
    """
    Find and return a Playlist by searching by name. If none exists, return None.
    """
    query = {'name': name}
    results = _playlists_collection.find_one(query)
    if results is None:
        return None
    return _dict_to_playlist(results)


def get_all_playlists() -> List[Playlist]:
    """
    Return a list of all Playlists in the database.
    """
    result = _playlists_collection.find()
    return [_dict_to_playlist(d) for d in result]


def delete_playlist_by_name(name: str) -> int:
    """
    Delete a Playlist by name and return the number of documents deleted.
    """
    query = {'name': name}
    return _playlists_collection.delete_one(query).deleted_count


def delete_all_playlists() -> int:
    """
    Delete all playlist documents in the database and return the number of documents deleted.
    """
    return _playlists_collection.delete_many(filter={}).deleted_count
