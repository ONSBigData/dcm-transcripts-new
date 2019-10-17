import { useState } from "react";
import update from 'immutability-helper';


const placeholderTranscript = {
    "name": "n/a",
    "segments": []
};

export default function useTranscriptData() {
    const [trData, setTrData] = useState(placeholderTranscript);

    const loadTrData = (json) => {
        let speakerIds = json.segments.map((s) => s['speaker_id']);
        speakerIds = new Set(speakerIds);
        
        json['no_speakers'] = speakerIds.size;

        let speakerIdToindex = {};
        speakerIds.forEach((id, i) => speakerIdToindex[id] = i);

        json['segments'] = json['segments'].map((s) => {
            s['speaker_ix'] = speakerIdToindex[s['speaker_id']];
            return s
        })

        setTrData(json);      
    };

    const editSegment = (segIndex, editedText) => {
        const newTrData = update(
            trData, 
            {
                segments: {
                    [segIndex]: {
                        edited: {
                            $set: editedText
                        }
                    }
                }
            }
        );

        setTrData(newTrData);
    };

    return [trData, loadTrData, editSegment]
};