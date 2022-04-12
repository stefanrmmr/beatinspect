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
# Set Preferences & Key
if audiofile_upload is not None:
    st.write('file upload complete')

    values = st.slider(
    'Select a range of values', 0.0, 100.0, (25.0, 75.0))
    st.write('Values:', values)

    bpm = bpm_detection.detect_bpm_main('data/bounce_back.wav', 10)
    st.write(f'BPM = {bpm}')
