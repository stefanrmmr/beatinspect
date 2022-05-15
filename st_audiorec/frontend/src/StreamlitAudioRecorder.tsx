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

  //





  //


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
                Streamlit.setComponentValue('test_buffers1');
                myFinalBuffer.set(new Uint8Array(myBuffer1), 0);
                Streamlit.setComponentValue('test_buffers2');
                myFinalBuffer.set(new Uint8Array(myBuffer2), myBuffer1.byteLength);

                Streamlit.setComponentValue('test_buffers3');


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



              };



              /*// remove base64 WAV header "data:audio/wav;base64,"
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
              };*/


              // update current status of base64full after every iteration
              // keep the setComponentValue statement within the filereader!
              if (endReached){
                // fs.writeFileSync('file.ogg', Buffer.from(base64data, 'base64'));
                // base64full is returned WITHOUT the base64 header "data:audio/wav;base64,"
                // Streamlit.setComponentValue(base64full);
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
