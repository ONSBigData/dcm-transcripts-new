import Word from './Word'
import EditSegment from './EditSegment'
import { useAudioStatus } from "../hooks/audio-status-hooks.js";
import {useState} from "react"
import colorPalette from "../helpers/color-array.js"


function makeWords(wordsData, segId) {
    var getWordId = (index) => `w_${segId}_${index}`;

    return wordsData.map((word, index) => (
        <>
            <Word
                key={getWordId(index)}
                wordId={getWordId(index)}
                {...word}
            />
        </>         
    ))
}

export default function Segment({
    segIx,
    start_s: startSec,
    end_s: endSec,
    type: speakerType,
    speaker_id,
    speaker_ix,
    words = [],
    edited,
    editSegment=() => {}
}) {
    const { audioStatus, startPlaying, stopPlaying } = useAudioStatus();
    const [editMode, setEditMode] = useState(typeof edited !== 'undefined')

    const playAudio = () => {
        startPlaying(startSec, endSec, segIx);
    }

    let styles = {
        'backgroundColor': colorPalette[speaker_ix]
    }

    return (
        <div className="segment" styles={styles}>
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

                <span className="seg-speaker">Speaker: {speaker_id} ({speakerType})</span>
            </div>
            <div className="seg-body">
                <div className="seg-body-orig" onDoubleClick={() => setEditMode(!editMode)}>
                    {makeWords(words, segIx)}
                </div>
                <div className={`seg-body-edit ${editMode ? "" : "seg-body-edit-hidden"}`}>
                    <hr></hr>
                    <EditSegment edited={edited} words={words} editSegment={editSegment} />
                </div>                
            </div>
            <div className="edit-button">
                <img src="pics/icon-edit.png" onClick={() => setEditMode(!editMode)} />
            </div>
        </div>
    )
}