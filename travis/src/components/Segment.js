import Word from './Word'
// import $ from 'jquery'
import { useAudioStatus } from "./audio-status-hooks";


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
    segId,
    start_s: startSec,
    end_s: endSec,
    type: speakerType,
    speaker_id,
    words = []
}) {
    const { startPlaying } = useAudioStatus();

    const playAudio = () => {
        startPlaying(startSec, endSec, segId);
    }    

    return (
        <div className="segment">
            <div className="seg-header">
                <span className="seg-id">{segId}. </span><br/>
                <a className="seg-time" onClick={playAudio}>
                    &#9658; {startSec.toFixed(2)}s - {endSec.toFixed(2)}s
                </a>
                <br/>

                <span className="seg-speaker">Speaker: {speaker_id} ({speakerType})</span>
            </div>
            <div className="seg-body">
                {makeWords(words, segId)}
            </div>
        </div>
    )
}