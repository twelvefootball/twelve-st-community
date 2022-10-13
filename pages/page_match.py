import streamlit as st
import data.twelve_api as twelve

#
#   SIDEBAR
#
from settings import create_default_configs


def sidebar_select_competition_and_seasons():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    # Multiselector for seasons
    seasons = twelve.seasons()
    selected_season_id = st.sidebar.selectbox("Seasons", seasons, format_func=lambda x: seasons[x])

    return  competitions,selected_competition_id,seasons,selected_season_id

# Use default settings
create_default_configs()

st.header("Match")

# Sidebar menu
competitions, selected_competition_id, seasons, selected_season_id = sidebar_select_competition_and_seasons()

# Get all available matches
matches = twelve.app_get_matches()

# TABS
tab_summary, tab_shots, tab_passes = st.tabs(['Summary', 'Shots', 'Passes'])
with tab_summary:
    pass

with tab_shots:
    pass
with tab_passes:
    pass


st.write(matches    )
# select match

# get match data