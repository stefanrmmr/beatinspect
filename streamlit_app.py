# beat_inspector by stefanrmmr (rs. analytics) - version April 2022
import streamlit as st
import streamlit.components.v1 as components

import os
import sys
import toml
import time
import pydub
import base64
import ffmpeg
import librosa
import numpy as np
import essentia.standard as es

import src.plots as plots  # plotting framework
import src.utils as utils  # utility functions
import src.design as design  # design choices
import src.wav_specs as wav_specs
import src.detect_keyscale as detect_keyscale


def beatinspect_main():

    # DESIGN implement changes to the standard streamlit UI/UX
    design.design_setup()  # switch to primaryColor for accents

    # TITLE and Information
    header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
    with header_col1:
        st.title('beat inspect ™')
        st.markdown('Version 1.3.1 - April 2022 - Github [@stefanrmmr](https://github.com/stefanrmmr/beatinspect)')
    with header_col3:
        st.write('')  # add spacing
        st.image("img/rs_logo_transparent_yellow.png")

    # AUDIO SOURCE File Upload Selection
    with st.expander("SECTION - Select prefered Audio Input Option",
                     expanded=True):

        audio_col0, audio_col1, audio_col2 = st.columns([0.03,0.5,1])
        with audio_col1:
            st.write('')  # add spacing
            st.write('')  # add spacing
            st.write('')  # add spacing
            choice = st.radio('',[' Audio File Upload',
                                  ' Record via Microphone'])
            st.write('')  # add spacing
        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
            elif 'Record' in choice:
                audiofile = None
                st.write('')  # ad spacing
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
        filename = os.path.join(os.getcwd(), audiofile.name)

        # evaluate whether the input audiofile has changed
        new_audiofile = False
        if audiofile.name != st.session_state.audiofile_name:
            # update session state and order new calc of attr
            st.session_state.audiofile_name = audiofile.name
            new_audiofile = True

        # Musical and Tech Specs Overview
        with st.expander("SECTION - Musical & Technical Specifications",
                         expanded=True):

            # extract tech Specifications about wav file
            sampling_freq, channels = wav_specs.read_wav(audiofile)

            # audio datei name in session state abspeichern
            # wenn die hochgeladene audiodatei.name anders ist als die im session state
            #    dann wird alles neu berechnet un die ergebnisse in session states abgespeichert
            # wenn die hochgeladene audiodatei.name GLEICH ist als die im session state
            #   dann alles aus session states laden anstatt zu berechnen

            pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

            with pref_col1:  # metrics : column for music scale evaluation
                with st.spinner('Finding Key & Scale'):
                    time.sleep(0.3)  # buffer for loading the spinner
                    # utility funct that calculates key & scale via essentia
                    # https://essentia.upf.edu/reference/streaming_Key.html

                    if new_audiofile:  # new audiofile --> update session sates
                        key, scale, key_strength = detect_keyscale.detect_ks(
                            audiofile.name, 'diatonic')
                        st.session_state.key = key
                        st.session_state.scale = scale
                        st.session_state.key_strength = key_strength
                    else:  # same audiofile --> load from session_state
                        key = st.session_state.key
                        scale = st.session_state.scale
                        key_strength = st.session_state.key_strength

                st.metric(label="", value=f"{key}-{scale}",
                          delta=f"Confidence {round(key_strength, 2)}",
                          delta_color="off")
                st.write('')  # add spacing

            with pref_col2:  # metrics: generating insights on tech specs
                with st.spinner('Fetching Tech Specs'):
                    time.sleep(0.3)  # buffer for loading the spinner

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
                    time.sleep(0.3)  # buffer for loading the spinner
                    # BPM estimation using essentia library

                    if new_audiofile:  # new audiofile --> update session sates
                        es_audio = es.MonoLoader(filename=audiofile.name)()
                        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
                        bpm_essentia, _, _, _, _ = rhythm_extractor(es_audio)
                        st.session_state.bpm_essentia = bpm_essentia
                    else:  # same audiofile --> load from session_state
                        bpm_essentia = st.session_state.bpm_essentia

                st.metric(label="", value=f"{round(bpm_essentia, 1)} BPM",
                          delta=f'Beat Tempo', delta_color="off")
                st.write('')  # add spacing


        # Inspect Audio File Specifications
        with st.expander("SECTION - Waveform and Spectrogram Insights",
                         expanded=False):

            # Generate graphs/plots for RMS & Amplitude over time
            st.audio(audiofile)  # display audio player UX

            # calculate the necessray data for further plotting
            with st.spinner('calculating spectrogram insights'):
                # calc spectrum data for plotting framework
                y,sr = librosa.load(filename, sr=sampling_freq)
                y_stft = librosa.stft(y)  # STFT of y
                scale_db = librosa.amplitude_to_db(np.abs(y_stft), ref=np.max)
                spectrogram_magn, phase = librosa.magphase(librosa.stft(y))
                rms = librosa.feature.rms(S=spectrogram_magn)  # calculating rms
                times = librosa.times_like(rms) #extracting rms timestamps

            # display the selected spectrum plot
            spectrum_coice = st.session_state.spectrum
            # due to the session state only updating after Selection
            # these plot calls need to be inversed/swapped like below
            if 'AMP' in spectrum_coice:  # generate rms spectrum plots
                with st.spinner('generating RMS spectrum plot'):
                    plots.rms_spectrum(times, rms)
            else:  # generate amp spectrum plots
                with st.spinner('generating AMP spectrum plot'):
                    plots.amp_spectrum(y,sr)

            # radio button selection for spectrum plot over time
            design.radiobutton_horizontal()  # switch alignment
            sradio_col1, sradio_col2 = st.columns([0.03, 1.5])
            with sradio_col2:
                st.session_state.spectrum = st.radio('Please select your spectrum of choice',
                                                     ['AMP Spectrum  ', 'RMS Spectrum  '])
            st.write('')  # add spacing

            # img2 = librosa.display.specshow(scale_db, ax=ax2, sr=sr, x_axis='time', y_axis='log')
            # fig.colorbar(img2, ax=ax2, format="%+2.f dB")

            # STREAMLIT double sided slider mit info dass max 20sec
            # nur wenn kleiner gleich 20 sec wird das zweite bild generiert
            # das mel spektrum gibt es nur für bestimmte abschnitte nicht ganzer track!

            # darunter custom select max 20 sec spectrum viewer !
            # INTERACTVE 3D spectrogram (turn and zoom in) for the selected timeframe
            # https://librosa.org/doc/0.9.1/generated/librosa.feature.rms.html


            # TODO select a section of the track (or the whole track) and analyze for sections that are above ZERO level
            # TODO for these sections that are "übersteuern" --> find out in which frequency bands they need to be decreased in amplitude
            # PLOT amplitude over frequency --> classical EQ view --> Spectrogram
            # Step 1 Select slider timeframe from overall plotted audio file (AMP oder time)
            # Step 2 Use the timeframe to calculate the Spectrogram (AMP(frequency))
            # Step 3 Plot Spectrogram plot with yellow vertical bars at frequencies where AMP too high!


    # FOOTER Content and Coop logos etc
    foot_col1, foot_col2, foot_col3, foot_col4, foot_col5 = st.columns([2,1.5,1.5,1.5,2])
    with foot_col2:
        essentia_html = utils.get_img_with_href('img/powered_by_essentia.png',
                                                'https://essentia.upf.edu/')
        st.markdown(essentia_html, unsafe_allow_html=True)
        # st.image('img/powered_by_essentia.png')
    with foot_col3:
        ustu_html = utils.get_img_with_href('img/coop_utility_studio.png',
                                            'https://utility-studio.com/')
        st.markdown(ustu_html, unsafe_allow_html=True)
        # st.image('img/coop_utility_studio.png')
    with foot_col4:
        librosa_html = utils.get_img_with_href('img/powered_by_librosa.png',
                                            'https://librosa.org/')
        st.markdown(librosa_html, unsafe_allow_html=True)
        # st.image('img/coop_utility_studio.png')

if __name__ == '__main__':

    # initialize spectrum choice session state
    if "spectrum" not in st.session_state:
        st.session_state.spectrum = 'RMS Spectrum'

    # initialize session state for audiofile.name
    if "audiofile_name" not in st.session_state:
        st.session_state.audiofile_name = None

    # initialize session states for attributes
    if "key" not in st.session_state:
        st.session_state.key = None
    if "scale" not in st.session_state:
        st.session_state.scale = None
    if "channels" not in st.session_state:
        st.session_state.channels = None
    if "bpm_essentia" not in st.session_state:
        st.session_state.bpm_essentia = None
    if "key_strength" not in st.session_state:
        st.session_state.key_strength = None
    if "sampling_freq" not in st.session_state:
        st.session_state.sampling_freq = None

    # initialize session states for plots
    if "plot_spectrum_amp" not in st.session_state:
        st.session_state.plot_spectrum_amp = None
    if "plot_spectrum_rms" not in st.session_state:
        st.session_state.plot_spectrum_rms = None

    # call main function
    beatinspect_main()
