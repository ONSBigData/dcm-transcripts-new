import Segment from './Segment'

export default function Transcript({
    trData,
    editSegment
}) {
    let {name, no_speakers: noSpeakers, segments} = trData;
    
    const saveTranscriptJson = () => {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(trData));
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "final-checkpoint.json");
        dlAnchorElem.click();
    };

    const exportTranscript = () => {
        var dataStr = "data:text/plain;charset=utf-8," + encodeURIComponent(trData);
        var dlAnchorElem = document.getElementById('downloadAnchorElem');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "final.txt");
        dlAnchorElem.click();
    };

    const makeSegments = (segmentsData) => {
        return segmentsData.map((segment, index) => (
            <>
                <Segment
                    key={`seg_${index}`}
                    segIx={index}
                    editSegment={(text) => editSegment(index, text)}
                    {...segment}
                />
            </>         
        ))
    }

    return (
        <div className="transcript">
            <h1>{name}</h1>
            <h5>{noSpeakers >= 0 ? noSpeakers : 'Unknown number of '} speakers</h5>

            <a id="downloadAnchorElem"></a>

            <a className="save-export" onClick={saveTranscriptJson}>Save transcript JSON</a>
            <a className="save-export" onClick={exportTranscript}>Export transcript</a>

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