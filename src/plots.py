# PLOTTING FRAMEWORK
import librosa.display
import matplotlib.pyplot as plt

def rms_spectrum(y, sr, times, rms):

    # global plotting settings
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=9)
    plt.rcParams['figure.dpi'] = 400
    plt.rcParams['text.color'] = 'white'

    # create 2x subplots for overview RMS
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
    ax1.set_xlabel('Time [minutes/sec]')
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