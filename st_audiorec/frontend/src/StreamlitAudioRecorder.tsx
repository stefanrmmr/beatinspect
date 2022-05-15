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
          let cSize = 1024*10; // chunksize 10kB
          var base64full = ''; // final base64 string
          var base64string = ''; // substring for one chunk
          let startPointer = 44; // start after WAV header
          let endPointer = myBlob.size;
          let endReached = false;

          var wavHeader44byte = myBlob.slice(0, 44); // first 44 bytes
          // the end byte is NOT included (exclusive byte44)

          while(startPointer<endPointer){
            // initiate start chunk pointer
            let newStartPointer = startPointer+cSize;
            if (newStartPointer > endPointer){
              // in case all chunks have been processed
              newStartPointer = endPointer;
              endReached = true;
            };

            // **BAUSTELLE 1**
            // slice out one chunk from the initial WAV-Blob
            // concatenate sliced out chunk with header bytes

            // var chunk = new Blob([myBlob.slice(startPointer, newStartPointer, 'audio/wav')]);
            var chunkAudio = myBlob.slice(startPointer, newStartPointer, 'audio/wav');
            // var chunkAudio = new Blob([wavHeader44byte, chunk], { type: "audio/wav" });
            // var chunkAudio = new Blob([wavHeader44byte, chunk]);

            var reader = new FileReader(); // initiate file reader
            reader.readAsDataURL(chunkAudio); // read in the chunk
            reader.onloadend = () => {
              var base64data = reader.result;
              // export chunk to string of base64 WAV Audio including header
              base64string = String(base64data);




              // **BAUSTELLE 2**
              // concatenate two base64 strings

              // ATTEMPT REMOVE BASE64
              // remove base64 WAV header "data:audio/wav;base64,"
              var base64stringArr = base64string.split(',');
              //base64string = base64string.substring(22);
              base64string = base64stringArr[1];

              if (base64full == ''){
                base64full = base64string;
              } else {
                // both need to be header free before
                //var bothData = atob(base64full) + atob(base64string); // binary string
                // var bothData64 = btoa(bothData); // base64 encoded
                //base64full = //version of bothData64 without the header
                // base64full = bothData64;
                base64full = base64full + base64string;
              };


              // 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



              /*
              // ATTEMPT CONCAT BASE64 main
              if (base64full == ''){
                base64full = base64string;
              } else {

                // convert base64full to ArrayBuffer
                var myB64Data1  = base64full.split(',');
                var myB64Chunk1 = myB64Data1[1];
                var binary_string1 = window.atob(myB64Chunk1);
                var len1 = binary_string1.length;
                var bytes1 = new Uint8Array(len1);
                for (var i = 0; i < len1; i++) {
                    bytes1[i] = binary_string1.charCodeAt(i);
                  }
                var myBuffer1 = bytes1.buffer;

                // convert base64string to ArrayBuffer
                var myB64Data2  = base64string.split(',');
                var myB64Chunk2 = myB64Data2[1];
                var binary_string2 = window.atob(myB64Chunk2);
                var len2 = binary_string2.length;
                var bytes2 = new Uint8Array(len2);
                for (var j = 0; j < len2; j++) {
                    bytes2[i] = binary_string2.charCodeAt(j);
                  }
                var myBuffer2 = bytes2.buffer;

                Streamlit.setComponentValue('test_buffers');

                // create final full array buffer
                var myFinalBuffer = new Uint8Array(myBuffer1.byteLength + myBuffer2.byteLength);
                myFinalBuffer.set(new Uint8Array(myBuffer1), 0);
                myFinalBuffer.set(new Uint8Array(myBuffer2), myBuffer1.byteLength);

                Streamlit.setComponentValue('test_buffers_concat');


                var options = {isFloat: false, numChannels: 2, sampleRate: 44100}

                const type = options.isFloat ? Float32Array : Uint16Array
                const numFrames = myFinalBuffer.byteLength / type.BYTES_PER_ELEMENT

                options = Object.assign({}, options, { numFrames })

                const numChannels =    options.numChannels || 2;
                const sampleRate =     options.sampleRate || 44100;
                const bytesPerSample = options.isFloat? 4 : 2;
                const format =         options.isFloat? 3 : 1;

                const blockAlign = numChannels * bytesPerSample;
                const byteRate = sampleRate * blockAlign;
                const dataSize = numFrames * blockAlign;

                const bufferHeader = new ArrayBuffer(44);
                const dv = new DataView(bufferHeader);

                let p = 0;
                let s = '';

                s = 'RIFF'; // ChunkID
                for (let i = 0; i < s.length; i++) {
                  dv.setUint8(p + i, s.charCodeAt(i));};
                p += s.length;

                dv.setUint32(p, (dataSize + 36), true);
                p += 4; // ChunkSize

                s = 'WAVE'; // Format
                for (let i = 0; i < s.length; i++) {
                  dv.setUint8(p + i, s.charCodeAt(i));};
                p += s.length;

                s = 'fmt '; // Subchunk1ID
                for (let i = 0; i < s.length; i++) {
                  dv.setUint8(p + i, s.charCodeAt(i));};
                p += s.length;

                dv.setUint32(p, 16, true);
                p += 4; // Subchunk1Size

                dv.setUint16(p, format, true);
                p += 2; // AudioFormat

                dv.setUint16(p, numChannels, true);
                p += 2; // NumChannels

                dv.setUint32(p, sampleRate, true);
                p += 4; // SampleRate

                dv.setUint32(p, byteRate, true);
                p += 4; // ByteRate

                dv.setUint16(p, blockAlign, true);
                p += 2; // BlockAlign

                dv.setUint16(p, (bytesPerSample * 8), true);
                p += 2; // BitsPerSample

                s = 'data'; // Subchunk2ID
                for (let i = 0; i < s.length; i++) {
                  dv.setUint8(p + i, s.charCodeAt(i));};
                p += s.length;

                dv.setUint32(p, dataSize, true);
                p += 4; // Subchunk2Size

                const headerBytes = new Uint8Array(bufferHeader);
                const wavBytes = new Uint8Array(headerBytes.length + myFinalBuffer.byteLength);

                // prepend header, then add pcmBytes
                wavBytes.set(headerBytes, 0)
                wavBytes.set(new Uint8Array(myFinalBuffer), headerBytes.length)

                myFinalBuffer = wavBytes;

                var binary = '';
                var bytes = new Uint8Array(myFinalBuffer);
                var len = bytes.byteLength;
                for (var k = 0; k < len; k++) {
                   binary += String.fromCharCode(bytes[k]);
                 };
                base64full = window.btoa(binary);

              }; // close else
              */


              // update current status of base64full after every iteration
              // keep the setComponentValue statement within the filereader!
              if (endReached){
                // fs.writeFileSync('file.ogg', Buffer.from(base64data, 'base64'));
                // base64full is returned WITHOUT the base64 header "data:audio/wav;base64,"
                Streamlit.setComponentValue(base64full);
              }
            };
            //update chunk pointer
            startPointer = newStartPointer;
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
