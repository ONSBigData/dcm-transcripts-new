import Word from './Word'


function makeWords(wordsData, segIndex) {
    return wordsData.map((word, index) => (
        <>
            <Word
                key={`w_${segIndex}_${index}`}
                {...word}
            />
        </>         
    ))
}

export default function Segment({
    index,
    start_s: startSec,
    end_s: endSec,
    type: speakerType,
    speaker_id,
    words = []
}) {

    return (
        <div className="segment">
            <div className="seg-header">
                <span>{index} ({startSec.toFixed(2)} - {endSec.toFixed(2)})</span><br/>
                Speaker {speaker_id} ({speakerType})
            </div>
            <div className="seg-body">
                {makeWords(words, index)}
            </div>
        </div>
    )
}