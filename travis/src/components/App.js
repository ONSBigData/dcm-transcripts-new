import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState, useEffect } from "react";
import $ from "jquery";

const placeholderTranscript = {
    "name": "n/aaaaa",
    "segments": []
};

export default function App() {
    const [trData, setTrData] = useState(placeholderTranscript);

    useEffect(() => {
        $.getJSON("dist/input/final.json", function(json) {
            setTrData(json);
        });    
    }, [])

    
    return (
        <>
            {/* <FileLoader setData={setTrData} /> */}
            <Audio />
            <Transcript {...trData}/>
        </>
    );
  }
  