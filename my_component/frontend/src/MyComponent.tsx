import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

import React from 'react'

import { Recorder } from 'react-voice-recorder'
import 'react-voice-recorder/dist/index.css'


class MyComponent extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      audioDetails: {
        url: null,
        blob: null,
        chunks: null,
        duration: {
          h: 0,
          m: 0,
          s: 0
        }
      }
    }
  }

  handleAudioStop(data: any) {
    console.log(data);
    this.setState({ audioDetails: data });
  }
  handleAudioUpload(file: any ) {
    console.log(file);
  }
  handleReset() {
    const reset = {
      url: null,
      blob: null,
      chunks: null,
      duration: {
        h: 0,
        m: 0,
        s: 0
      }
    };
    this.setState({ audioDetails: reset });
  }
  render() {
    return (
      <Recorder
        record={true}
        title={"New recording"}
        audioURL={this.state.audioDetails.url}
        showUIAudio
        handleAudioStop={(data: any) => this.handleAudioStop(data)}
        handleAudioUpload={(data: any) => this.handleAudioUpload(data)}
        handleReset={() => this.handleReset()}
        mimeTypeToUseWhenRecording={`audio/webm`}
      />
    )
  }
}

// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
