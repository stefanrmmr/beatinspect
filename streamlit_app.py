# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import sys
import toml
# import librosa

sys.path.append("src")

import src.bpm_detection as bpm_detection
# from src.bpm_detection import detect_bpm_main

# Streamlit Design Choices (page layout)
primary_color = st.get_option("theme.primaryColor")

st.set_page_config(layout="centered",
    page_icon="resources/rs_logo_transparent.png",
    page_title="beat inspector")

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

progressbar_design = '''<style> .stProgress .st-bo {background-color: #e3fc03;}</style>'''
st.markdown(progressbar_design, unsafe_allow_html=True)

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
audiofile_upload = st.file_uploader("Please select and upload"
                                    " an audio file (.wav)",type='wav')
# Set Preferences for Analytics
if audiofile_upload is not None:

    # display audio player UX
    st.audio(audiofile_upload)

    pref_col1, pref_col2, pref_col3 = st.columns([8, 5, 5])

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
                    bpm = bpm_detection.detect_bpm_main(audiofile_upload, timeframe)

            # y, sr = librosa.load(librosa.ex(audiofile_upload), duration=value)
            # bpm, beats = librosa.beat.beat_track(y=y, sr=sr)
            with pref_col3:
                # bpm_output = f'<p style="font-family:sans-serif; color:{primary_color}; font-size: 25.6px;">BPM = {round(bpm, 2)}</p>'
                # st.markdown(bpm_output, unsafe_allow_html=True)
                st.metric(label="Track Tempo", value=f"{round(bpm, 2)} BPM", delta='A Minor Scale', delta_color="off")
                # st.header(f'BPM = {round(bpm, 2)}')
