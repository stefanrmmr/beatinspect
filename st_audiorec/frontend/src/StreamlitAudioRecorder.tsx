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
            var chunk = myBlob.slice(startPointer, newStartPointer, 'audio/wav');
            var chunkAudio = new Blob([wavHeader44byte, chunk], { type: "audio/wav" });
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


              //NaNUklGRixgAwBXQVZFZm10IBAAAAABAAIARKwAABCxAgAEABAAZGF0YQBgAwDD/8P/uP+4/6//r/+m/6b/nP+c/4//j/+F/4X/f/9//37/fv9+/37/e/97/3b/dv90/3T/eP94/37/fv+G/4b/i/+L/4//j/+V/5X/nP+c/6L/ov+s/6z/uP+4/77/vv/C/8L/xf/F/8v/y//W/9b/3v/e/97/3v/a/9r/2P/Y/9n/2f/Z/9n/1//X/9D/0P/D/8P/tv+2/7D/sP+r/6v/pf+l/5//n/+U/5T/g/+D/3b/dv9x/3H/cP9w/23/bf9o/2j/Xf9d/1L/Uv9Q/1D/Vv9W/2D/YP9m/2b/Zf9l/2T/ZP9v/2//fv9+/4f/h/+Q/5D/nP+c/6f/p/+y/7L/vv++/87/zv/g/+D/6v/q/+n/6f/l/+X/5//n//D/8P/2//b/8v/y/+T/5P/S/9L/yf/J/8r/yv/K/8r/v/+//6f/p/+Q/5D/hv+G/4j/iP+H/4f/ev96/2r/av9g/2D/W/9b/1v/W/9e/17/ZP9k/2j/aP9q/2r/bv9u/3r/ev+P/4//pP+k/7H/sf+5/7n/w//D/9X/1f/t/+3/AQABAAoACgAJAAkACAAIAAsACwASABIAGgAaAB8AHwAaABoACgAKAPv/+//1//X/9//3//f/9//t/+3/3f/d/8z/zP/G/8b/yv/K/8z/zP/E/8T/tf+1/6j/qP+k/6T/rP+s/7j/uP+//7//v/+//77/vv/D/8P/0f/R/+b/5v/4//j/AAAAAAIAAgAIAAgAFQAVACgAKAA6ADoAQQBBADwAPAA4ADgAPQA9AEkASQBVAFUAXABcAFkAWQBPAE8ASABIAEkASQBNAE0ATwBPAEoASgBBAEEAOgA6ADcANwA6ADoAPQA9ADcANwAoACgAHAAcABkAGQAgACAAKAAoACgAKAAaABoADAAMAA0ADQAZABkAJQAlACkAKQAiACIAGgAaABsAGwArACsAPgA+AEwATABPAE8ATQBNAFAAUABbAFsAbwBvAIcAhwCTAJMAkACQAIoAigCNAI0AmACYAKgAqACuAK4ApQClAJgAmACRAJEAkQCRAJIAkgCJAIkAdgB2AGEAYQBYAFgAVgBWAFIAUgBHAEcANQA1ACUAJQAeAB4AHAAcABwAHAAiACIAIwAjABwAHAAWABYAGgAaACcAJwA5ADkARQBFAEsASwBRAFEAWgBaAGUAZQB4AHgAjACMAJUAlQCTAJMAjQCNAJEAkQCeAJ4ApACkAKAAoACUAJQAiACIAH0AfQB5AHkAfQB9AHkAeQBoAGgAUgBSAD8APwA1ADUAMQAxAC0ALQAkACQAFgAWAAoACgACAAIAAgACAAgACAALAAsAAwADAPn/+f/1//X//P/8/woACgAUABQAFAAUABQAFAAaABoAJQAlADQANABAAEAAQABAADoAOgA8ADwARABEAFEAUQBdAF0AXgBeAFUAVQBMAEwARwBHAEkASQBOAE4ATgBOAEIAQgAuAC4AHQAdABgAGAAaABoAEQARAP3//f/r/+v/4//j/+L/4v/h/+H/3P/c/8//z//B/8H/uf+5/7z/vP/G/8b/0f/R/8//z//H/8f/w//D/8n/yf/c/9z/9P/0/wEAAQAAAAAAAAAAAAgACAAaABoANAA0AEUARQBGAEYAQABAADwAPAA9AD0AQwBDAEgASAA/AD8ALgAuACEAIQAVABUACAAIAPz//P/s/+z/2f/Z/8X/xf+2/7b/qv+q/6D/oP+Z/5n/j/+P/37/fv9y/3L/cf9x/3b/dv+A/4D/iP+I/4z/jP+N/43/kv+S/6D/oP+z/7P/xv/G/9T/1P/c/9z/5f/l//X/9f8IAAgAFQAVABUAFQAPAA8AEAAQABcAFwAaABoAGAAYAA4ADgAAAAAA9f/1/+z/7P/j/+P/2f/Z/8v/y/+2/7b/ov+i/5X/lf+Q/5D/kv+S/5L/kv+I/4j/ev96/3b/dv+A/4D/kP+Q/5n/mf+T/5P/jP+M/5L/kv+g/6D/q/+r/7T/tP+2/7b/tP+0/7b/tv+9/73/yv/K/9r/2v/d/93/0v/S/83/zf/U/9T/2//b/97/3v/i/+L/4f/h/9n/2f/Q/9D/yv/K/8z/zP/P/8//wv/C/6v/q/+m/6b/qv+q/6X/pf+Z/5n/jf+N/4T/hP+C/4L/gP+A/3v/e/92/3b/cP9w/2T/ZP9d/13/Zf9l/27/bv9z/3P/d/93/3r/ev94/3j/ev96/4b/hv+Y/5j/pv+m/6r/qv+s/6z/t/+3/8r/yv/Y/9j/4v/i/+r/6v/u/+7/7//v//P/8//6//r//f/9//b/9v/q/+r/3P/c/9D/0P/H/8f/wf/B/7z/vP+v/6//m/+b/43/jf+H/4f/gP+A/3b/dv9n/2f/W/9b/1n/Wf9d/13/Yv9i/27/bv95/3n/dv92/23/bf90/3T/if+J/6D/oP+z/7P/uv+6/7v/u//I/8j/4f/h//f/9/8GAAYACQAJAAIAAgAFAAUAFAAUAB8AHwAhACEAGQAZAA8ADwAJAAkACQAJAAgACAAKAAoABwAHAPX/9f/e/97/1v/W/9n/2f/f/9//2//b/8v/y/+8/7z/v/+//8j/yP/S/9L/2//b/9v/2//Z/9n/4v/i//L/8v8FAAUAFgAWABwAHAAdAB0AIwAjACoAKgA1ADUASQBJAFUAVQBRAFEATwBPAFgAWABoAGgAdQB1AHsAewB2AHYAcQBxAHQAdACBAIEAjgCOAIsAiwB5AHkAbABsAGgAaABoAGgAZgBmAFsAWwBQAFAASwBLAEQARAA7ADsANQA1ADMAMwAmACYAFQAVAAsACwAJAAkAEAAQABgAGAAYABgAGAAYABsAGwAcABwAKwArAEcARwBdAF0AagBqAHUAdQB/AH8AjQCNAKIAogC1ALUAwADAAMgAyADMAMwAzADMANEA0QDUANQA1wDXANkA2QDWANYA0ADQAMQAxAC3ALcArgCuAKYApgCRAJEAdAB0AF0AXQBRAFEAUABQAE8ATwBDAEMAMQAxACQAJAAhACEAKgAqADAAMAAoACgAJAAkADQANABRAFEAbgBuAH4AfgCHAIcAkwCTAKAAoACpAKkAtAC0AMQAxADRANEA1ADUANoA2gDhAOEA5gDmAOcA5wDeAN4AxQDFAKoAqgCgAKAApQClALEAsQCtAK0AkgCSAHIAcgBgAGAAXQBdAF8AXwBeAF4AWABYAEsASwA9AD0APAA8AEYARgBOAE4ATgBOAEkASQBNAE0AWwBbAGUAZQBpAGkAcQBxAHsAewB+AH4AfAB8AIEAgQCQAJAAngCeAKMAowCcAJwAkgCSAIoAigCHAIcAigCKAI8AjwCNAI0AjACMAJMAkwCbAJsAiwCLAGkAaQBbAFsAZQBlAGcAZwBbAFsATwBPAEsASwBOAE4ATQBNAD4APgAwADAAIQAhAP7//v/r/+v/DgAOAC0ALQAXABcA9P/0/+v/6/8AAAAAGAAYAAsACwDr/+v/9P/0/xQAFAASABIAAAAAAAEAAQAQABAANAA0AFoAWgBUAFQAPgA+AEYARgBJAEkALQAtAAUABQDx//H/HwAfAHMAcwByAHIAHAAcAOz/7P/x//H/4f/h/53/nf9Y/1j/Z/9n/8n/yf8EAAQA7P/s/+v/6/8JAAkA2//b/3D/cP87/zv/UP9Q/2b/Zv9Y/1j/Vf9V/5D/kP/Y/9j/1v/W/6j/qP+o/6j/vf+9/57/nv91/3X/e/97/6v/q//k/+T/BgAGAAwADAD9//3/yP/I/33/ff9g/2D/ef95/5X/lf+v/6//3f/d/+3/7f+u/67/Tv9O/xn/Gf8o/yj/U/9T/1z/XP9S/1L/gP+A/9T/1P/5//n/6//r/8r/yv+I/4j/RP9E/zP/M/9E/0T/R/9H/zn/Of9A/0D/eP94/6v/q/+K/4r/Sf9J/1j/WP+M/4z/gv+C/1v/W/9f/1//jf+N/7r/uv/J/8n/zv/O/+P/4//Q/9D/aP9o/xX/Ff8u/y7/af9p/27/bv9d/13/if+J//3//f9WAFYAPQA9AP3//f/7//v/BgAGAMj/yP9k/2T/Lv8u/zz/PP9h/2H/X/9f/0z/TP9t/23/qv+q/7H/sf+C/4L/V/9X/0//T/91/3X/pf+l/57/nv9x/3H/av9q/5D/kP+y/7L/w//D/8//z//e/97/9v/2/wsACwAfAB8ARQBFAEwATAALAAsAzP/M/9P/0/8DAAMALgAuADcANwAWABYA+f/5//n/+f/h/+H/rP+s/6H/of+6/7r/yP/I/9D/0P/H/8f/mv+a/4b/hv+z/7P/7f/t/wQABADr/+v/s/+z/4//j/+O/47/gP+A/2r/av+M/4z/2v/a/yAAIABQAFAAWwBbAFEAUQBQAFAASwBLADMAMwAlACUAHgAeAAwADAAXABcARABEAE8ATwBBAEEARQBFAD4APgAXABcA5P/k/8H/wf/E/8T/1v/W/93/3f/x//H/FQAVACMAIwAeAB4AEwATAO3/7f++/77/tP+0/9L/0v8BAAEAMgAyAD0APQAiACIAHQAdADQANAA9AD0APQA9AEEAQQAuAC4ACAAIAPL/8v/0//T/AwADABkAGQA3ADcAYQBhAHsAewBeAF4ANgA2AEIAQgBZAFkANAA0APH/8f/e/97/+f/5/wgACADz//P/0P/Q/9n/2f8QABAANAA0ADQANAAzADMAMgAyADIAMgBOAE4AeQB5AGgAaAAdAB0A/f/9/zoAOgCLAIsAjgCOAFkAWQBBAEEASwBLADoAOgAMAAwA6v/q/+T/5P8IAAgAUwBTAI0AjQCXAJcAfwB/AFsAWwBRAFEAZQBlAGIAYgA0ADQAHgAeADEAMQAqACoADAAMABIAEgBIAEgAfAB8AHUAdQA+AD4AJAAkAEsASwB2AHYAgQCBAIMAgwCBAIEAiQCJAMIAwgAAAQAB+gD6AMkAyQCyALIAwwDDANMA0wCpAKkAPgA+ANz/3P/G/8b/2P/Y/+r/6v8YABgAVgBWAGEAYQAtAC0A/f/9/+r/6v/c/9z/2P/Y//X/9f8vAC8AYQBhAGsAawBgAGAAXABcAF8AXwBaAFoAXgBeAJAAkADMAMwAzQDNAJ0AnQB6AHoAkwCTAN4A3gArASsBUQFRAUkBSQEdAR0B6QDpANUA1QDbANsAzQDNAKgAqACJAIkAZABkABsAGwC4/7j/ff99/4X/hf+W/5b/df91/zn/Of8p/yn/T/9P/5H/kf/j/+P/GwAbABwAHAAfAB8AagBqANgA2AD4APgArgCuAFEAUQBTAFMAtwC3AOkA6QCoAKgAWQBZAEoASgBeAF4AgACAAMcAxwAXARcB9wD3ADMAMwCU/5T/0P/Q/1UAVQBCAEIArv+u/1T/VP9c/1z/U/9T/zD/MP9s/2z/CAAIACkAKQBb/1v/n/6f/v/+//75//n/WABYANP/0/9J/0n/uv+6/wEBAQG9Ab0B7gDuAE3/Tf9y/nL+Xf9d/3QBdAGBAoECUQFRAYf/h/9C/0L/bABsAHkBeQFiAWIBPQA9AP7+/v6D/oP+tP60/vv++/7u/u7+m/6b/s/+z/4eAB4AowGjAa8BrwEKAAoAV/5X/gT+BP73/vf+7//v/xsAGwDA/8D/OP84/8T+xP7F/sX+Of85/6P/o/+//7//sP+w/5v/m/9r/2v/Ff8V/wT/BP+I/4j/FAAUAAcABwCx/7H/xv/G/0UARQB+AH4AJQAlAPz//P+0ALQAlQGVATYBNgGH/4f/z/3P/R79Hv2F/YX9Yv5i/jH/Mf/c/9z/ZwBnAJsAmwBJAEkA4P/g/73/vf+4/7j/5P/k/3QAdADiAOIAUQBRAAH/Af86/jr+sf6x/qj/qP+8/7z/bv5u/u387fyv/K/8s/2z/Qz/DP8SABIAZgBmAFcAVwDDAMMALgEuAZIAkgBq/2r/n/6f/nf+d/7n/uf+W/9b/0L/Qv8z/zP/vv++/zYANgBTAFMAmQCZAMoAygCAAIAA6v/q/y//L//Z/tn+lf+V/8AAwAAvAS8ByQDJAAAAAAAn/yf/3/7f/k//T//N/83/AAAAABAAEAABAAEA4//j/4r/iv+W/pb+f/1//TD9MP3D/cP9u/67/oX/hf+z/7P/m/+b//b/9v/PAM8AdAF0AUwBTAFhAGEAcf9x/0X/Rf/L/8v/VQBVAJ4AngDOAM4A3ADcAIkAiQDe/97/O/87/wP/A/9I/0j/6//r/9UA1QDAAcABDQINApkBmQH0APQAewB7APX/9f9Q/1D/8P7w/uT+5P7V/tX+lf6V/k7+Tv5k/mT+5P7k/j7/Pv9D/0P/Xv9e/4j/iP95/3n/d/93/+b/5v+dAJ0AIgEiATsBOwEwATABTwFPAU0BTQHRANEARgBGADoAOgCcAJwAFQEVAYEBgQHWAdYB/AH8AcMBwwEbARsBdwB3AEoASgBCAEIA4P/g/1j/WP8Y/xj/F/8X/zb/Nv96/3r/v/+//9f/1//P/8//zv/O/+L/4v/p/+n/1//X/87/zv+o/6j/Pv8+/wT/BP9c/1z/x//H/9n/2f8FAAUAsgCyAJsBmwFAAkACSwJLAv0B/QH+Af4BWAJYAlYCVgLAAcABGAEYAYoAigDz//P/XP9c/+r+6v7I/sj+6P7o/tz+3P62/rb+Iv8i/wMAAwB6AHoAaQBpAEYARgAyADIAPAA8AGgAaAB/AH8AawBrAEwATAA4ADgARABEAGUAZQBXAFcAQQBBAKYApgBVAVUBqwGrAa8BrwGxAbEBvQG9Aa0BrQE0ATQBYABgAMD/wP+d/53/x//H/w8ADwAuAC4A4//j/4j/iP+T/5P/5P/k//L/8v98/3z/9f71/ur+6v5e/17/tf+1/3v/e/9D/0P/m/+b/ycAJwCRAJEA2wDbAN0A3QBmAGYA7v/u/zEAMQAYARgBuQG5AYABgAHsAOwA0QDRAAABAAG1ALUAFQAVANL/0v/x//H/IAAgAEkASQAxADEAzP/M/5//n//V/9X/CgAKABwAHAD4//j/mf+Z/3T/dP+t/63/xf/F/6n/qf+K/4r/S/9L/x3/Hf8//z//Zf9l/23/bf+S/5L/9f/1/68ArwCfAZ8BHAIcAsEBwQE3ATcBFAEUAQ0BDQH1APUA0QDRAKEAoQB7AHsAZABkADwAPAD7//v/0P/Q/8L/wv+l/6X/aP9o/x//H/8N/w3/Mf8x/0L/Qv9C/0L/Uf9R/33/ff/R/9H/FwAXABUAFQANAA0ARwBHAHQAdABqAGoAZgBmAFoAWgBEAEQATABMADwAPAAEAAQA8//z/wgACAD0//T/1P/U//b/9v8vAC8AQwBDACUAJQDt/+3/4P/g/wkACQAzADMANgA2ABoAGgAMAAwADwAPACYAJgBFAEUASQBJADoAOgACAAIAzP/M/+r/6v8iACIAMgAyAFMAUwCQAJAAowCjAJUAlQCuAK4AyQDJAIsAiwAeAB4A7f/t/yAAIABtAG0AaABoABsAGwAWABYArwCvADkBOQEFAQUBUQBRALH/sf+s/6z/GAAYAAcABwBV/1X/1/7X/tv+2/7w/vD+Af8B/zb/Nv9l/2X/kf+R/87/zv8dAB0AqgCqADgBOAFKAUoBLwEvAVABUAFWAVYBKAEoASgBKAFcAVwBoAGgAdAB0AGPAY8BLAEsAW8BbwHcAdwBfAF8AboAugBjAGMAigCKAKYApgDX/9f/Z/5n/rn9uf3//f/9TP5M/jH+Mf6//b/9TP1M/ZL9kv2B/oH+MP8w/3f/d/+R/5H/hv+G/+X/5f/SANIASAFIAfEA8QCRAJEAhgCGAMgAyABoAWgBuAG4AS8BLwHEAMQAEwETAV8BXwE4ATgB1ADUAHYAdgCDAIMAlgCWANr/2v/0/vT+vv6+/lz+XP5f/V/95fzl/Hr9ev1D/kP+QP5A/or9iv0a/Rr9i/2L/X3+ff4b/xv/Iv8i/7L+sv6x/bH9Yfxh/Lz7vPth/GH8nP2c/VX+Vf7J/sn+9P/0/zsBOwEnAScBEQARAGT/ZP9T/1P/d/93/9j/2P9GAEYA/f/9/47+jv4Z/Rn9B/0H/fr9+v2L/ov+Yv5i/gb+Bv5B/UH97vvu+0D7QPv3+/f7jf2N/WP/Y/+TAJMAQQBBAKD+oP5+/H784vri+hz7HPsv/S/9Ev8S/2n/af+3/rf+oP2g/Yf8h/w=




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
