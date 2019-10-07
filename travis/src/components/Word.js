import Popup from "reactjs-popup";


import chroma from "chroma-js";

var scale = chroma.scale(['red', 'green']);

export default function Word({
    word,
    confidence,
}) {
    var color = scale(confidence).alpha(0.3).hex();

    var wordElement = <span className="word" style={{'background-color': color}}>
        {word}
    </span>

    return (
        <>
            <Popup
                trigger={wordElement}
                on='hover'
                position="top center"
                closeOnDocumentClick
            >
                Confidence: {confidence}                
            </Popup>
            <span className="word-break"></span>
        </>
    )
}