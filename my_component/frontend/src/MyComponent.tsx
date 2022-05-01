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
  audioDataUrl: string
  reset: boolean
}

class MyComponent extends StreamlitComponentBase<State> {
  public state = { isFocused: false, recordState: null, audioDataUrl: '', reset: false}

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.

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
          <AudioReactRecorder
            state={recordState}
            onStop={this.onStop_audio}
            backgroundColor='rgb(255,255,255)'
          />

          <audio
            id='audio'
            controls
            src={this.state.audioDataUrl}
          ></audio>

          <button id='record' onClick={this.onClick_start}>
            Start
          </button>
          <button id='stop' onClick={this.onClick_stop}>
            Stop
          </button>
          <button id='reset' onClick={this.onClick_reset}>
            Reset
          </button>

        </div>
      </span>
    )
  }

  private onClick_start = () => {
    this.state.reset = false
    this.setState({
      recordState: RecordState.START
    })
  }

  private onClick_stop = () => {
    this.state.reset = false
    this.setState({
      recordState: RecordState.STOP
    })
  }

  private onClick_reset = () => {
    this.state.reset = true
    this.setState({
      recordState: RecordState.STOP,
    }) // stop recording
    this.setState({
      audioDataUrl: ''
    })
    Streamlit.setComponentValue(this.state.audioDataUrl)
  }

  private onStop_audio = (data) => {
    if (this.state.reset)
    {
      this.setState({
        audioDataUrl: ''
      })
      Streamlit.setComponentValue(this.state.audioDataUrl)
    }else{
      this.setState({
        audioDataUrl: data.url
      })
      Streamlit.setComponentValue(this.state.audioDataUrl)
    }

  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
