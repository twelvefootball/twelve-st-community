import traceback

import streamlit as st
from st_row_buttons import st_row_buttons

import data.twelve_api as twelve
import pandas as pd
from settings import create_default_configs, HOME_TEAM_COLOR, AWAY_TEAM_COLOR
from visuals.match_visuals import XGMatchTrend, XGMatchShots, XGMatchProb, PitchMatchShotmapViz, PitchHorizontalArrows
from visuals.twelve_visuals import TwelvePitchVisual

def sidebar_select_competition():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    return  competitions, selected_competition_id


# Use default settings
create_default_configs()

st.header("David plots passes")

# Sidebar menu
competitions, selected_competition_id = sidebar_select_competition()

# Get all available matches
matches = twelve.app_get_matches(selected_competition_id)

# Create Dictionary of matches
matches_dict = {x['matchId']: f"{x['homeTeam']['name']} {x['homeTeam']['score']}-{x['awayTeam']['score']} {x['awayTeam']['name']}" for x in matches}

# select match
selected_match_id = st.sidebar.selectbox("Match", matches_dict, format_func=lambda x:matches_dict[x])

# Buttons
selected_sub_nav = st_row_buttons(['Passes'])

if  selected_sub_nav == 'Passes':

    # get match data - passes
    
    passes = twelve.get_match_passes(selected_match_id)

    # Home Team passes
    df_passes = pd.DataFrame(passes['AwayTeamPasses'])
    df_passes = df_passes[df_passes['type'].isin(['pass'])] #throw-in,pass
    df_passes = df_passes[df_passes['points'] >= 10.0]

    viz = TwelvePitchVisual("Match passes", "pass types")

    viz.info_text = f"Info text"

    fig, ax = viz.create_pass_visual(df_passes['startX'],
                 df_passes['startY'],
                 df_passes['endX'],
                 df_passes['endY'],
                 df_passes['points'])

    st.columns(3)[0].pyplot(fig, dpi=100, facecolor=fig.get_facecolor(), bbox_inches=None)

    st.write(df_passes)

