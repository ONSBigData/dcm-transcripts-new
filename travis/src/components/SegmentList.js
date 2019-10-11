import Segment from './Segment'


function makeSegments(segmentsData) {
    return segmentsData.map((segment, index) => (
        <>
            <Segment
                key={`seg_${index}`}
                segId={index}
                {...segment}
            />
        </>         
    ))
}


export default function SegmentList({
    segments = [],
}) {
    return (
        <div className="segment-list">
            { segments.length === 0 ? (
                <p>No segments in the transcript</p>
            ) : (
                makeSegments(segments)
            )}
        </div>
    )
}