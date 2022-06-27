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

def numfmt(x, pos):
    # your custom formatter function: divide by 2
    s = '{}'.format(x / 2)
    return s

def rms_spectrum(times, rms):

    # global plotting settings
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=10)
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['text.color'] = 'white'

    fig, ax2 = plt.subplots(1)
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.0)
    fig.set_size_inches(8, 3, forward=True)

    ax2.vlines(x=[0], ymin=-1, ymax=1, colors='lightgrey', ls='--', lw=0.75)
    ax2.axhline(y=1, color='#e3fc03', linestyle='--', lw=0.75)
    ax2.axhline(y=0.1, color='lightgrey', linestyle='--', lw=0.75)
    ax2.axhline(y=0.01, color='lightgrey', linestyle='--', lw=0.75)

    # AX2 RMS Energy Visualizer
    ax2.semilogy(times, rms[0], label='RMS Energy', color='#e3fc03')

    ax2.patch.set_facecolor('black')
    ax2.patch.set_alpha(0.0)
    ax2.set_ylabel('RMS Energy [log]')
    ax2.set_xlabel('Time [sec]')
    # ax2.xaxis.set_ticks_position('top') # the rest is the same
    # ax2.get_xaxis().set_visible(False)
    ax2.set_ylim(bottom=0.0001)                 # setting lower bounds for y axis
    ax2.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
    ax2.yaxis.label.set_color('white')          #setting up Y-axis label color to blue
    ax2.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
    ax2.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black
    ax2.spines['left'].set_color('white')        # setting up Y-axis tick color to red
    ax2.spines['top'].set_color('white')         #setting up above X-axis tick color to red
    ax2.spines['right'].set_color('white')        # setting up Y-axis tick color to red
    ax2.spines['bottom'].set_color('white')         #setting up above X-axis tick color to red
    ax2.spines['right'].set_visible(False)      # Hide the right and top spines
    # ax2.spines['bottom'].set_visible(False)     # Hide the right and bottom spines

    # change ax2 xlabels to be half the value
    yfmt = tkr.FuncFormatter(numfmt)
    # create your custom formatter function
    ax2.xaxis.set_major_formatter(yfmt)

    plt.tight_layout()
    st.pyplot(fig)


def amp_spectrum(y, sr):

    # global plotting settings
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=10)
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['text.color'] = 'white'

    fig, ax1 = plt.subplots(1)
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.0)
    fig.set_size_inches(8, 3, forward=True)

    # GUIDELINES multiple lines all full height
    ax1.vlines(x=[0], ymin=-1, ymax=1, colors='lightgrey', ls='--', lw=0.75)
    ax1.axhline(y=0.5, color='lightgrey', linestyle='--', lw=0.75)
    ax1.axhline(y=-0.5, color='lightgrey', linestyle='--', lw=0.75)
    ax1.axhline(y=1.0, color='#e3fc03', linestyle='--', lw=0.75)
    ax1.axhline(y=-1.0, color='#e3fc03', linestyle='--', lw=0.75)

    # AX1 wavshow overview spectrogram
    librosa.display.waveshow(y, sr, ax=ax1, color='lightgrey', x_axis='time', label='Time [min]')

    ax1.patch.set_facecolor('black')
    ax1.patch.set_alpha(0.0)
    ax1.set_ylabel('Amplitude')
    ax1.set_xlabel('Time [minutes:sec]')
    ax1.set_ylim([-1.1, 1.1])
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

    plt.tight_layout()
    st.pyplot(fig)


def amprms_spectrum(y, sr, times, rms):

    # global plotting settings
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=9)
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['text.color'] = 'white'

    fig, (ax1, ax2) = plt.subplots(2)
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.0)
    #fig.set_size_inches(8, 10, forward=True)

    # GUIDELINES multiple lines all full height
    ax1.vlines(x=[0], ymin=-1, ymax=1, colors='lightgrey', ls='--', lw=0.75)
    ax1.axhline(y=0.5, color='lightgrey', linestyle='--', lw=0.75)
    ax1.axhline(y=-0.5, color='lightgrey', linestyle='--', lw=0.75)
    ax1.axhline(y=1.0, color='#e3fc03', linestyle='--', lw=0.75)
    ax1.axhline(y=-1.0, color='#e3fc03', linestyle='--', lw=0.75)

    ax2.vlines(x=[0], ymin=-1, ymax=1, colors='lightgrey', ls='--', lw=0.75)
    ax2.axhline(y=1, color='#e3fc03', linestyle='--', lw=0.75)
    ax2.axhline(y=0.1, color='lightgrey', linestyle='--', lw=0.75)
    ax2.axhline(y=0.01, color='lightgrey', linestyle='--', lw=0.75)

    # AX1 wavshow overview spectrogram
    librosa.display.waveshow(y, sr, ax=ax1, color='grey', x_axis='time', label='Time [min]')

    ax1.patch.set_facecolor('black')
    ax1.patch.set_alpha(0.0)
    ax1.set_ylabel('Amplitude')
    ax1.set_xlabel('Time [minutes:sec]')
    ax1.set_ylim([-1.1, 1.1])
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

    # AX2 RMS Energy Visualizer
    ax2.semilogy(times, rms[0], label='RMS Energy', color='#e3fc03')

    ax2.patch.set_facecolor('black')
    ax2.patch.set_alpha(0.0)
    ax2.set_ylabel('RMS Energy [log]')
    ax2.xaxis.set_ticks_position('top') # the rest is the same
    ax2.get_xaxis().set_visible(False)
    ax2.set_ylim(bottom=0.0001)                 # setting lower bounds for y axis
    ax2.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
    ax2.yaxis.label.set_color('white')          #setting up Y-axis label color to blue
    ax2.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
    ax2.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black
    ax2.spines['left'].set_color('white')        # setting up Y-axis tick color to red
    ax2.spines['top'].set_color('white')         #setting up above X-axis tick color to red
    ax2.spines['right'].set_color('white')        # setting up Y-axis tick color to red
    ax2.spines['bottom'].set_color('white')         #setting up above X-axis tick color to red
    ax2.spines['right'].set_visible(False)      # Hide the right and top spines
    ax2.spines['bottom'].set_visible(False)     # Hide the right and bottom spines

    plt.tight_layout()
    st.pyplot(fig)


def melspectrogram_plotly3d(y, sr, mark_peaks, camera_mode_3d, zvalue_treshold):

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
