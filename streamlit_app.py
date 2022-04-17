# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import os
import sys
import toml
import time
import base64
import numpy as np
import librosa
import librosa.display
import essentia.standard as es

import src.utils as utils  # utility functions
import src.design as design  # design choices
import src.wav_techspecs as wav_techspecs
import src.detect_keyscale as detect_keyscale
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
plt.rcParams['text.color'] = 'white'


def beatinspect_main():
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
                                  ' Record via Microphone'])
            st.write('')  # add spacing

        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
            elif 'Record' in choice:
                audiofile = None
                st.write('')
                st.write('SOON to be implemented!')
                # https://www.youtube.com/watch?v=BuD3gILJW-Q&ab_channel=Streamlit
                # USE streamlit custom component that implements a custom html/css/react element
                # input data can be passed to this component and it returns data
                # TODO build a component that uses the html/script code of above (for demo webapp rec tool)
                # the component should show up in case the radio button record mic is selected
                # the component should return a path to a audiofile
                # clean existing audio files bevore saving the new audio file! (tmp dictonary)

    # ANALYTICS for Audio File
    if audiofile is not None:

        # Save audiofile to main directory to be called via path
        with open(audiofile.name,"wb") as f:
            f.write(audiofile.getbuffer())

        # extract tech Specifications about wav file
        sampling_freq, channels = wav_techspecs.read_wav(audiofile)

        # Inspect Audio File Specifications
        with st.expander("SECTION - Waveform and Spectrogram Insights",
                         expanded=False):
            st.audio(audiofile)  # display audio player UX

            # plt.rc('xtick', labelsize=9)
            plt.rc('ytick', labelsize=9)
            # plt.rc('axes', labelsize=9)
            plt.rcParams['figure.dpi'] = 400

            fig1, ax1 = plt.subplots(1,1)
            fig1.set_size_inches(8, 3, forward=True)
            plt.ylabel('Amplitude')
            ax1.set_ylim([-1.1, 1.1])

            # GUIDELINES multiple lines all full height
            ax1.vlines(x=[0], ymin=-1, ymax=1, colors='lightgrey', ls='--', lw=0.75)
            ax1.axhline(y=0.5, color='lightgrey', linestyle='--', lw=0.75)
            ax1.axhline(y=-0.5, color='lightgrey', linestyle='--', lw=0.75)
            ax1.axhline(y=1.0, color='#e3fc03', linestyle='--', lw=0.75)
            ax1.axhline(y=-1.0, color='#e3fc03', linestyle='--', lw=0.75)

            fig1.patch.set_facecolor('black')
            fig1.patch.set_alpha(0.0)
            ax1.patch.set_facecolor('black')
            ax1.patch.set_alpha(0.0)

            ax1.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
            ax1.yaxis.label.set_color('white')          #setting up Y-axis label color to blue

            ax1.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
            ax1.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black

            ax1.spines['left'].set_color('white')        # setting up Y-axis tick color to red
            ax1.spines['top'].set_color('white')         #setting up above X-axis tick color to red
            ax1.spines['right'].set_color('white')        # setting up Y-axis tick color to red
            ax1.spines['bottom'].set_color('white')         #setting up above X-axis tick color to red

            ax1.spines['right'].set_visible(False)   # Hide the right and top spines
            ax1.spines['top'].set_visible(False)     # Hide the right and top spines

            filename = os.path.join(os.getcwd(), audiofile.name)

            y,sr = librosa.load(filename, sr=sampling_freq)
            librosa.display.waveshow(y, sr, ax=ax1, color='grey', x_axis='time')

            plt.xlabel('')
            st.pyplot(fig1)


            y_stft = librosa.stft(y)  # STFT of y
            scale_db = librosa.amplitude_to_db(np.abs(y_stft), ref=np.max)

            fig2, ax2 = plt.subplots(1,1)
            fig2.set_size_inches(8, 8, forward=True)
            img2 = librosa.display.specshow(scale_db, cmap='viridis', y_axis='log', x_axis='time', ax=ax2)
            ax2.set(title='Viridis lol')
            fig2.colorbar(img2, ax=ax2, format="%+2.f dB")
            st.pyplot(fig2)




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
