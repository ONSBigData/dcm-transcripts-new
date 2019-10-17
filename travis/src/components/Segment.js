import Word from './Word'
import EditSegment from './EditSegment'
import { useAudioStatus } from "../hooks/audio-status-hooks.js";
import {useState} from "react"
import colorPalette from "../helpers/color-array.js"
import {textFromWords} from '../helpers/helper.js'


function makeWords(wordsData, segId) {
    var getWordId = (index) => `w_${segId}_${index}`;

    return wordsData.map((word, index) => (
        <Word
            key={getWordId(index)}
            wordId={getWordId(index)}
            {...word}
        />
    ))
}

export default function Segment({
    segIx,
    selectedSpeakerId,
    setSelectedSpeakerId,
    start_s: startSec,
    end_s: endSec,
    type: speakerType,
    speaker_id: speakerId,
    speaker_ix: speakerIx,
    words = [],
    edited,
    editSegment=() => {}
}) {
    const { audioStatus, startPlaying, stopPlaying } = useAudioStatus();
    const [editMode, setEditMode] = useState(typeof edited !== 'undefined');

    let initEditBoxText = typeof edited !== 'undefined' ? edited : textFromWords(words);
    const [editBoxText, setEditBoxText] = useState(initEditBoxText);

    const playAudio = () => {
        startPlaying(startSec, endSec, segIx);
    }

    let styles = {
        'backgroundColor': colorPalette[speakerIx] + '60'
    }

    let display = (selectedSpeakerId !== null) && (selectedSpeakerId !== speakerId) ? 'none' : 'flex';

    return (
        <div className="segment" style={{'display': display}}>
            <div className="seg-header">
                <span className="seg-id">{segIx}. </span><br/>
                <a className="seg-time" onClick={playAudio}>
                    &#9658; {startSec.toFixed(2)}s - {endSec.toFixed(2)}s
                    
                </a>
                <br/>
                <div hidden={!audioStatus.playing || audioStatus.segId !== segIx}>
                    <a 
                        className="seg-audio-stop" 
                        onClick={() => stopPlaying()}
                    >
                        &#11035; Stop playing
                    </a>
                    <br/>
                </div>

                <span 
                    style={styles} 
                    className="seg-speaker"
                    onClick={() => {
                        setSelectedSpeakerId(selectedSpeakerId !== null ? null : speakerId)
                    }}
                >
                    Speaker: {speakerId} ({speakerType})
                </span>
            </div>
            <div className="seg-body">
                <div className="seg-body-orig" onDoubleClick={() => setEditMode(!editMode)}>
                    {makeWords(words, segIx)}
                </div>
                <div className={`seg-body-edit ${editMode ? "" : "seg-body-edit-hidden"}`}>
                    <hr></hr>
                    <EditSegment 
                        initEditBoxText={initEditBoxText}
                        editSegment={editSegment}
                        editBoxText={editBoxText} 
                        setEditBoxText={setEditBoxText}
                    />
                </div>                
            </div>
            <div className="edit-button">
                <img src="pics/icon-edit.png" onClick={() => setEditMode(!editMode)} /><br/>
                <img src="pics/icon-accept.png" onClick={() => editSegment(editBoxText)} /><br/>
            </div>
        </div>
    )
}