import chroma from "chroma-js";
import { useState } from "react";
import ReactTooltip from 'react-tooltip'

var scale = chroma.scale(['red', 'green']);

export default function Word({
    wordId,
    word,
    confidence,
    others={}
}) {
    const [hovered, setHovered] = useState(false)

    var style = {};

    let isPunct = ('type' in others) && (others['type'] == 'punctuation');
    if (!isPunct) {
        var color = scale(confidence);
        style['backgroundColor'] = color.alpha(hovered ? 0.8 : 0.3).hex();
    }
    else {
        style['marginLeft'] = '-0.2em';
    }

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
        <ReactTooltip 
            key={`${wordId}_tooltip`}
            id={`${wordId}_tooltip`} 
            aria-haspopup='true'
        >
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