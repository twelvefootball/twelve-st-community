import streamlit as st
import data.twelve_api as twelve
import pandas as pd
#
#   SIDEBAR
#
from settings import create_default_configs


def sidebar_select_competition():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    return  competitions, selected_competition_id


def __create_df_from_stories(twelve_stories):
    def get_description(story):
        if story['type_id'] == 1:
            if story['description'] == 'Assist':
                return story['description']
            return 'Pass'

        if story['type_id'] == 1003:
            return 'Ball Carry'

        return story['description']

    story_points = []
    for s1 in twelve_stories:
        if s1.get('point', None) is not None and s1['point']['type'] is not None and s1['point']['type'] not in ['press', 'love']:
            story_points.append({
                'player_id': s1['players'][0]['playerId'],
                'player': s1['players'][0]['name'],
                'points': s1['point']['value'],
                'type': s1['point']['type'],
                'type_id': s1['type_id'],
                'description': get_description(s1),
                'period': s1['period'],
                'minute': s1['minute'],
                'second': s1['second'],
                'team_id': s1['players'][0]['teamId'],
                'shot_xg': 0 if s1.get('stats', None) is None else s1['stats'].get('expectedGoals', 0),
                'start_x': s1.get('x'),
                'start_y': s1.get('y'),
                'goal': True if s1['type_id'] == 16 and s1['point']['value'] > 0 else False,
                'shot_on_target': True if s1['type_id'] in [15, 16] and 'Blocked' not in s1['description'] else False,
                'shot_on_post': True if s1['type_id'] in [14] else False,
                'shot_off_target': True if s1['type_id'] in [13] else False,
                'own_goal': True if s1['type_id'] == 16 and s1['point']['value'] <= 0 else False,
                'successful': s1['point']['value']>0
            })
    df = pd.DataFrame(story_points)
    return df


# Use default settings
# create_default_configs()

st.header("Match")

# Sidebar menu
competitions, selected_competition_id = sidebar_select_competition()

# Get all available matches
matches = twelve.app_get_matches(selected_competition_id)


# Create Dictionary of matches
matches_dict = {x['matchId']: f"{x['homeTeam']['name']} {x['homeTeam']['score']}-{x['awayTeam']['score']} {x['awayTeam']['name']}" for x in matches}

selected_match_id = st.sidebar.selectbox("Match", matches_dict, format_func=lambda x:matches_dict[x])


# TABS
tab_summary, tab_shots, tab_passes = st.tabs(['Summary', 'Shots', 'Passes'])
with tab_summary:

    st.write("stories")
    stories = twelve.get_match_points_stories(selected_match_id)

    # Transform stories to Dataframe
    df_stories = __create_df_from_stories(stories)

    st.dataframe(df_stories)

    st.write("players")
    players = twelve.get_match_players(selected_match_id)
    st.write(players)

with tab_shots:

    shots = twelve.get_match_shots(selected_match_id)
    st.write(shots)

with tab_passes:
    passes = twelve.get_match_passes(selected_match_id)
    st.write(passes)

# select match

# get match data