import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import 'audio-react-recorder/dist/index.css'

import * as fs from 'fs'


//import { FilesManager } from 'turbodepot-node';



interface State {
  isFocused: boolean
  recordState: null
  audioDataURL: string
  reset: boolean
}

class StAudioRec extends StreamlitComponentBase<State> {
  public state = { isFocused: false, recordState: null, audioDataURL: '', reset: false}

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
            src={this.state.audioDataURL}
          />

          <button id='continue' onClick={this.onClick_continue}>
            Continue to Analysis
          </button>

        </div>
      </span>
    )
  }

  private blobToBase64 = blob => {
    return new Promise((resolve, _) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.readAsDataURL(blob);
    });
  };

  private sendAudioFile = file => {
    const formData = new FormData();
    formData.append('audio-file', file);
    return fetch('http://localhost:3000/audioUpload', {
      method: 'POST',
      body: formData
    });
  };

  private onClick_start = () => {
    this.setState({
      reset: false,
      audioDataURL: '',
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
      audioDataURL: '',
      recordState: RecordState.STOP
    })
    Streamlit.setComponentValue('')
  }

  private onClick_continue = () => {
    if (this.state.audioDataURL !== '')
    {
      // NOT WORKING THO: --> see python code notes
      // return a string to the blob content
      //var blob_url = String(this.state.audioDataURL)
      //Streamlit.setComponentValue(blob_url.substring(5))

      var content = fs.readFileSync('file.ogg');
      Streamlit.setComponentValue(content)


      // 1. fetch content from blob url directly
      // 2. store content in tmp folder as files
      // 3. convert audioblob --> arraybuffer --> audiobuffer --> wav files
      // 4. get url of file stored in tmp folder and hand it to python
      // 5. maybe also hand the file directly to python?

      //let filesManager = new FilesManager();
      //const temp_path = filesManager.createTempDirectory('temp-dir-name');

      //Streamlit.setComponentValue(String(temp_path))
    }
  }

  private onStop_audio = (data) => {
    if (this.state.reset === true)
    {
      this.setState({
        audioDataURL: ''
      })
      Streamlit.setComponentValue('')
    }else{
      this.setState({
        audioDataURL: data.url
      })

      // var base64data = this.blobToBase64(data)

      var reader = new FileReader();
      reader.readAsDataURL(data.url);
      reader.onloadend = () => {
        // @ts-ignore: Object is possibly 'null'.
        var base64data = reader.result;
        //log of base64data is "data:audio/ogg; codecs=opus;base64,GkX..."
        // @ts-ignore: Object is possibly 'null'.
        fs.writeFileSync('file.ogg', Buffer.from(base64data.replace('data:audio/ogg; codecs=opus;base64,', ''), 'base64'));


      }


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
