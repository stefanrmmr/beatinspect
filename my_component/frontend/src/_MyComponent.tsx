import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import 'audio-react-recorder/dist/index.css'


class MyComponent extends StreamlitComponentBase {

  constructor(props) {
    super(props)

    this.state = {
      recordState: null,
      audioData: null
    }
  }

  start = () => {
    this.setState({
      recordState: RecordState.START
    })
  }

  pause = () => {
    this.setState({
      recordState: RecordState.PAUSE
    })
  }

  stop = () => {
    this.setState({
      recordState: RecordState.STOP
    })
  }

  onStop = (data) => {
    this.setState({
      audioData: data
    })
    console.log('onStop: audio data', data)
  }

  public render = (): ReactNode => {

    const name = this.props.args["name"]
    const { recordState } = this.state

    return (
      <div>
        <AudioReactRecorder
          state={recordState}
          onStop={this.onStop}
          backgroundColor='rgb(255,255,255)'
        />
        <audio
          id='audio'
          controls
          src={this.state.audioData ? this.state.audioData.url : null}
        ></audio>
        <button id='record' onClick={this.start}>
          Start
        </button>
        <button id='pause' onClick={this.pause}>
          Pause
        </button>
        <button id='stop' onClick={this.stop}>
          Stop
        </button>
      </div>
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.

// export an object of class MyComponent!
export default withStreamlitConnection(MyComponent)
// You don't need to edit withStreamlitConnection (but you're welcome to!).

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
