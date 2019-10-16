import Transcript from './Transcript'
import Audio from './Audio'
import { useEffect } from "react";
import $ from "jquery";
import useTranscriptData from '../hooks/transcript-data-hooks';

export default function App({
    transcriptUrl,
    audioUrl
}) {
    const [trData, loadTrData, editSegment] = useTranscriptData();

    useEffect(() => {
        $.getJSON(transcriptUrl, function(json) {
            loadTrData(json);
        });
    }, [])

    
    return (
        <>
            <a href="index.html" className="back-to-index">Choose new files</a>
            <Audio audioUrl={audioUrl}/>
            <Transcript trData={trData} editSegment={editSegment}/>
        </>
    );
  }
  