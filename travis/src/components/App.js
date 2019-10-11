import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState } from "react";

const sampleTranscript = require('../sample-transcript/final.json');

export default function App() {
    const [trData, setTrData] = useState(sampleTranscript);
    const [playStatus, setPlayStatus] = useState({
        playing: false,
        pos: 0,
        fromPos: 0,
        toPos: 0,
    })
    
    return (
        <>
            <FileLoader setData={setTrData} />
            <Audio playStatus={playStatus} setPlayStatus={setPlayStatus}/>
            <Transcript {...trData} />
        </>
    );
  }
  