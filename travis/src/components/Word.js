import chroma from "chroma-js";
import { useState } from "react";
import ReactTooltip from 'react-tooltip'

var scale = chroma.scale(['red', 'green']);

export default function Word({
    wordId,
    word,
    confidence,
}) {
    const [hovered, setHovered] = useState(false)
    var color = scale(confidence);
    var style = {
        'background-color': color.alpha(hovered ? 0.8 : 0.3).hex(),
    };

    //-------------- Rendering

    var wordElement = (
        <span 
                className="word" 
                style={style} 
                onMouseEnter={(e) => setHovered(true)} 
                onMouseLeave={(e) => setHovered(false)}
                data-tip 
                data-for={`${wordId}_tooltip`}
        >
            {word}
        </span>
    )

    var tooltipElement = (
        <ReactTooltip id={`${wordId}_tooltip`} aria-haspopup='true' role='example'>
            Confidence: {Number(confidence).toFixed(2)}
        </ReactTooltip>
    )

    return (
        <>
            {wordElement}
            {tooltipElement}
        </>
    )
}