import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

import React from "react"
import { ReactMediaRecorder } from "react-media-recorder";

const AudioRecorder = () => (
  <div>
    <ReactMediaRecorder
      audio
      render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
        <div>
          <p>{status}</p>
          <button onClick={startRecording}>Start Recording</button>
          <button onClick={stopRecording}>Stop Recording</button>
          <audio src={mediaBlobUrl} controls autoPlay loop />
        </div>
      )}
    />
  </div>
);

// export an object of class MyComponent!
export default withStreamlitConnection(AudioRecorder)
// You don't need to edit withStreamlitConnection (but you're welcome to!).

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()
