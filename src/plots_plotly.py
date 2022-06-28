# PLOTTING FRAMEWORK
import streamlit as st
import contextlib
import numpy as np
import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import plotly.graph_objects as go
# has classes for tick-locating and -formatting

streamlit_dark = 'rgb(15,17,22)'  # #0F1116' default dark theme

def melspectrogram_plotly3d(y, sr, sec_offset, mark_peaks, camera_mode_3d, zvalue_treshold):

    mels_count = 300
    max_freq = 32768  # Hz
    # zvalue_treshold = -15  # dB
    # mark_peaks = False
    # camera_mode_3d = False

    # calc playtime duration in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    # Passing through arguments to the Mel filters
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=mels_count, fmax=max_freq)
    # decibel is measured using the np.max(S) value as a reference point
    mel_data = librosa.power_to_db(S, ref=np.max) # convert spectrum to dB

    # data for plotting spectrogram with log scale instead of mel
    log_data = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    # caculate sample points for adequate tick labels in plot
    xvalues_count, yvalues_count = len(mel_data[0]), len(mel_data)  # 764, 200

    # flat surface on level of zvalue treshold
    flat_data = np.full((len(mel_data), len(mel_data[0])), zvalue_treshold)


    # PLOT CONFIG
    config = {'displayModeBar': True, 'displaylogo': False,
              'modeBarButtonsToRemove': ['orbitRotation',
                                         'resetCameraDefault3d']}

    layout = go.Layout(  # layout of spikes that visualize cursor
        scene=go.layout.Scene(  # position on 3D plot side walls
            xaxis = go.layout.scene.XAxis(showspikes=True, color='white'),
            yaxis = go.layout.scene.YAxis(showspikes=True, color='white'),
            zaxis = go.layout.scene.ZAxis(showspikes=False)))

    if (camera_mode_3d == False):
        # 3D camera positioning: TOP VIEW
        camera = dict(up=dict(x=1, y=0, z=0),
                      center=dict(x=0, y=0, z=0),
                      eye=dict(x=0, y=0, z=1))
    if (camera_mode_3d == True):
        # 3D camera positioning: PERSPECTIVE VIEW
        camera = dict(up=dict(x=0, y=0, z=0),
                      center=dict(x=0, y=0, z=0),
                      eye=dict(x=1, y=1, z=0.8))

    # create custom colorscale for surfaceplot
    colorscale_melspectrum = [[0, 'rgb(0,0,0)'],
                              [0.005, 'rgb(100,100,100)'],
                              [0.01, 'rgb(0,0,0)'],
                              [0.3, 'rgb(30,30,30)'],
                              [0.4, 'rgb(50,50,50)'],
                              [0.5, 'rgb(80,80,80)'],
                              [0.75, 'rgb(227, 252, 3)'],
                              [0.9, 'rgb(227, 252, 3)'],
                              [0.975, 'rgb(255,255,255)'],
                              [1, 'rgb(255,255,255)']]

    # create custom colorscale for surfaceplot
    colorscale_flat = [[0, 'white'],[1, 'white']]

    # contour height level rings for values > treshold
    contours = {"z": {"show": mark_peaks, "start": zvalue_treshold,
                      "end": 0, "size": 1, "color":"black"}}

    # CALC correct 3D MEl Spectrogram X-AXIS Tick label texts & positions
    x_tickvals, x_ticktext = [], []
    timestep = duration/(10)  # 10x timeslots
    xvaluestep = xvalues_count/(10)  # 10x timeslots
    xvalue, timevalue = 0, 0
    while (xvalue < xvalues_count):
        x_tickvals.append(round(xvalue,2))
        x_ticktext.append(round(timevalue,2))
        xvalue += xvaluestep
        timevalue += timestep

    # FACTOR IN OFFSET from timeframe selection
    [x + sec_offset for x in x_ticktext]


    # CALC correct 3D MEl Spectrogram Y-AXIS Tick label texts & positions
    y_tickvals, yvalue = [], 0
    y_ticktext = ["0", "512", "1024", "2048", "4096", "8192", "16384", "32768"]
    while (yvalue <= yvalues_count+1):
        y_tickvals.append(round(yvalue,1))
        yvalue += (yvalues_count/7)


    # PLOTLY GRPAH OBJECT GENERATE PLOT
    if (mark_peaks == True):  # plot surface using selected colorscheme, layout and contours
        fig = go.Figure(data=[go.Surface(z=mel_data,
                                         showscale=True, colorscale=colorscale_melspectrum,
                                         #hovertemplate='<br>%{x} sec<br>%{y} Hz<br>%{z} dB<extra></extra>',
                                         hovertemplate='<br>%{z} dB<extra></extra>',
                                         opacity=1, contours=contours), # colormapped opaque surface
                              go.Surface(z=flat_data, name=f'<br>amplitude<br>treshold',
                                         # name=f'<br>amplitude<br>treshold<br>{zvalue_treshold} dB',
                                         showscale=False, colorscale=colorscale_flat,
                                         # hovertemplate='<br>%{x} sec<br>%{y} Hz<br>%{z} dB',
                                         hovertemplate='<br>%{z} dB',
                                         opacity=0.4)], layout=layout)  # translucent flat surface

    if (mark_peaks == False):  # plot surface using selected colorscheme, layout and contours
        fig = go.Figure(data=[go.Surface(z=mel_data,
                                         showscale=True, colorscale=colorscale_melspectrum,
                                         #hovertemplate='<br>%{x} sec<br>%{y} Hz<br>%{z} dB<extra></extra>',
                                         hovertemplate='<br>%{z} dB<extra></extra>',
                                         opacity=1, contours=contours)], layout=layout)

    # background and axis label colors and dimensions
    fig.update_layout(autosize=True, width=950, height=600,
                      margin=dict(t=0, r=0, l=20, b=0),  # margins
                      paper_bgcolor=streamlit_dark,  # rgb(15,17,22)
                      font_family= 'Arial', # "Courier New",
                      font_color="white",
                      legend_title_font_color="white")

    # replace perspective camera with orthogonal view
    fig.layout.scene.camera.projection.type = "orthographic"
    # turntable view of defined camera position
    fig.update_layout(scene_aspectmode='manual',
                      scene_camera=camera,
                      dragmode = "turntable",
                      scene_aspectratio=dict(x=1.5, y=1, z=0.75),

                      scene_zaxis = dict(
                        gridcolor="rgb(055, 055, 055)",
                        showbackground=True,
                        backgroundcolor=streamlit_dark,
                        title = 'Volume [dB]'),

                      scene_xaxis = dict(
                        gridcolor="rgb(055, 055, 055)",
                        showbackground=True,
                        backgroundcolor=streamlit_dark,
                        title = 'Time [secs]',
                        tickvals = x_tickvals,
                        ticktext = x_ticktext,
                        tickangle = 45),

                      scene_yaxis = dict(
                        gridcolor="rgb(055, 055, 055)",
                        showbackground=True,
                        backgroundcolor=streamlit_dark,
                        title = 'Frequency [Hz]',
                        tickvals = y_tickvals,
                        ticktext = y_ticktext)
                     )

    # enable x-axis traces without permanent projection
    fig.update_traces(contours_x=dict(show=False, usecolormap=False,
                                      highlightcolor= "#e3fc03", #"#ff008d",
                                      highlightwidth=15, project_x=True))

    # define colorbar attributes
    fig.data[0].colorbar.title = "Amp [dB]"  # title text
    fig.data[0].colorbar.orientation = "v"  # orientation
    fig.data[0].colorbar.thickness = 25  # colorbar width
    fig.data[0].colorbar.len = 0.6  # colorbar length

    st.plotly_chart(fig, use_container_width=True, config=config)
