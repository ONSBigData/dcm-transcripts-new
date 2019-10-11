import SegmentList from './SegmentList'


export default function Transcript({
    name,
    segments
}) {
    return (
        <div className="transcript">
            <h1>{name}</h1>

            <SegmentList
                segments={segments}
            />
        </div>
    )
}