from steam.steamid import SteamID
from steam.webapi import WebAPI
from flask import current_app, g


def get_webapi():
    api = getattr(g, 'webapi', None)
    if api is None:
        g.api = api = WebAPI(current_app.config['STEAM_API_KEY'])
    return api


def string_to_steamid(string, resolve_customurl=True):
    steam_api = get_webapi()
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
    steam_api = get_webapi()
    return {
        int(player['steamid']): player['personaname']
        for player in steam_api.ISteamUser.GetPlayerSummaries(
            steamids=",".join(str(id64) for id64 in id64s)
        ).get('response', {}).get('players', [])
    }
