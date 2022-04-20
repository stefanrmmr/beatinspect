import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

import React, { ReactNode } from "react"
import AudioReactRecorder, { RecordState } from 'audio-react-recorder'



/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */

class MyComponent extends StreamlitComponentBase<any> {
  constructor(props: any) {
    super(props);

    this.state = {
      recordState: null
    };
  }

  start = () => {
    this.setState({
      recordState: RecordState.START
    })
  }

  stop = () => {
    this.setState({
      recordState: RecordState.STOP
    })
  }

  //audioData contains blob and blobUrl
  onStop = (audioData: any) => {
    console.log('audioData', audioData)
  }

  render() {
    const { recordState } = this.state

    return (
      <div>
        <AudioReactRecorder state={recordState} onStop={this.onStop} />

        <button onClick={this.start}>Start</button>
        <button onClick={this.stop}>Stop</button>
      </div>
    )
  }
}
// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
