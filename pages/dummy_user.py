import streamlit as st

import data.twelve_api as twelve

st.title('My Title')


data = twelve.app_get_matches(8)

st.write(data)