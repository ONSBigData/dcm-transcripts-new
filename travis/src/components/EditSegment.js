


export default function EditSegment({
    segId,
    words = []
}) {
    let text = words.map((w) => w['word']).join(' ');

    return (
        <div className="edit-segment">
            <textarea className="edit-area" defaultValue={text} rows={4} />
        </div>
    )
}