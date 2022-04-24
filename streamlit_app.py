# beat_inspector by stefanrmmr (rs. analytics) - version April 2022

# Version 1.1 add bpm detection, build page structure
# Version 1.2 add music scale detection & design tweaks
# Version 1.3 add amp & rms spectrum, session states, bit_depth
# Version 1.4 add live recording feature via custom component

import streamlit as st
import streamlit.components.v1 as components
# from my_component import my_component

import os
import sys
import toml
import time
import pydub
import base64
import ffmpeg
import librosa
import numpy as np
import soundfile as sf
import essentia.standard as es

import base64
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from pydub import AudioSegment

import src.plots as plots  # plotting framework
import src.utils as utils  # utility functions
import src.design as design  # design choices
import src.detect_keyscale as detect_keyscale

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "my_component/frontend/build")
_component_func = components.declare_component("my_component", path=build_dir)


def beatinspect_main():

    # DESIGN implement changes to the standard streamlit UI/UX
    design.design_setup()  # switch to primaryColor for accents

    # initialize global vars
    advanced_analytics = False
    audiofile_name = None

    # TITLE and Information
    header_col1, header_col2, header_col3 = st.columns([10, 2.5, 2.5])
    with header_col1:
        st.title('beat inspect ™')
        st.markdown('Version 1.3.2 - April 2022 - Github '
            '[@stefanrmmr](https://github.com/stefanrmmr/beatinspect)')
    with header_col3:
        st.write('')  # add spacing
        st.image("img/rs_logo_transparent_yellow.png")





    # ++++++++++++++++













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
            # choice = st.radio('',[' Audio File Upload'])
            st.write('')  # add spacing
        with audio_col2:
            if 'Upload' in choice:
                audiofile = st.file_uploader("", type='wav')
                if audiofile is not None:
                    advanced_analytics = True
                    # enable advanced analytics bc uploaded
                    audiofile_name = audiofile.name
                    # Save to main dir to be called via path
                    with open(audiofile_name,"wb") as f:
                        f.write(audiofile.getbuffer())

            elif 'Record' in choice:
                audiofile = None
                # st.write('')  # ad spacing
                # st.write('SOON to be implemented!')

                rv1 = _component_func(name='servus')
                st.write(rv1)

                stt_button  = Button(label="Speak", width=100, height=20)

                stt_button.js_on_event("button_click", CustomJS(code="""
                const timeMilliSec = 10000 //Fixed 10sec recording
                navigator.mediaDevices.getUserMedia({ audio: true })
                  .then(stream => {
                    const mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();
                    const audioChunks = [];
                    mediaRecorder.addEventListener("dataavailable", event => {
                      audioChunks.push(event.data);
                    });
                    mediaRecorder.addEventListener("stop", () => {
                      //convert audioBuffer to wav
                      const audioBlob = new Blob(audioChunks, {type:'audio/wav'});
                      //create base64 reader
                      var reader = new FileReader();
                      reader.readAsDataURL(audioBlob);
                      reader.onloadend = function() {
                        //read base64
                        var base64data = reader.result;
                        //send data to streamlit
                        document.dispatchEvent(new CustomEvent("GET_AUDIO_BASE64", {detail: base64data}));
                      }
                    });
                    setTimeout(() => {
                      mediaRecorder.stop();
                    }, timeMilliSec);
                  });
                  """))

                result = streamlit_bokeh_events(
                    stt_button,
                    events="GET_AUDIO_BASE64",
                    key="listen",
                    refresh_on_update=False,
                    override_height=75,
                    debounce_time=0)

                if result:
                    if "GET_AUDIO_BASE64" in result:
                        b64_str_metadata = result.get("GET_AUDIO_BASE64")
                        metadata_string = "data:audio/wav;base64,"
                        if len(b64_str_metadata)>len(metadata_string):
                            #get rid of metadata (data:audio/wav;base64,)

                            if b64_str_metadata.startswith(metadata_string):
                                b64_str = b64_str_metadata[len(metadata_string):]
                            else:
                                b64_str = b64_str_metadata

                            decoded = base64.b64decode(b64_str)

                            st.write("Read sound from Frontend")
                            st.audio(decoded)

                            #save it server side if needed
                            uploaded_file = 'test.wav'
                            with open(uploaded_file,'wb') as f:
                                f.write(decoded)

                            #convert File to wav and save it again
                            wav = AudioSegment.from_file(uploaded_file)
                            getaudio = wav.export(uploaded_file, format="wav")

                            st.write("Read sound by saving in server and reloading file")
                            st.audio(uploaded_file)

                            audiofile_name = uploaded_file
                # ++++++++++++++++

                # https://www.youtube.com/watch?v=BuD3gILJW-Q&ab_channel=Streamlit
                # USE streamlit custom component that implements a custom html/css/react element
                # input data can be passed to this component and it returns data
                # TODO build a component that uses the html/script code of above (for demo webapp rec tool)
                # the component should show up in case the radio button record mic is selected
                # the component should return a path to a audiofile
                # clean existing audio files bevore saving the new audio file! (tmp dictonary)

    # ANALYTICS for Audio File
    if audiofile_name is not None:

        audiofile_path = os.path.join(os.getcwd(), audiofile_name)

        # evaluate whether the input audiofile has changed
        new_audiofile = False # same audiofile --> load from session_state
        if audiofile_name != st.session_state.audiofile_name:
            # update session state and order new calc of attr
            st.session_state.audiofile_name = audiofile_name
            # reset session state for selected amp/rms plot
            st.session_state.spectrum = 'RMS Spectrum'
            new_audiofile = True # new audiofile --> update session sates

        # Musical and Tech Specs Overview
        with st.expander("SECTION - Musical & Technical Specifications",
                         expanded=True):

            # extract technical specifications about wav file
            # no needfor session_state saving bc instant calc
            wav_specs = sf.SoundFile(audiofile_path)
            bit_depth = int(str(wav_specs.subtype)[4:])
            sampling_freq = wav_specs.samplerate
            channels = wav_specs.channels
            frames = wav_specs.frames
            seconds = frames/sampling_freq

            pref_col0, pref_col1, pref_col2, pref_col3 = st.columns([0.2, 1, 1, 1])

            with pref_col1:  # metrics: generating insights on tech specs
                if int(channels) == 1:  # single channel .wav
                    channels = 'MONO'
                elif int(channels) == 2:  # double channel .wav
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
                st.write('')  # add spacing


        # Inspect Audio File Specifications
        with st.expander("SECTION - Waveform and Spectrogram Insights",
                         expanded=False):
            if not advanced_analytics:
                analytics_msg = '<p style="color: #e3fc03; font-size: 1rem;">Only available for audio files provided via "Audio File Upload"</p>'
                st.markdown(analytics_msg, unsafe_allow_html=True)
            if advanced_analytics:  # only if audio file uploaded
                # Generate graphs/plots for RMS & Amplitude over time
                st.audio(audiofile)  # display web audio player UX/UI

                if new_audiofile: # new audiofile --> update session sates
                    # calculate the necessray data for further plotting
                    with st.spinner('calculating spectrogram insights'):
                        # calc spectrum data for plotting framework
                        y,sr = librosa.load(audiofile_path, sr=sampling_freq)
                        y_stft = librosa.stft(y)  # STFT of y
                        scale_db = librosa.amplitude_to_db(np.abs(y_stft), ref=np.max)
                        spectrogram_magn, phase = librosa.magphase(librosa.stft(y))
                        rms = librosa.feature.rms(S=spectrogram_magn)  # calculating rms
                        times = librosa.times_like(rms) #extracting rms timestamps
                        st.session_state.y, st.session_state.sr = y, sr
                        st.session_state.times, st.session_state.rms = times, rms
                else:  # same audiofile --> load from session_state
                    y, sr = st.session_state.y, st.session_state.sr
                    times, rms = st.session_state.times, st.session_state.rms

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

    # initialize session states for plots
    if "plot_spectrum_amp" not in st.session_state:
        st.session_state.plot_spectrum_amp = None
    if "plot_spectrum_rms" not in st.session_state:
        st.session_state.plot_spectrum_rms = None

    # call main function
    beatinspect_main()
