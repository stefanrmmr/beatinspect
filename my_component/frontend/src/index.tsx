import React from "react"
import ReactDOM from "react-dom"
import MyComponent from "./MyComponent"
import AudioRecorder from "./codex2"

ReactDOM.render(
  <React.StrictMode>
    <MyComponent />
    <AudioRecorder />
  </React.StrictMode>,
  document.getElementById("root")
)
