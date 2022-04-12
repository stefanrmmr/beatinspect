# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import sys
import toml

sys.path.append("src")

import src.bpm_detection as bpm_detection
# from src.bpm_detection import detect_bpm_main

# Streamlit Design Choices (page layout)
st.set_page_config(layout="centered",
    page_icon="resources/rs_logo_transparent.png",
    page_title="beat inspector")

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Title and Information
header_col1, header_col2, header_col3 = st.columns([10, 1.7, 3.3])
with header_col1:
    st.title('beat inspector ™')
    st.write('by rs. analytics (github @stefanrmmr)'
             ' - version 1.0.0 - April 2022')
    st.write('')
with header_col3:
    st.image("resources/rs_logo_transparent.png")

# Audio File Upload
audiofile_upload = st.file_uploader("Please select and upload"
                                    " an audio file (.wav)",type='wav')
# Set Preferences for Analytics
if audiofile_upload is not None:
    value = st.slider('Select size of the the time-window to be scanned (sec)',
        min_value=0.5, max_value=10, value=3, step=0.5)

    # Initiate Analysis of bpm
    if st.button('Analyse BPM'):
        bpm = bpm_detection.detect_bpm_main(audiofile_upload, value)
        st.write(f'BPM = {bpm}')
        st.write(f'Audio file: {audiofile_upload}')
