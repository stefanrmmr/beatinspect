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
# import src.record_audio as record_audio
import src.wav_techspecs as wav_techspecs
import src.detect_keyscale as detect_keyscale






from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://twitter.com/ChristianKlose3", "@ChristianKlose3"),
        br(),
        link("https://buymeacoffee.com/chrischross", image('https://i.imgur.com/thJhzOO.png')),
    ]
    layout(*myargs)






def beatinspect_main():

    footer()

    # DESIGN implement changes to the standard streamlit UI/UX
    design.design_setup()  # switch to primaryColor for accents

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
                                  ' Record via Microphone',
                                  ' Read from Audio Chip'])
            st.write('')  # add spacing

        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
            elif 'Record' in choice:
                st.write('SOON1')  # TODO SOON
                audiofile = None
            else:
                st.write('SOON2')  # TODO SOON
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
