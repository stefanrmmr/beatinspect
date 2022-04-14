# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import os
import sys
import toml
import time
import librosa
import essentia.standard as es

# import src.bpm_detection as bpm_detection
import src.wav_techspecs as wav_techspecs

# Streamlit Design Choices (page layout)
primary_color = st.get_option("theme.primaryColor")

st.set_page_config(layout="centered",
                   page_icon="resources/rs_logo_transparent_yellow.png",
                   page_title="beat inspector")

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.markdown('''<style>.stSpinner > div > div {border-top-color: #e3fc03;}</style>''',
    unsafe_allow_html=True)

# Title and Information
header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
with header_col1:
    st.title('beat inspector ™')
    st.write('Version 1.1.0 - April 2022 - Github @stefanrmmr')

with header_col3:
    st.write('')
    st.image("resources/rs_logo_transparent_yellow.png")

# Audio File Upload
with st.expander("SECTION - Audio File Upload",expanded=True):
    audiofile = st.file_uploader("Please select and upload an audio file (.WAV)", type='wav')

# Audio File Analytics
if audiofile is not None:

    # Save audiofile to tmp directory to be called via path
    with open(audiofile.name,"wb") as f:
        f.write(audiofile.getbuffer())

    # Inspect Audio File Specifications
    with st.expander("SECTION - Waveform and Spectrogram Insights", expanded=False):
        st.audio(audiofile)  # display audio player UX

    # Musical and Tech Specs Overview
    with st.expander("SECTION - Musical & Technical Specifications", expanded=True):

        pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

        with pref_col1:  # output: column for music scale evaluation
            with st.spinner('Calculating Scale'):
                time.sleep(0.5)
            scale_text = f'<p style="font-family:sans-serif; color:{primary_color}; font-size: 32px;">SCALE ...</p>'
            st.write('')
            st.write('')
            st.markdown(scale_text, unsafe_allow_html=True)
            st.write('')  # add spacing

        with pref_col2:  # metrics: generating insights on tech specs
            with st.spinner('Fetching Tech Specs'):
                time.sleep(0.5)
                # extract tech Specifications about wav file
                sampling_freq, channels = wav_techspecs.read_wav(audiofile)
                # assign audio channel description
                if int(channels) == 1:  # single channel .wav
                    channels = 'MONO Signal'
                elif int(channels) == 2:  # double channel .wav
                    channels = 'STEREO Signal'
                else:  # multi channel .wav
                    channels = str(channels) + ' Channel Signal'
            st.metric(label="", value=f"{sampling_freq} Hz", delta=f'WAV - {channels}', delta_color="off")
            st.write('')  # add spacing

        with pref_col3:  # metrics: calculcation of tempo
            with st.spinner('Calculating BPM'):
                time.sleep(0.5)
                # BPM estimation using essentia library
                es_audio = es.MonoLoader(filename=audiofile.name)()
                rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
                bpm_essentia, es_beats, beats_confidence, _, beats_intervals = rhythm_extractor(es_audio)
            st.metric(label="", value=f"{round(bpm_essentia, 1)} BPM", delta=f'Beat Tempo', delta_color="off")
            st.write('')  # add spacing


foot_col1, foot_col2, foot_col3, foot_col4 = st.columns([3,1.5,1.5,3])
with foot_col2:
    st.image('resources/powered_by_essentia.png')
    st.markdown("[![this is an image link](./resources/powered_by_essentia.png)](https://streamlit.io)")
with foot_col3:
    st.image('resources/coop_utility_studio.png')
