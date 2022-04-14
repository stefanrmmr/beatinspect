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

        with st.spinner('Calculating BPM'):
            # extract tech Specifications about wav file
            sampling_freq, channels = wav_techspecs.read_wav(audiofile)
            # BPM estimation powered by essentia library
            es_audio = es.MonoLoader(filename=audiofile.name)()
            rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
            bpm_essentia, es_beats, beats_confidence, _, beats_intervals = rhythm_extractor(es_audio)

            # channel information description
            if int(channels) == 1:  # single channel .wav
                channels = 'Mono'
            elif int(channels) == 2:  # double channel .wav
                channels = 'Stereo'
            else:  # multi channel .wav
                channels = str(channels) + ' Channel Audio'

        st.metric(label="Audio File Technical Specifications", value=f"{round(bpm_essentia, 1)} BPM", delta=f'{channels} - WAV {sampling_freq} Hz', delta_color="off")
        bpm_output = f'<p style="font-family:sans-serif; color:{primary_color}; font-size: 25.6px;">Musical Scale (SOON!)</p>'
        st.markdown(bpm_output, unsafe_allow_html=True)

foot_col1, foot_col2, foot_col3 = st.columns([1, 2, 5])
with foot_col1:
    st.write('powered by')
with foot_col2:
    st.image('resources/essentia_logo.png')
