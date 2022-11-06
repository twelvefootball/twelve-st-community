import json
import typing

import requests
import time
from datetime import datetime
import streamlit as st

from settings import TWELVE_USERNAME, TWELVE_PASSWORD, TWELVE_API, TWELVE_BLOB

COMPETITIONS_TO_TWELVE_TOURNAMENT = {

     8: 12,
     226: 13
}

SEASONS_TO_TWELVE_SEASON_ID = {

    2021: 89,
    2022: 96,

}


def competitions()->dict:
    """
        Get All Competitions
    """
    return {
        8: 'Premier League',
        226: 'Allsvenskan'
    }


def seasons()->dict:
    """
        Get All Seasons
    """
    return {
        2021: 2021,
        2022: 2022
    }


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_season_players_ratings(competition_id:int, season_ids:[]):

    """Get players season rankings"""
    ret = dict()
    for season_id in season_ids:
        ret[season_id] = __app_players_ranking(competition_id, season_id)
    return ret


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_match_points_stories(match_id: int):
    """
        Get Match Details
    """
    return __get_task(f"{TWELVE_API}/vnext2/matches/{match_id}/stories")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_match_players(match_id: int):
    """
        Get Match Details
    """
    return __get_task(f"{TWELVE_API}/vnext2/matches/{match_id}/players")


class StatusCodeException(Exception):
    pass


class TwelveJobError(Exception):
    """
    When the code fails to download the file from the Twelve server.
    Either server is down, trying to look for the wrong key in the
    downloaded json or the file is not yet available.
    """
    pass


class MatchPossessionChains(object):
    def __init__(self, match_id: int, base_file: dict, events_file: typing.List[typing.List[dict]]):
        self.match_id = match_id
        self.base_file = base_file
        self.events_file = events_file


class TWELVE:
    api_url = TWELVE_API
    blob_url = TWELVE_BLOB
    access_token = {
        'access': None,
        'expires': datetime(1970, 1, 1)
    }


def __post_resource(url, payload) -> dict:
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, data=payload, headers=headers)
    if resp.status_code != 200:
        print(f"{url} -> {resp.status_code}")
        resp = {}
    else:
        resp = resp.json()
    return resp


def get_access_token(usr, psw) -> str:
    if TWELVE.access_token['access'] is None or (datetime.now() - TWELVE.access_token['expires']).seconds > 600:
        payload = json.dumps({"id": usr, "secret": psw})
        TWELVE.access_token['access'] = __post_resource(f"{TWELVE_API}/auth/login/username", payload)['accessToken']
        TWELVE.access_token['expires'] = datetime.now()
        print('New token')

    return TWELVE.access_token['access']


def get_access() -> str:
    if TWELVE.access_token['access'] is None or (datetime.now() - TWELVE.access_token['expires']).seconds > 600:
        payload = json.dumps({"id": TWELVE_USERNAME, "secret": TWELVE_PASSWORD})
        TWELVE.access_token['access'] = __post_resource(f"{TWELVE_API}/auth/login/username", payload)['accessToken']
        TWELVE.access_token['expires'] = datetime.now()
        print('New token')

    return TWELVE.access_token['access']


def __get_task(url: str, data=None) -> dict:
    access_token = get_access()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    start_time = time.time()
    if data is None:
        resp = requests.get(url, headers=headers)
    else:
        resp = requests.get(url, data=json.dumps(data), headers=headers)

    print(f"-{url}- %s seconds ---" % (time.time() - start_time))
    if resp.status_code != 200:
        print(f"{url} -> {resp.status_code}")
        resp = {}
    else:
        start_time = time.time()
        resp = resp.json()
        print(f"-{url}- %s seconds json---" % (time.time() - start_time))
    return resp


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def app_get_matches(competition_id):

    matches = __get_task(f"{TWELVE_API}/vnext2/matches/")
    matches = [x for x in matches['completed'] if x['competitionId']==competition_id]
    return matches[0]['matches']


def __app_players_ranking(competition_id,season_id):
    return __get_task(f"{TWELVE_API}/vnext2/competitions/{competition_id}/seasons/{season_id}/points")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_match_shots(match_id: int):
    return __get_task(f"{TWELVE_API}/vnext2/matches/{match_id}/shots")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_match_passes(match_id: int):
    return __get_task(f"{TWELVE_API}/vnext2/matches/{match_id}/passes")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_team_season_data(tournament_id, season_id, team_id, type_id):
    """
        1 = pass
        3 = dribbles
        1003 = carry
        ...
    """
    return __get_task(f"{TWELVE_API}/analytics/tournament/{COMPETITIONS_TO_TWELVE_TOURNAMENT.get(tournament_id)}/season/{SEASONS_TO_TWELVE_SEASON_ID.get(season_id)}/teams/{team_id}/type_id/{type_id}/")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_player_season_data(tournament_id, season_id, player_id, type_id):
    """
        1 = pass
        3 = dribbles
        1003 = carry
        ...
    """
    return __get_task(f"{TWELVE_API}/analytics/tournament/{COMPETITIONS_TO_TWELVE_TOURNAMENT.get(tournament_id)}/season/{SEASONS_TO_TWELVE_SEASON_ID.get(season_id)}/players/{player_id}/type_id/{type_id}/")


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_players_season_minutes(season_id, tournament_id, player_id):
    return __get_task(f"{TWELVE_API}/analytics/tournament/{COMPETITIONS_TO_TWELVE_TOURNAMENT.get(tournament_id)}/season/{SEASONS_TO_TWELVE_SEASON_ID.get(season_id)}/players/{player_id}/minutes")


def get_tournament_season_teams(tournament_id: int, season_id: int) -> dict:
    return __get_task(f"{TWELVE_API}/analysis/competition/{tournament_id}/season/{season_id}/teams")


def get_team_matches(tournament_id: int, season_id: int, team_id_list: list) -> dict:
    return __get_task(f"{TWELVE_API}/analysis/competition/{tournament_id}/season/{season_id}/matches?teamIdList=" +
                          ",".join(map(str, team_id_list)))


@st.experimental_memo(ttl=60*60, show_spinner=True) # Caching the results for 60s*60
def get_tournament_season_matches_dict(tournament_id: int, season_id: int) -> dict:
    season_teams = get_tournament_season_teams(tournament_id, season_id)
    team_id_list = [team["teamId"] for team in season_teams["teams"]]
    return get_team_matches(tournament_id, season_id, team_id_list)




