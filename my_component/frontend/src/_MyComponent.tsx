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

export default AudioRecorder
