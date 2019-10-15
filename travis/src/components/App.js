import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState, useEffect } from "react";
import $ from "jquery";
import useTranscriptData from '../hooks/transcript-data-hooks';

export default function App() {
    const [trData, loadTrData, editSegment] = useTranscriptData();

    useEffect(() => {
        $.getJSON("dist/input/final.json", function(json) {
            loadTrData(json);
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
  