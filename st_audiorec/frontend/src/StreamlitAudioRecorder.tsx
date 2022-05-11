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
      //var content = fs.readFileSync('file.ogg');
      //Streamlit.setComponentValue(content)
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

      // **CONCEPT for Data-Handling**
      // fetch blob-object from blob-url
      // convert blob object --> blob base64data
      // convert base64data --> ogg file and save to temp
      // load file from temp and return via st component value

      var xhr = new XMLHttpRequest();
      xhr.open('GET', data.url, true);
      xhr.responseType = 'blob';
      xhr.onload = function(e) {
        if (this.status == 200) {
          var myBlob = this.response;

          // tested: loading the blob from Url: low time consumption
          // tested: initiating new filereader: low time consumption
          // tested: loading blob into filereader: low time consumption
          // tested: converting blob to base64: insane time consumption
          // tested: fetching blob arrayBuffer: insane time consumption

          // info: apparently for larger blob sizes converting to buffer
          // via response constructor is 6x faster than using FileReader

          // info: apparently WAV files take up around 10x more space
          // then equivalent MP3-based files. (.ogg is even smaller)

          // 20sec WAV audio blob --> 4Mb in memory size
          // reading in the whole blob file into memory before processing
          // causes memory overload and lag --> freezes the browser
          // read in the blob in sub-sets/blob chunks to avoid inefficiencies

          // A File objects is also an instance of a Blob,
          // which offers the .slice method to create a smaller view of the file.

          // Split blob into chunks of that are 1kB in size
          var cSize = 1024 /* cSize should be byte 1024*1 = 1KB */
          var createChunks = (myBlob,cSize) => {
            let startPointer = 0;
            let endPointer = myBlob.size;
            let chunks = []; // array of chunks
            while(startPointer<endPointer){
              let newStartPointer = startPointer+cSize;
              chunks.push(myBlob.slice(startPointer,newStartPointer));
              startPointer = newStartPointer;
            }
            return chunks;
          }

          let base64full = ''

          // for alle chunks in createChunks convert und an string adden
          // vor dem add to string "data:audio/wav;base64," vorne entfernen

          for (var i = 0; i < createChunks.length; i++) {
              var chunk = createChunks[i]
              var reader = new FileReader();
              reader.readAsDataURL(chunk)
              reader.onloadend = () => {
                const base64data = reader.result;
                var base64string = String(base64data);
                base64string = base64string.substring(22);
                base64full = base64full + base64string
              }

          Streamlit.setComponentValue(base64full)
          //var reader = new FileReader();
          //reader.readAsDataURL(myBlob)
          //reader.onloadend = () => {
            //const base64data = reader.result;
            //Streamlit.setComponentValue(base64data)
            // data:audio/wav;base64,UklGRiwAAwBXQVZFZm10IBAAAAAB...
            // conversion to base64 works just fine! Milestone achieved lol

            // fs.writeFileSync('file.ogg', Buffer.from(base64data, 'base64'));
          }
        }
      };
      xhr.send();

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
