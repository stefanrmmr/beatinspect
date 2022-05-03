import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import 'audio-react-recorder/dist/index.css'

interface State {
  isFocused: boolean
  recordState: null
  audioDataURI: string
  reset: boolean
}

class StAudioRec extends StreamlitComponentBase<State> {
  public state = { isFocused: false, recordState: null, audioDataURI: '', reset: false}

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    const { recordState } = this.state

    // compatibility with older vers of Streamlit that don't send theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.state.isFocused ? theme.primaryColor : "gray"}`
      style.border = borderStyling
      style.outline = borderStyling
    }

    return (
      <span>
        <div>
          <button id='record' onClick={this.onClick_start}>
            Start Recording
          </button>
          <button id='stop' onClick={this.onClick_stop}>
            Stop
          </button>
          <button id='reset' onClick={this.onClick_reset}>
            Reset
          </button>

          <AudioReactRecorder
            state={recordState}
            onStop={this.onStop_audio}
            type='audio/wav'
            backgroundColor='rgb(15, 17, 22)'
            foregroundColor='rgb(227, 252, 3)'
            canvasWidth={450}
            canvasHeight={100}
          />

          <audio
            id='audio'
            controls
            src={this.state.audioDataURI}
          />

          <button id='continue' onClick={this.onClick_continue}>
            Continue to Analysis
          </button>

        </div>
      </span>
    )
  }

  private onClick_start = () => {
    this.setState({
      reset: false,
      audioDataURI: '',
      recordState: RecordState.START
    })
    Streamlit.setComponentValue('')
  }

  private onClick_stop = () => {
    this.setState({
      reset: false,
      recordState: RecordState.STOP
    })
  }

  private onClick_reset = () => {
    this.setState({
      reset: true,
      audioDataURI: '',
      recordState: RecordState.STOP
    })
    Streamlit.setComponentValue('')
  }

  private onClick_continue = () => {
    if (this.state.audioDataURI !== '')
    {
      Streamlit.setComponentValue(this.state.audioDataURI)
    }
  }

  private downloadBlob(blob, name = 'file.txt') {
    // Convert your blob into a Blob URL (a special url that points to an object in the browser's memory)
    const blobUrl = URL.createObjectURL(blob);

    // Create a link element
    const link = document.createElement("a");

    // Set link's href to point to the Blob URL
    link.href = blobUrl;
    link.download = name;

    // Append link to the body
    document.body.appendChild(link);

    // Dispatch click event on the link
    // This is necessary as link.click() does not work on the latest firefox
    link.dispatchEvent(
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
      })
    );

    // Remove link from body
    document.body.removeChild(link);
  }

  private onStop_audio = (data) => {
    if (this.state.reset === true)
    {
      this.setState({
        audioDataURI: ''
      })
      Streamlit.setComponentValue('')
    }else{

      // Usage
      this.downloadBlob(data, 'audiofile.wav');

      this.setState({
        // the URI is a link to the audio data stored in the browser cache
        // the URI is sandboxed to the client browser that created the blob
        // the URI is can not be converted to a normal URL/download link
        // use an AJAX request to pull blob content from the browser memory
        audioDataURI: data.url
      })
    }

  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(StAudioRec)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
