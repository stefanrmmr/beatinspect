# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import os
import sys
import toml
import time
import librosa
import essentia.standard as es

import src.wav_techspecs as wav_techspecs
import src.detect_keyscale as detect_keyscale


# DESIGN CHOICES
# get primaryColor from streamlit
primary_color = st.get_option("theme.primaryColor")
# Design page layout and browser window details
st.set_page_config(layout="centered",
                   page_icon="resources/rs_logo_transparent_yellow.png",
                   page_title="beat inspector")
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #e3fc03;}</style>''',
    unsafe_allow_html=True)
# Design change stMetricsValue to primary color via specific css-element
st.markdown('''<style>.css-1xarl3l.e16fv1kl1 {color: #e3fc03;}</style>''',
    unsafe_allow_html=True)


# Title and Information
header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
with header_col1:
    st.title('beat inspector ™')
    st.write('Version 1.1.0 - April 2022 - Github @stefanrmmr')
with header_col3:
    st.write('')  # add spacing
    st.image("resources/rs_logo_transparent_yellow.png")

# Audio File Upload
with st.expander("SECTION - Select prefered Audio Input Option",expanded=True):

    audio_col0, audio_col1, audio_col2 = st.columns([0.05,0.5,1])
    with audio_col1:
        choice = st.radio('', ['Audio File Upload', 'Record via Microphone', 'Read from Audio Chip'])
        st.write('')  # add spacing

    with audio_col2:
        if 'Upload' in choice:
            audiofile = st.file_uploader("Please upload an audio file (.WAV)", type='wav')
        elif 'Record' in choice:
            st.write('SOON1')  # TODO SOON
            audiofile = None
        else:
            st.write('SOON2')  # TODO SOON
            audiofile = None

# Audio File Analytics
if audiofile is not None:

    # Save audiofile to main directory to be called via path
    with open(audiofile.name,"wb") as f:
        f.write(audiofile.getbuffer())

    # Inspect Audio File Specifications
    with st.expander("SECTION - Waveform and Spectrogram Insights", expanded=False):
        st.audio(audiofile)  # display audio player UX

        # TODO select a section of the track (or the whole track) and analyze for sections that are above ZERO level
        # TODO for these sections that are "übersteuern" --> find out in which frequency bands they need to be decreased in amplitude
        # PLOT amplitude over frequency --> classical EQ view --> Spectrogram
        # Step 1 Select slider timeframe from overall plotted audio file (AMP oder time)
        # Step 2 Use the timeframe to calculate the Spectrogram (AMP(frequency))
        # Step 3 Plot Spectrogram plot with yellow vertical bars at frequencies where AMP too high!

    # Musical and Tech Specs Overview
    with st.expander("SECTION - Musical & Technical Specifications", expanded=True):

        pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

        with pref_col1:  # output: column for music scale evaluation
            with st.spinner('Finding Key & Scale'):
                time.sleep(0.5)
                # call utility function that calculates key,scale using essentia
                # https://essentia.upf.edu/reference/streaming_Key.html
                key, scale, key_strength = detect_keyscale.detect_ks(audiofile.name, 'diatonic')

            # scale_text = f'<p color:{primary_color}; font-size: 32px;">{key}-{scale}</p>'
            # conf_text = f'<p  color: white; font-size: 18px;">{round(key_strength, 2)}</p>'
            # st.markdown(scale_text, unsafe_allow_html=True)
            # st.markdown(conf_text, unsafe_allow_html=True)
            st.metric(label="", value=f"{key}-{scale}",
                      delta=f"Confidence {round(key_strength, 2)}",
                      delta_color="off")
            st.write('')  # add spacing

        with pref_col2:  # metrics: generating insights on tech specs
            with st.spinner('Fetching Tech Specs'):
                time.sleep(0.5)
                # extract tech Specifications about wav file
                sampling_freq, channels = wav_techspecs.read_wav(audiofile)
                # assign audio channel description
                if int(channels) == 1:  # single channel .wav
                    channels = 'MONO'
                elif int(channels) == 2:  # double channel .wav
                    channels = 'STEREO'
                else:  # multi channel .wav
                    channels = str(channels) + ' Channel'
            st.metric(label="", value=f"{sampling_freq} Hz",
                      delta=f'WAV - {channels}', delta_color="off")
            st.write('')  # add spacing

        with pref_col3:  # metrics: calculcation of tempo
            with st.spinner('Calculating BPM'):
                time.sleep(0.5)
                # BPM estimation using essentia library
                es_audio = es.MonoLoader(filename=audiofile.name)()
                rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
                bpm_essentia, _, _, _, _ = rhythm_extractor(es_audio)
            st.metric(label="", value=f"{round(bpm_essentia, 1)} BPM",
                      delta=f'Beat Tempo', delta_color="off")
            st.write('')  # add spacing


# FOOTER Content and Coop logos etc
foot_col1, foot_col2, foot_col3, foot_col4 = st.columns([3,1.5,1.5,3])
with foot_col2:
    st.image('resources/powered_by_essentia.png')
with foot_col3:
    st.image('resources/coop_utility_studio.png')
