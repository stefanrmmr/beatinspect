import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

import AudioReactRecorder, { RecordState } from 'audio-react-recorder'
import 'audio-react-recorder/dist/index.css'

interface State {
  numClicks: number
  isFocused: boolean
  recordState: null
  audioData: string
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class MyComponent extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false, recordState: null, audioData: ''}

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    const { recordState } = this.state

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.state.isFocused ? theme.primaryColor : "gray"
      }`
      style.border = borderStyling
      style.outline = borderStyling
    }

    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    return (
      <span>
        <div>
          <AudioReactRecorder
            state={recordState}
            onStop={this.onStop}
            backgroundColor='rgb(255,255,255)'
          />
          <audio
            id='audio'
            controls
            src={this.state.audioData}
          ></audio>
          <button id='record' onClick={this.start}>
            Start
          </button>
          <button id='pause' onClick={this.pause}>
            Pause
          </button>
          <button id='stop' onClick={this.stop}>
            Stop
          </button>
        </div>



        Hello, {name}! &nbsp;
        <button id='button_a' style={style} onClick={this.onClickedA}>
          Button A
        </button>
        <button id='button_b' style={style} onClick={this.onClickedB}>
          Button B
        </button>
        <button id='button_c' style={style} onClick={this.onClickedC}>
          Button C
        </button>
      </span>
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 1 }),
      () => Streamlit.setComponentValue(this.state.numClicks)
    )
  }


  private onClickedA = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    Streamlit.setComponentValue('A')
  }

  private onClickedB = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    Streamlit.setComponentValue('B')
  }

  private onClickedC = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    Streamlit.setComponentValue('C')
  }



  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }

  /** fucntions from react audio recorder app */
  private start = () => {
    this.setState({
      recordState: RecordState.START
    })
  }

  private pause = () => {
    this.setState({
      recordState: RecordState.PAUSE
    })
  }

  private stop = () => {
    this.setState({
      recordState: RecordState.STOP
    })
  }

  private onStop = (data) => {
    this.setState({
      audioData: data
    })
  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
// You don't need to edit withStreamlitConnection (but you're welcome to!).

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
