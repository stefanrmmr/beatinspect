# beat_inspector by stefanrmmr (rs. analytics) - version April 2022

import streamlit as st
import toml

# primaryColor = toml.load("config.toml")['theme']['primaryColor']
# primaryColor = st.get_option("theme.primaryColor")
# # s = f"""
# <style>
# div.stButton > button:first-child {{ border: 5px solid {primaryColor}; border-radius:20px 20px 20px 20px; }}
# <style>
# """
# st.markdown(s, unsafe_allow_html=True)

st.markdown('''
div.stButton > button:first-child {
background-color: #00cc00;color:white;font-size:20px;height:3em;width:30em;border-radius:10px 10px 10px 10px;
}
.css-2trqyj:focus:not(:active) {
border-color: #ffffff;
box-shadow: none;
color: #ffffff;
background-color: #0066cc;
}
.css-2trqyj:focus:(:active) {
border-color: #ffffff;
box-shadow: none;
color: #ffffff;
background-color: #0066cc;
}
.css-2trqyj:focus:active){
background-color: #0066cc;
border-color: #ffffff;
box-shadow: none;
color: #ffffff;
background-color: #0066cc;
}''', unsafe_allow_html=True)


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


if st.button('servus'):
    st.write('hello')

audiofile_upload = st.file_uploader("Please select and upload an audio file (.wav)",type='wav')
# Set Preferences & Key
if audiofile_upload is not None:
    st.write('file upload complete')
