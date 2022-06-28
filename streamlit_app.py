# beat_inspector by stefanrmmr (rs. analytics) - version April 2022

# Version 1.1 add bpm detection, build page structure
# Version 1.2 add music scale detection & design tweaks
# Version 1.3 add amp & rms spectrum, session states, bit_depth
# Version 1.4 add live recording feature via custom component
# Version 1.5 add 3d mel spectrum analyzer with peaks detection

import streamlit as st
import streamlit.components.v1 as components

import os
import sys
import toml
import time
import base64
import librosa
import requests
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
import essentia.standard as es

import src.plots_matplotlib as plots_mtpl  # plotting framework matplotly
import src.plots_plotly as plots_pltl  # plotting framework plotly dash
import src.utils as utils  # utility functions
import src.detect_keyscale as detect_keyscale

# import design augmentation for streamlit UX/UI
import src.streamlit_design as streamlit_design

# custom component for recording client audio in browser
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
# specify directory and initialize st_audiorec object functionality
st_audiorec = components.declare_component("st_audiorec", path=build_dir)


# CALLBACK FUNCTIONS & Session States
def radiobuttons1_callback():
    st.session_state.spectrum3d = st.session_state['radiobuttons1_value']

def radiobuttons2_callback():
    st.session_state.spectrum2d = st.session_state['radiobuttons2_value']

def slider1_callback():
    st.session_state.melspec_treshold = st.session_state['slider1_value']


def beatinspect_main():

    # DESIGN implement changes to the standard streamlit UI/UX
    streamlit_design.design_setup()  # switch to primaryColor

    # initialize global vars
    advanced_analytics = False
    audiofile_name = None

    # TITLE and Information
    header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
    with header_col1:
        st.title('beat inspect ™')
        st.markdown('Version 1.5.0 - June 2022 - '+
            '[@GitHub](https://github.com/stefanrmmr/beatinspect) '+
            '[@Instagram](https://www.instagram.com/beatinspect)')
    with header_col3:
        st.write('')  # add spacing
        st.image("img/rs_logo_transparent_yellow.png")

    # AUDIO SOURCE File Upload Selection
    with st.expander("SECTION - Select prefered Audio Input Option",
                     expanded=True):

        audio_col0, audio_col1, audio_col2 = st.columns([0.03,0.5,1])
        with audio_col1:
            streamlit_design.add_spacing(3)  # add linebreaks
            choice = st.radio('',[' Audio File Upload',
                                  ' Record via Microphone'])
            # choice = st.radio('',[' Audio File Upload'])
            st.write('')  # add spacing
        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
                if audiofile is not None:
                    # only enable advanced analytics for files
                    # that have not been recorded with beatinspect
                    audiofile_name = audiofile.name
                    if not "beatinspect_rec_" in audiofile_name:
                        advanced_analytics = True
                        # enable advanced analytics bc uploaded

                    # Save to main dir to be called via path
                    with open(audiofile_name,"wb") as f:
                        f.write(audiofile.getbuffer())

            elif 'Record' in choice:
                audiofile = None

                rec_msg = '<p style="color: #e3fc03; font-size: 1rem;">'\
                          'Use this audio-recorder to generate files that '\
                          'can be analyzed using beatinspect - min. 15 '\
                          'seconds for optimal functionality!</p>'
                st.markdown(rec_msg, unsafe_allow_html=True)

                # the audiorec custom component
                base64data_audio = st_audiorec()

                # APPROACH: DECODE BASE64 DATA FROM return value
                # st.write(base64data_audio)
                # if (base64data_audio != None) and (base64data_audio != '') and ('test' not in base64data_audio):
                    # decoding process of base64 string to wav file
                    # with st.spinner('Decoding audio data...'):
                        # base64data_audio = base64data_audio.replace('data:audio/wav;base64,', '')
                        # TODOOOOOOOOO
                        # st.write(base64data_audio)  # remove metadata header of base64 string

                        # audiofile_name = "temp.wav"
                        # wav_file = open(audiofile_name, "wb")
                        # decode_string = base64.b64decode(base64data_audio+'==')
                        # wav_file.write(decode_string)

                    # audiofile_path = os.path.join(os.getcwd(), audiofile_name)
                    # st.audio(audiofile_path)


    # ANALYTICS for Audio File
    if audiofile_name is not None:

        audiofile_path = os.path.join(os.getcwd(), audiofile_name)
        # evaluate whether the input audiofile has changed
        new_audiofile = False # same audiofile --> load from session_state
        if audiofile_name != st.session_state.audiofile_name:
            # update session state and order new calc of attr
            st.session_state.audiofile_name = audiofile_name
            # reset session state for selected amp/rms plot

            # RESET critical selection values in case of file change
            st.session_state.spectrum2d = 'RMS Spectrum'
            st.session_state.spectrum3d = 'Peaks'
            st.session_state.melspec_treshold = -10

            new_audiofile = True # new audiofile --> update session sates

        # Musical and Tech Specs Overview
        with st.expander("SECTION - Musical & Technical Specifications",
                         expanded=True):

            # extract technical specifications about wav file
            # no needfor session_state saving bc instant calc
            wav_specs = sf.SoundFile(audiofile_path)
            wav_data, _ = sf.read(audiofile_path)
            try:
                bit_depth = int(str(wav_specs.subtype)[4:])
            except:
                bit_depth = ''
            sampling_freq = wav_specs.samplerate
            channels = wav_specs.channels
            frames = wav_specs.frames
            # seconds = frames/sampling_freq

            pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

            with pref_col1:  # metrics: generating insights on tech specs
                if int(channels) == 1:
                    # single channel .wav
                    channels = 'MONO'
                elif int(channels) == 2:
                    # double channel .wav
                    channels = 'STEREO'
                else:  # multi channel .wav
                    channels = str(channels) + ' Channel'

                st.metric(label="", value=f"{sampling_freq} Hz",
                          delta=f'{bit_depth}bit WAV - {channels}', delta_color="off")
                st.write('')  # add spacing

            with pref_col2:  # metrics : column for music scale evaluation
                if new_audiofile:  # new audiofile --> update session sates
                    with st.spinner('Finding Key & Scale'):
                        time.sleep(0.3)  # buffer for loading the spinner
                        # utility funct that calculates key & scale via essentia
                        # https://essentia.upf.edu/reference/streaming_Key.html
                        key, scale, key_strength = detect_keyscale.detect_ks(
                            audiofile_name, 'diatonic')
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

            with pref_col3:  # metrics: calculcation of tempo
                if new_audiofile:  # new audiofile --> update session sates
                    with st.spinner('Calculating BPM'):
                        time.sleep(0.3)  # buffer for loading the spinner
                        # BPM estimation using essentia library
                        es_audio = es.MonoLoader(filename=audiofile_name)()
                        rhythm_ex = es.RhythmExtractor2013(method="multifeature")
                        bpm_essentia, _, _, _, _ = rhythm_ex(es_audio)
                        st.session_state.bpm_essentia = bpm_essentia
                else:  # same audiofile --> load from session_state
                    bpm_essentia = st.session_state.bpm_essentia

                st.metric(label="", value=f"{round(bpm_essentia, 1)} BPM",
                          delta=f'Beat Tempo', delta_color="off")
                streamlit_design.add_spacing(1)  # add linebreak


        if advanced_analytics:
            # calculate the necessary spectrum data for in-depth insights
            # however only calc data in case the file is suitable/qualified

            if new_audiofile:
                # new audiofile --> update session states
                with st.spinner('calculating spectrogram insights'):
                    y, sr = librosa.load(audiofile_path, sr=sampling_freq)
                    y_stft = librosa.stft(y)  # STFT of y audio signal
                    scale_db = librosa.amplitude_to_db(np.abs(y_stft), ref=np.max)
                    spectrogram_magn, phase = librosa.magphase(librosa.stft(y))
                    rms = librosa.feature.rms(S=spectrogram_magn)  # calculating rms
                    times = librosa.times_like(rms) #extracting rms timestamps
                    duration = librosa.get_duration(y=y, sr=sr)
                    st.session_state.y, st.session_state.sr = y, sr
                    st.session_state.times, st.session_state.rms = times, rms
                    st.session_state.duration = duration

            if not new_audiofile:
                # same audiofile --> load from session_state
                y, sr = st.session_state.y, st.session_state.sr
                times, rms = st.session_state.times, st.session_state.rms
                duration = st.session_state.duration


        # Inspect Audio File Specifications
        with st.expander("SECTION - Loudness Amplitude Analytics",
                         expanded=True):

            if not advanced_analytics:
                analytics_msg = '<p style="color: #e3fc03; font-size: 1rem;">'\
                                'Only available for original audio files '\
                                '(excluding beatinspect recordings)</p>'
                st.markdown(analytics_msg, unsafe_allow_html=True)

            if advanced_analytics:  # only if audio file uploaded
                # Generate graphs/plots for RMS & Amplitude over time
                # st.audio(audiofile)  # display web audio player UX/UI

                streamlit_design.add_spacing(1)  # add linebreak
                # due to the session state only updating after Selection
                # these plot calls need to be inversed/swapped like below
                if 'AMP' in st.session_state.spectrum2d:  # generate rms spectrum plots
                    with st.spinner('generating AMP spectrum plot'):
                        # time.sleep(0.3)  # add delay for spinner
                        plots_mtpl.amp_spectrum(y, sr)
                if 'RMS' in st.session_state.spectrum2d:  # generate amp spectrum plots
                    with st.spinner('generating RMS spectrum plot'):
                        # time.sleep(0.3)  # add delay for spinner
                        plots_mtpl.rms_spectrum(times, rms)

                # radio button selection for spectrum plot over time
                streamlit_design.radiobutton_horizontal()  # switch alignment
                sradio2_col1, sradio2_col2, sradio2_col3, sradio2_col4 = st.columns([0.08, 1.5, 1.5, 0.1])
                with sradio2_col2:
                    streamlit_design.add_spacing(2)  # add linebreaks
                    st.radio('Please select your Volume-Spectrum of choice.',
                              ['RMS Spectrum  ', 'AMP Spectrum  '],
                              key='radiobuttons2_value', on_change=radiobuttons2_callback)

                with sradio2_col3:
                    meter = pyln.Meter(sampling_freq) # create BS.1770 meter --> international standard
                    peak_normalized_audio = pyln.normalize.peak(wav_data, 0)  # peak normalize audio to 0 dB
                    loudness = meter.integrated_loudness(peak_normalized_audio) # measure loudness

                    st.metric(label="", value=f"{round(loudness, 2)} dB",
                              delta=f'Audio Loudness', delta_color="off")

                st.write('')  # add spacing


        # Inspect Audio File Specifications
        with st.expander("SECTION - 3D MEL Spectrogram & Peak Detection",
                         expanded=True):

            if not advanced_analytics:
                analytics_msg = '<p style="color: #e3fc03; font-size: 1rem;">'\
                                'Only available for original audio files '\
                                '(excluding beatinspect recordings)</p>'
                st.markdown(analytics_msg, unsafe_allow_html=True)

            if advanced_analytics:  # only if audio file uploaded
                # Generate graphs/plots for RMS & Amplitude over time
                st.audio(audiofile)  # display web audio player UX/UI



                # TODO slider default values set to be at 30sec when duration larger than 1min
                #      otherwise use the -25% on both ends approach as listed below

                # AUDIO TIMEFRAME Selection for Mel-Spectrogram
                slider0_col1, slider0_col2, slider0_col3 = st.columns([0.45, 2, 0.3])
                with slider0_col2:  # add columns for sufficient padding
                    streamlit_design.add_spacing(1)  # add linebreak

                    if duration > 30:  # if audio is longer than 30 sec --> performance limited
                        sec_range = st.slider('Select Timeframe for the spectrogram - Limited Performance if longer than 30 sec!',
                                              0, int(duration), 0, 30)  # only select first 30 sec
                    else:  # if the audio file is shorter than 30 sec  --> no performance loss
                        sec_range = st.slider('Select Timeframe for the spectrogram - Limited Performance if longer than 30 sec!',
                                              0, int(duration), 0, int(duration))  # full timeframe

                    y_slice, sr_slice = librosa.load(audiofile_path, sr=sampling_freq, offset=sec_range[0],
                                                     duration=sec_range[1] - sec_range[0])

                if 'Peaks' in st.session_state.spectrum3d:
                    with st.spinner('generating 3D Mel Spectrogram - PEAKS DETECTION'):
                        # plot 3D interactive mel spectrogram
                        plots_pltl.melspectrogram_plotly3d(y_slice, sr_slice, sec_range[0], True, True, st.session_state.melspec_treshold)
                if 'Default' in st.session_state.spectrum3d:
                    with st.spinner('generating 3D Mel Spectrogram - DEFAULT MODE'):
                        # plot 3D interactive mel spectrogram
                        plots_pltl.melspectrogram_plotly3d(y_slice, sr_slice, sec_range[0], False, False, st.session_state.melspec_treshold)

                fullscreen_msg = '<p style="color: #e3fc03; font-size: 1rem;">'\
                                'Drag the graph to explore 3D viewing angles & zooming!'\
                                ' - Works best in fullscreen mode!'
                mardown1_col1, mardown1_col2 = st.columns([0.06, 3])
                with mardown1_col2:  # add padding for the markdown text
                    st.markdown(fullscreen_msg, unsafe_allow_html=True)


                # radio button selection for spectrum plot over time
                streamlit_design.radiobutton_horizontal()  # switch alignment
                sradio1_col1, sradio1_col2, sradio1_col3, sradio1_col4 = st.columns([0.08, 1.5, 1.5, 0.1])
                with sradio1_col2:
                    st.radio('Please select your prefered Mel-Spectrum viewing mode.', ['Peaks Detection  ', 'Default Top View  '],
                              key='radiobuttons1_value', on_change=radiobuttons1_callback)
                with sradio1_col3:
                    st.slider('Peaks Detection Treshold Selection [dB]', -25, 0, -10, key='slider1_value', on_change=slider1_callback)
                st.write('')






    with st.spinner('footer logos'):
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
    if "spectrum2d" not in st.session_state:
        st.session_state.spectrum2d = 'RMS Spectrum'  # "RMS Spectrum"

    # initialize mel-spectrum choice session state
    if "spectrum3d" not in st.session_state:
        st.session_state.spectrum3d = 'Peaks'  # "Default"

    if "melspec_treshold" not in st.session_state:
        st.session_state.melspec_treshold = -10

    # initialize session state for audiofile.name
    if "audiofile_name" not in st.session_state:
        st.session_state.audiofile_name = None

    # initialize session states for attributes
    if "key" not in st.session_state:
        st.session_state.key = None
    if "scale" not in st.session_state:
        st.session_state.scale = None
    if "bpm_essentia" not in st.session_state:
        st.session_state.bpm_essentia = None
    if "key_strength" not in st.session_state:
        st.session_state.key_strength = None

    # initialize session states for plots attr
    if "y" not in st.session_state:
        st.session_state.y = None
    if "sr" not in st.session_state:
        st.session_state.sr = None
    if "rms" not in st.session_state:
        st.session_state.rms = None
    if "times" not in st.session_state:
        st.session_state.times = None
    if "duration" not in st.session_state:
        st.session_state.duration = None

    # everytime something on a streamlit app interface is clicked it is automatically run again!
    # Callbacks are run before the app script run. On clicking/dragging any slider or button,
    # via the callback, the relevant session state values are updated before the script is run again

    # NORMAL button that updates a session state after it has been clicked.
    # --> click --> something has changed --> rerun st.app (using current session state value) --> update session states
    # *this configuration is lagging behind*

    # button using CALLBACK that updates a related session state variable
    # --> click --> session state update --> something has changed --> rerun st.app (using current session state value)
    # *this configuration is NOT lagging behind*


    # call main function
    beatinspect_main()
