import traceback

import streamlit as st
from st_row_buttons import st_row_buttons

import data.twelve_api as twelve
import pandas as pd
from settings import create_default_configs, HOME_TEAM_COLOR, AWAY_TEAM_COLOR
from visuals.match_visuals import XGMatchTrend, XGMatchShots, XGMatchProb, PitchMatchShotmapViz, PitchHorizontalArrows


def sidebar_select_competition():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    return  competitions, selected_competition_id


def get_match_data(match_id):

    shots = twelve.get_match_shots(match_id)

    stories = dict()
    stories['stories'] = twelve.get_match_points_stories(match_id)

    return stories, shots


# Use default settings
create_default_configs()

st.header("Plotting Passes Demo")

# Sidebar menu
competitions, selected_competition_id = sidebar_select_competition()

# Get all available matches
matches = twelve.app_get_matches(selected_competition_id)

# Create Dictionary of matches
matches_dict = {x['matchId']: f"{x['homeTeam']['name']} {x['homeTeam']['score']}-{x['awayTeam']['score']} {x['awayTeam']['name']}" for x in matches}


# select match
selected_match_id = st.sidebar.selectbox("Match", matches_dict, format_func=lambda x:matches_dict[x])


# TABS
# tab_visuals, tab_summary, tab_shots, tab_passes = st.tabs(['Visuals', 'Summary', 'Shots', 'Passes'])

# Buttons
selected_sub_nav = st_row_buttons(['Passes'])

if  selected_sub_nav == 'Passes':

    # get match data - passes
    
    passes = twelve.get_match_passes(selected_match_id)

    # Home Team passes
    df_passes = pd.DataFrame(passes['HomeTeamPasses'])
    df_passes = df_passes[df_passes['type'].isin(['goalkick'])] #throw-in,pass
    # df = df[df['points'] >= 0]

    viz = PitchHorizontalArrows('AllPlayerRuns',
                                title=f"Passes",
                                subtitle="Goalkicks",
                                provider='opta')

    viz.info_text = f"Info text"

    viz.set_data(df_passes['startX'],
                 df_passes['startY'],
                 df_passes['endX'],
                 df_passes['endY'],
                 df_passes['points'])

    fig, ax = viz.create_visual(False)

    st.columns(3)[0].pyplot(fig, dpi=100, facecolor=fig.get_facecolor(), bbox_inches=None)

    st.write(passes)

