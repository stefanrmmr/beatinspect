# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import sys
import toml
# import librosa
# sys.path.append("src")

import src.bpm_detection as bpm_detection
# from src.bpm_detection import detect_bpm_main

# Streamlit Design Choices (page layout)
primary_color = st.get_option("theme.primaryColor")

st.set_page_config(layout="centered",
                   page_icon="resources/rs_logo_transparent.png",
                   page_title="beat inspector")

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.markdown('''<style>.stSpinner > div > div {border-top-color: #e3fc03;}</style>''',
    unsafe_allow_html=True)

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
with st.expander("Audio File Upload Section",expanded=True):
    audiofile_upload = st.file_uploader("Please select and upload an audio file (.WAV)", type='wav')
    if audiofile_upload is not None:
        st.audio(audiofile_upload)  # display audio player UX

# Set Preferences for Analytics
if audiofile_upload is not None:

    pref_col1, pref_col2, pref_col3 = st.columns([8, 5, 8])

    with pref_col1:
        complexity = st.radio("Select complexity of audio track",
            ('Basic instrumental loop', 'Advanced dynamic track'))
        timeframe = 5  # Initialize timeframe for audio analytics
        if 'Basic' in complexity:
            timeframe = 2.5

    with pref_col2:
        # Initiate Analysis of bpm
        st.write('')  # add spacing
        st.write('')  # add spacing
        if st.button('Detect BPM'):
            with pref_col3:
                with st.spinner('Calculating BPM'):
                    bpm, sampling_freq, channels = bpm_detection.detect_bpm_main(audiofile_upload, timeframe)
                    if int(channels) == 1:  # single channel .wav
                        channels = 'Mono'
                    elif int(channels) == 2:  # double channel .wav
                        channels = 'Stereo'
                    else:  # multi channel .wav
                        channels = str(channels) + 'Channel'

            with pref_col3:  # Output Analytics Results
                st.metric(label="Audio File Technical Specifications", value=f"{round(bpm, 1)} BPM", delta=f'{channels} - {sampling_freq} Hz', delta_color="off")
                bpm_output = f'<p style="font-family:sans-serif; color:{primary_color}; font-size: 25.6px;">Musical Scale (soon)</p>'
                st.markdown(bpm_output, unsafe_allow_html=True)
