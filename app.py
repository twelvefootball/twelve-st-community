import streamlit as st

# from settings import create_default_configs

# create_default_configs()

st.title("Test")


from data.twelve_api import get_tournament_season_matches_dict

ret = get_tournament_season_matches_dict(12, 89)
st.write(ret)

# st.write("DB username:", st.secrets["TWELVE_USERNAME"])