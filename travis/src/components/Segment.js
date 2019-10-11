import Word from './Word'


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

    return (
        <div className="segment">
            <div className="seg-header">
                <span className="seg-id">{segId}. </span>
                <span className="seg-time">({startSec.toFixed(2)} - {endSec.toFixed(2)})</span><br/>

                <span className="seg-speaker">Speaker: {speaker_id} ({speakerType})</span>
            </div>
            <div className="seg-body">
                {makeWords(words, segId)}
            </div>
        </div>
    )
}