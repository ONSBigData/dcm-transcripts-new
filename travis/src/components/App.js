import Transcript from './Transcript'
import FileLoader from './FileLoader'
import Audio from './Audio'
import { useState, useEffect } from "react";
import $ from "jquery";
import useTranscriptData from '../hooks/transcript-data-hooks';
import {getUrlParameter} from "../helpers/helper.js"    

export default function App() {
    const [trData, loadTrData, editSegment] = useTranscriptData();

    useEffect(() => {
        let jsonUrl = getUrlParameter('transcript-url', "input/final.json");
        $.getJSON(jsonUrl, function(json) {
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
  