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


def get_match_data(match_id):

    shots = twelve.get_match_shots(match_id)

    stories = dict()
    stories['stories'] = twelve.get_match_points_stories(match_id)

    return stories, shots


def subpage_goals_xg_page(match_id, home_team, away_team):

    viz_cols = st.columns(4)

    stories, shots = get_match_data(match_id)

    stories['homeTeam'] = home_team
    stories['awayTeam'] = away_team
    # XG TREND
    try:
        viz = XGMatchTrend("XGMatchTrend",
                           home_team['name'],
                           away_team['name'],
                           home_team['score'],
                           away_team['score'],
                           bg_color=home_team['home_color'])
        end_min = stories['stories'][-1]['minute']
        end_period = stories['stories'][-1]['period']
        viz.set_data(
            [x['xg'] for x in shots['HomeTeamShots']],
            [x['minute'] for x in shots['HomeTeamShots']],
            [x['xg'] for x in shots['AwayTeamShots']],
            [x['minute'] for x in shots['AwayTeamShots']],
            end_period=end_period,
            end_min=end_min)
        viz.set_team_colors(home_team['home_color'], home_team['away_color'], away_team['home_color'],
                            away_team['away_color'])

        fig, ax = viz.create_visual(False)
        viz_cols[0].pyplot(fig, dpi=200, facecolor=fig.get_facecolor(), bbox_inches=None)

    except Exception as err:
        traceback.print_exc()

    # XGMatchShots
    try:
        viz2 = XGMatchShots('XGMatchShots',
                            home_team['name'],
                            away_team['name'],
                            home_team['score'],
                            away_team['score'],
                            bg_color=home_team['home_color'])
        viz2.set_data(stories, shots['HomeTeamShots'], shots['AwayTeamShots'])
        viz2.set_team_colors(home_team['home_color'], home_team['away_color'], away_team['home_color'],
                             away_team['away_color'])

        fig, ax = viz2.create_visual(False)
        viz_cols[1].pyplot(fig, dpi=200, facecolor=fig.get_facecolor(), bbox_inches=None)

    except Exception as err:
        traceback.print_exc()

    # PitchMatchShotmapViz
    try:
        viz = PitchMatchShotmapViz(f'PitchMatchShotmapViz',
                                   home_team['name'],
                                   away_team['name'],
                                   home_team['score'],
                                   away_team['score'],
                                   bg_color=home_team['home_color'])

        viz.set_data(shots['HomeTeamShots'], shots['AwayTeamShots'], stories)
        viz.set_team_colors(home_team['home_color'], home_team['away_color'], away_team['home_color'],
                            away_team['away_color'])

        fig, ax = viz.create_visual(False)
        viz_cols[2].pyplot(fig, dpi=200, facecolor=fig.get_facecolor(),
                    bbox_inches=None)  # , transparent=False, bbox_inches='tight')
    except Exception as err:
        traceback.print_exc()

    # Match Probabilities
    try:
        viz4 = XGMatchProb("XGMatchProb",
                           home_team['name'],
                           away_team['name'],
                           home_team['score'],
                           away_team['score'],
                           bg_color=home_team['home_color'])
        viz4.set_data([x['xg'] for x in shots['HomeTeamShots']], [x['xg'] for x in shots['AwayTeamShots']])
        viz4.set_team_colors(home_team['home_color'], home_team['away_color'], away_team['home_color'],
                             away_team['away_color'])

        fig, ax = viz4.create_visual(False)
        viz_cols[3].pyplot(fig, dpi=200, facecolor=fig.get_facecolor(),
                    bbox_inches=None)  # , transparent=False, bbox_inches='tight')
    except Exception as err:
        traceback.print_exc()


# Use default settings
create_default_configs()

st.header("Match")

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
selected_sub_nav = st_row_buttons(['Visuals', 'Summary', 'Shots', 'Passes','Season Shots'])

if selected_sub_nav == 'Visuals':

    match_info = {x['matchId']: x for x in matches}

    # Add color to team
    home_team = match_info.get(selected_match_id)['homeTeam']
    home_team['home_color'] = HOME_TEAM_COLOR
    home_team['away_color'] = HOME_TEAM_COLOR

    away_team = match_info.get(selected_match_id)['awayTeam']
    away_team['home_color'] = AWAY_TEAM_COLOR
    away_team['away_color'] = AWAY_TEAM_COLOR

    subpage_goals_xg_page(selected_match_id,
                          match_info.get(selected_match_id)['homeTeam'],
                          match_info.get(selected_match_id)['awayTeam'],

                          )

elif selected_sub_nav == 'Summary':

    st.write("stories")

    # get match data
    stories = twelve.get_match_points_stories(selected_match_id)

    # Transform stories to Dataframe
    df_stories = __create_df_from_stories(stories)

    st.dataframe(df_stories)

    st.write("players")
    players = twelve.get_match_players(selected_match_id)
    st.write(players)


elif selected_sub_nav == 'Shots':

    # get match data - shots
    shots = twelve.get_match_shots(selected_match_id)
    st.write(shots)


elif selected_sub_nav == 'Passes':

    # get match data - passes
    passes = twelve.get_match_passes(selected_match_id)
    st.write(passes)

    # Home Team passes
    df_passes = pd.DataFrame(passes['HomeTeamPasses'])
    df_passes = df_passes[df_passes['type'].isin(['goalkick'])] #throw-in,pass
    # df = df[df['points'] >= 0]

    viz = TwelvePitchVisual("Match passes", "pass types")

    viz.info_text = f"Info text"

    fig, ax = viz.create_pass_visual(df_passes['startX'],
                 df_passes['startY'],
                 df_passes['endX'],
                 df_passes['endY'],
                 df_passes['points'])

    st.columns(3)[0].pyplot(fig, dpi=100, facecolor=fig.get_facecolor(), bbox_inches=None)

else:
    data = twelve.get_season_shots(8, 2022)

    # Convert to dataframe
    data = pd.DataFrame(data)

    viz = TwelvePitchVisual("Season shots", "xG map")

    viz.info_text = f"Info text"

    fig, ax = viz.create_shot_visual(data['x'],
                                     data['y'],
                 data['xg'],
                 data['shot_outcome'],)

    st.columns(3)[0].pyplot(fig, dpi=100, facecolor=fig.get_facecolor(), bbox_inches=None)

    st.write(data)
