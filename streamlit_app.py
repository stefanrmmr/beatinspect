# beat_inspector by stefanrmmr (rs. analytics) - version April 2022

import streamlit as st
import toml

primaryColor = toml.load("config.toml")['theme']['primaryColor']


# Streamlit Design Choices (update button colors)
button_design = """
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>"""
st.markdown(button_design, unsafe_allow_html=True)

# Streamlit Design Choices (remove red header line)
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


# TITLE and information
header_col1, header_col2, header_col3 = st.columns([10, 1.7, 3.3])

with header_col1:
  st.title('beat inspector ™')
  st.write('by rs. analytics (github @stefanrmmr) - version 1.0.0 April 2022')
  st.write('')
with header_col3:
  st.image("resources/rs_logo_transparent.png")

if st.button('Say hello'):
     st.write('Why hello there')
 else:
     st.write('Goodbye')

audiofile_upload = st.file_uploader("Please select and upload an audio file (.wav)",type='wav')
# Set Preferences & Key
if audiofile_upload is not None:
    st.write('file upload complete')
