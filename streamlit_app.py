# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import os
import sys
import toml
import time
import base64
import essentia.standard as es

import src.utils as utils  # utility functions
import src.design as design  # design choices
import src.wav_techspecs as wav_techspecs
import src.detect_keyscale as detect_keyscale

from streamlit.components.v1 import html

def beatinspect_main():
    # DESIGN implement changes to the standard streamlit UI/UX
    design.design_setup()  # switch to primaryColor for accents


    # Define your javascript
    my_js = """
    alert("Hola mundo");
    """

    # Wrapt the javascript as html code
    my_html = f"<script>{my_js}</script>"

    main_html = """
    <html>
      <head>
        <title>MediaRecorder API - Sample</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="keywords" content="WebRTC getUserMedia MediaRecorder API">
        <link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
        <style>
          button{
            margin: 10px 5px;
          }
          li{
            margin: 10px;
          }
          body{
            width: 90%;
            max-width: 960px;
            margin: 0px auto;
          }
          #btns{
            display: none;
          }
          h1{
            margin: 100px;
          }
        </style>
      </head>
      <body>
        <h1> MediaRecorder API example</h1>

        <p> For now it is supported only in Firefox(v25+) and Chrome(v47+)</p>
        <div id='gUMArea'>
          <div>
          Record:
            <input type="radio" name="media" value="video" checked id='mediaVideo'>Video
            <input type="radio" name="media" value="audio">audio
          </div>
          <button class="btn btn-default"  id='gUMbtn'>Request Stream</button>
        </div>
        <div id='btns'>
          <button  class="btn btn-default" id='start'>Start</button>
          <button  class="btn btn-default" id='stop'>Stop</button>
        </div>
        <div>
          <ul  class="list-unstyled" id='ul'></ul>
        </div>
        <script src="https://code.jquery.com/jquery-2.2.0.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script src="script.js"></script>
      </body>
    </html>
    """
    # Execute your app
    st.title("Javascript example")
    html(main_html)






    # TITLE and Information
    header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
    with header_col1:
        st.title('beat inspect ™')
        st.write('Version 1.2.0 - April 2022 - Github @stefanrmmr')
    with header_col3:
        st.write('')  # add spacing
        st.image("resources/rs_logo_transparent_yellow.png")

    # AUDIO SOURCE File Upload Selection
    with st.expander("SECTION - Select prefered Audio Input Option",
                     expanded=True):

        audio_col0, audio_col1, audio_col2 = st.columns([0.03,0.5,1])
        with audio_col1:
            choice = st.radio('',[' Audio File Upload',
                                  ' Record via Microphone'])
            st.write('')  # add spacing

        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
            elif 'Record' in choice:
                audiofile = None


    # ANALYTICS for Audio File
    if audiofile is not None:

        # Save audiofile to main directory to be called via path
        with open(audiofile.name,"wb") as f:
            f.write(audiofile.getbuffer())

        # Inspect Audio File Specifications
        with st.expander("SECTION - Waveform and Spectrogram Insights",
                         expanded=False):
            st.audio(audiofile)  # display audio player UX

            # TODO select a section of the track (or the whole track) and analyze for sections that are above ZERO level
            # TODO for these sections that are "übersteuern" --> find out in which frequency bands they need to be decreased in amplitude
            # PLOT amplitude over frequency --> classical EQ view --> Spectrogram
            # Step 1 Select slider timeframe from overall plotted audio file (AMP oder time)
            # Step 2 Use the timeframe to calculate the Spectrogram (AMP(frequency))
            # Step 3 Plot Spectrogram plot with yellow vertical bars at frequencies where AMP too high!

        # Musical and Tech Specs Overview
        with st.expander("SECTION - Musical & Technical Specifications",
                         expanded=True):

            pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

            with pref_col1:  # output: column for music scale evaluation
                with st.spinner('Finding Key & Scale'):
                    time.sleep(0.5)
                    # call utility function that calculates key,scale using essentia
                    # https://essentia.upf.edu/reference/streaming_Key.html
                    key, scale, key_strength = detect_keyscale.detect_ks(
                        audiofile.name, 'diatonic')

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
        essentia_html = utils.get_img_with_href('resources/powered_by_essentia.png',
                                                'https://essentia.upf.edu/')
        st.markdown(essentia_html, unsafe_allow_html=True)
        # st.image('resources/powered_by_essentia.png')
    with foot_col3:
        ustu_html = utils.get_img_with_href('resources/coop_utility_studio.png',
                                            'https://utility-studio.com/')
        st.markdown(ustu_html, unsafe_allow_html=True)
        # st.image('resources/coop_utility_studio.png')


if __name__ == '__main__':
    # call main function
    beatinspect_main()
