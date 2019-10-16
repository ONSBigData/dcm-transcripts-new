import Segment from './Segment'
import {textFromWords} from '../helpers/helper.js'
import { useState } from "react";



export default function Transcript({
    trData,
    editSegment
}) {
    let {
        name, 
        no_speakers: noSpeakers, 
        segments
    } = trData;

    const [selectedSpeakerId, setSelectedSpeakerId] = useState(null);
    
    const saveTranscriptJson = () => {
        var data = {...trData};
        data['segments'] = data['segments'].filter((s) => (
            ((selectedSpeakerId === null) || (selectedSpeakerId === s.speaker_id))
        ));

        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "final-checkpoint.json");
        dlAnchorElem.click();
    };

    const exportTranscript = () => {
        var rows = [
            `Transcript ID: ${trData.name}`,
            `=================================================`,
            `* No. speakers: ${noSpeakers >= 0 ? noSpeakers : 'unknown'}`,
            '',
            ''
        ];

        trData['segments'].forEach((s, i) => {
            if ((selectedSpeakerId !== null) && (selectedSpeakerId !== s.speaker_id)) {
                return;
            }

            rows.push(`Segment ${i}`);
            rows.push(`---------------------------------------`);
            rows.push(`* ${s['start_s'].toFixed(2)}s - ${s['end_s'].toFixed(2)}s`);
            rows.push(`* Speaker ID: ${typeof s['speaker_id'] !== 'undefined' ? s['speaker_id'] : 'unknown'}`);
            rows.push(`* Type: ${typeof s['type'] !== 'undefined' ? s['type'] : 'unknown'}`);
            rows.push('');

            let text = typeof s['edited'] !== 'undefined' ? s['edited'] : textFromWords(s['words']);
            rows.push(text);
            rows.push('');
            rows.push('');
        });

        var dataStr = "data:text/text;charset=utf-8," + encodeURIComponent(rows.join('\n'));
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "final.md");
        dlAnchorElem.click();
    };

    const makeSegments = (segmentsData) => {
        return segmentsData.map((segment, index) => (
            <Segment
                key={`seg_${index}`}
                segIx={index}
                selectedSpeakerId={selectedSpeakerId}
                setSelectedSpeakerId={setSelectedSpeakerId}
                editSegment={(text) => editSegment(index, text)}
                {...segment}
            />
        ))
    }

    return (
        <div className="transcript">
            <h1>{name}</h1>
            <h5>{noSpeakers >= 0 ? noSpeakers : 'Unknown number of '} speakers</h5>

            <a id="downloadAnchorElem"></a>

            <a className="save-export" onClick={saveTranscriptJson}>Save transcript as JSON</a>
            <a className="save-export" onClick={exportTranscript}>Export transcript as Markdown</a>

            <div className="segment-list">
                { segments.length === 0 ? (
                    <p>No segments in the transcript</p>
                ) : (
                    makeSegments(segments)
                )}
            </div>
        </div>
    )
}