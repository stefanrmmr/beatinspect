# beat_inspector by stefanrmmr (rs. analytics) - version April 2022

import streamlit as st

# Streamlit Design Choices (remove red header line)
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# TITLE and information 
header_col1, header_col2, header_col3 = st.columns([10, 1, 4])

with header_col1:
  st.title('beat inspector™')
  st.markdown('by [rs. analytics](https://www.linkedin.com/in/stefanrmmr/) - version 1.0.0 April 2022')
  st.write('')
with header_col3:
  st.image("Screenshot_4_black")




