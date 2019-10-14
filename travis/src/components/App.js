import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState, useEffect } from "react";
import $ from "jquery";
import useTranscriptData from './transcript-data-hooks';

export default function App() {
    const [trData, updateTrData, editSegment] = useTranscriptData();

    useEffect(() => {
        $.getJSON("dist/input/final.json", function(json) {
            updateTrData(json);
        });
    }, [])

    
    return (
        <>
            {/* <FileLoader updateTrData={updateTrData} /> */}
            <Audio />
            <Transcript trData={trData} editSegment={editSegment}/>
        </>
    );
  }
  