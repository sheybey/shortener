from steam.steamid import SteamID
from steam.webapi import WebAPI

from . import app


def string_to_steamid(string, resolve_customurl=True):
    steam_api = WebAPI(app.config['STEAM_API_KEY'])
    try:
        steamid = SteamID(string)
        if not steamid.is_valid() and resolve_customurl:
            steamid = SteamID(
                steam_api.ISteamUser.ResolveVanityURL(
                    vanityurl=string
                ).get('response', {}).get('steamid')
            )
        return steamid
    except ValueError:
        return SteamID()


def resolve_steam_names(id64s):
    return {
        int(player['steamid']): player['personaname']
        for player in steam_api.ISteamUser.GetPlayerSummaries(
            steamids=",".join(str(id64) for id64 in id64s)
        ).get('response', {}).get('players', [])
    }
