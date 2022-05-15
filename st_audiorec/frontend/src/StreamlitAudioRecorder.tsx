import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import 'audio-react-recorder/dist/index.css'

// import * as fs from 'fs'
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

      // tested: loading the blob from Url: low time consumption
      // tested: initiating new filereader: low time consumption
      // tested: loading blob into filereader: low time consumption
      // tested: splitting blob into chunks: low time consumption
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

      var xhr = new XMLHttpRequest();
      xhr.open('GET', data.url, true);
      xhr.responseType = 'blob';
      xhr.onload = function(e) {
        if (this.status == 200) {
          var myBlob = this.response;

          // PROCESSING APPROACH A: all at once
          /*var reader = new FileReader();
          reader.readAsDataURL(myBlob);
          reader.onloadend = () => {
            const base64data = reader.result;
            base64string = String(base64data);
            base64string = base64string.substring(22);
            Streamlit.setComponentValue(base64string);
          }*/

          // PROCESSING APPROACH B:
          let cSize = 1024*100; // chunksize 100kB
          var base64full = ''; // final base64 string
          var base64string = ''; // substring for one chunk
          let startPointer = 44; // start after WAV header
          let endPointer = myBlob.size;
          let endReached = false;

          var wavHeader44byte = myBlob.slice(0, 43); // first 44 bytes

          while(startPointer<endPointer){
            // initiate start chunk pointer
            let newStartPointer = startPointer+cSize-1;
            if (newStartPointer > endPointer){
              // in case all chunks have been processed
              newStartPointer = endPointer;
              endReached = true;
            };

            // **BAUSTELLE 1**
            // slice out one chunk from the initial WAV-Blob
            // concatenate sliced out chunk with header bytes

            // var chunk = new Blob([myBlob.slice(startPointer, newStartPointer, 'audio/wav')]);
            var chunk = myBlob.slice(startPointer, newStartPointer);
            var chunkAudio = new Blob([wavHeader44byte, chunk], { type: "audio/wav" });

            var reader = new FileReader(); // initiate file reader
            reader.readAsDataURL(chunkAudio); // read in the chunk
            reader.onloadend = () => {
              var base64data = reader.result;
              // export chunk to string of base64 WAV Audio including header
              base64string = String(base64data);
              // remove base64 WAV header "data:audio/wav;base64,"
              base64string = base64string.substring(22);


              // **BAUSTELLE 2**
              // concatenate two base64 strings
              // ? or export as arraybuffers that are concatenated and then transformed to base64

              if (base64full == ''){
                base64full = base64string;
              } else {

                var bothData = atob(base64full) + atob(base64string); // binary string
                var bothData64 = btoa(bothData); // base64 encoded
                //base64full = //version of bothData64 without the header
                base64full = bothData64;
              }






              // update current status of base64full after every iteration
              // keep the setComponentValue statement within the filereader!
              if (endReached){
                // fs.writeFileSync('file.ogg', Buffer.from(base64data, 'base64'));
                // base64full is returned WITHOUT the base64 header "data:audio/wav;base64,"
                Streamlit.setComponentValue(base64full);
              }
            };
            //update chunk pointer
            startPointer = newStartPointer+1;
          };

        };
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
