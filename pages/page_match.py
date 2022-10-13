import streamlit as st
import data.twelve_api as twelve

#
#   SIDEBAR
#
from settings import create_default_configs


def sidebar_select_competition():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    return  competitions, selected_competition_id


# Use default settings
create_default_configs()

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

    stories = twelve.get_match_points_stories(selected_match_id)
    st.write(stories)

with tab_shots:
    shots = twelve.get_match_shots(selected_match_id)
    st.write(shots)

with tab_passes:
    passes = twelve.get_match_passes(selected_match_id)
    st.write(passes)


st.write(matches    )
# select match

# get match data