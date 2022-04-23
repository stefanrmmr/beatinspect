import React, { useState, useEffect } from 'react'
import { useMediaRecorder } from 'use-media-recorder'

const AudioRecorder = () => {
    const [stateIndex, setStateIndex] = useState(0)
    const [audioURL, setAudioURL] = useState('')
    const [chunks, setChunks] = useState([])
    const [mediaRecorder, mediaStream, mediaStreamError] = useMediaRecorder()

    const State = ['Initial', 'Record', 'Download']

    useEffect(() => {
        if(mediaStreamError){
            setStateIndex('')
        }
    }, [mediaStreamError])

    useEffect(() => {
        if(mediaRecorder){
            mediaRecorder.ondataavailable = (e) => {
                setChunks(chunks => [...chunks, e.data])
            }

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, {'type': 'audio/ogg; codecs=opus'})
                setChunks([])
                setAudioURL(window.URL.createObjectURL(blob))
            }
        }
    }, [mediaRecorder])

    const clearDisplay = () => {
        document.querySelector('.display').textContent = ''
    }

    const clearControls = () => {
        document.querySelector('.controllers').textContent = ''
    }

    const record = () => {
        setStateIndex(1)
        mediaRecorder.start()
    }

    const stopRecording = () => {
        setStateIndex(2)
        mediaRecorder.stop()
    }

    const analyzeAudio = () => {
        // this element needs to create a return value for streamlit
        const downloadLink = document.createElement('a')
        downloadLink.href = audioURL
        downloadLink.setAttribute('download', 'audio')
        downloadLink.click()
    }

    const addButton = (id, funString, text) => {
        const btn = document.createElement('button')
        btn.id = id
        btn.setAttribute('onclick', funString)
        btn.textContent = text
        document.querySelector('.controllers').append(btn)
    }

    const addMessage = (text) => {
        const msg = document.createElement('p')
        msg.textContent = text
        document.querySelector('.display').append(msg)
    }

    const addAudio = () => {
        const audio = document.createElement('audio')
        audio.controls = true
        audio.src = audioURL
        document.querySelector('.display').append(audio)
    }

    const application = (index) => {
        switch (State[index]) {
            case 'Initial':
                clearDisplay()
                clearControls()

                addMessage('Press the start button to start recording\n')
                addButton('record', 'record()', 'Start Recording')
                break;

            case 'Record':
                clearDisplay()
                clearControls()

                addMessage('Recording...\n')
                addButton('stop', 'stopRecording()', 'Stop Recording')
                break

            case 'Download':
                clearControls()
                clearDisplay()

                addAudio()
                addButton('continue', 'analyzeAudio()', 'Continue')
                addButton('record', 'record()', 'Record Again')
                break

            default:
                clearControls()
                clearDisplay()

                addMessage('Your browser does not support mediaDevices')
                break;
        }
    }

    useEffect(() => {
        application(stateIndex)
    }, [stateIndex])

    return (
        <div>
            <div className="display"></div>
            <div className="controllers"></div>
        </div>
    )
}

export default AudioRecorder
