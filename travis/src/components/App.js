import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState, useEffect } from "react";
import $ from "jquery";
import useTranscriptData from '../hooks/transcript-data-hooks';

export default function App() {
    const [trData, loadTrData, editSegment] = useTranscriptData();

    useEffect(() => {
        $.getJSON("input/final.json", function(json) {
            loadTrData(json);
        });
    }, [])

    
    return (
        <>
            <a href="index.html" className="back-to-index">Back</a>
            {/* <FileLoader updateTrData={loadTrData} /> */}
            <Audio />
            <Transcript trData={trData} editSegment={editSegment}/>
        </>
    );
  }
  