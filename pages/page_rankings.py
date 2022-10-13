import streamlit as st
from st_row_buttons import st_row_buttons

import data.twelve_api as twelve
import pandas as pd
from settings import create_default_configs

#
#    UI
#
def sidebar_select_competition_and_seasons():
    # Single selector for competition
    competitions = twelve.competitions()
    selected_competition_id = st.sidebar.selectbox("Competition", competitions, format_func=lambda x: competitions[x])

    # Multiselector for seasons
    seasons = twelve.seasons()
    selected_season_ids = st.sidebar.multiselect("Seasons", seasons, seasons, format_func=lambda x: seasons[x])

    # Check if seasons are selected
    if len(selected_season_ids) == 0:
        st.info("At least one season needs to be selected!")
        st.stop()

    return  competitions,selected_competition_id,seasons,selected_season_ids

#
#    DATA PROCESSOR
#
def get_players_season_rankings(selected_competition_id, selected_season_ids):

    # Create Dataframe
    data = list()
    ret = twelve.get_season_players_ratings(selected_competition_id, selected_season_ids)
    for k in ret.keys(): #Seasons

        season_rankings = ret[k]
        for row in season_rankings:
            #print()
            data.append({


                'player_id': row['playerId'],
                'player': row['playerName'],
                'team_id': row['teamId'],
                'team': row['teamName'],
                'position': 'other' if  row['position'] is None else row['position'],
                'points': row['totalLeaguePoint']/1000,
                'attack': next((x for x in row['points'] if x['type']=='attack'),{'value':0})['value'],
                'defence': next((x for x in row['points'] if x['type']=='defence'),{'value':0})['value'],
                 'shot':  next((x for x in row['points'] if x['type']=='shot'),{'value':0})['value'],
                'matches': row['matchesCount'],
                'minutes': row['playedMin'],
                'season': k,
                # TODO: can add other attributes if needed


            })

    df = pd.DataFrame(data)
    return df.assign(points_p90=df.points/df.minutes*90)\
               .assign(attack_p90=df.attack/df.minutes*90).\
        assign(defence_p90=df.defence/df.minutes*90).assign(shot_p90=df.shot/df.minutes*90)


# Use default settings
create_default_configs()

# Sidebar menu for competition and seasons
competitions, selected_competition_id, seasons, selected_season_ids = sidebar_select_competition_and_seasons()

# Get the data
selected_sub_nav = st_row_buttons(['Player Ranking', 'Team Rankings'])

if selected_sub_nav == 'Player Ranking':

    # SUBPAGE 1
    # Title of the page
    st.title("Players Ranking")

    df_players_rankings = get_players_season_rankings(selected_competition_id, selected_season_ids)

    # Sidebar filter minutes
    minimal_minutes = st.sidebar.slider("Minutes", 0, 1000, 500)

    # Sidebar filter position, all positions in dataset
    selected_positions = st.sidebar.multiselect("Positions", df_players_rankings['position'].unique(), df_players_rankings['position'].unique())

    # Checkbox
    if st.sidebar.checkbox('Aggregate seasons', False):
        # Aggregate data from different seasons
        df_players_rankings = df_players_rankings.groupby(['player_id','player','team_id','team','position']).sum().reset_index()

    # FILTER data
    df_players_rankings = df_players_rankings[df_players_rankings['minutes'] >= minimal_minutes]
    df_players_rankings = df_players_rankings[df_players_rankings['position'].isin(selected_positions)]

    # Show Dataframe
    st.dataframe(df_players_rankings)

else:

    # SUBPAGE 2
    st.title("Team Ranking")
