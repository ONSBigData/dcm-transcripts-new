import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState } from "react";

const sampleTranscript = require('../sample-transcript/final.json');

export default function App() {
    const [trData, setTrData] = useState(sampleTranscript);
    
    return (
        <>
            <FileLoader setData={setTrData} />
            <Audio />
            <Transcript {...trData}/>
        </>
    );
  }
  