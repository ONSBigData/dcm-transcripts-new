import { useState, useEffect } from "react";

export default function EditSegment({
    editSegment,
    words = [],
    edited = null
}) {
    let defText = '';
    if (edited !== null) {
        defText = edited;
    }
    else {
        words.forEach((word, i) => {
            let others = word['others'] ? word['others'] : {};
            let isPunct = ('type' in others) && (others['type'] == 'punctuation');
    
            if (i > 0 && !isPunct) {
                defText += ' ';
            }

            defText += word['word'];
        })
    }

    const [saved, setSaved] = useState(true);

    return (
        <div className="edit-segment">
            <textarea 
                className={`edit-area ${!saved ? 'edit-area-unsaved' : ''}`}
                defaultValue={defText} 
                rows={4} 
                onKeyPress={(e) => {
                    setSaved(false);

                   if (e.key === 'Enter' && e.ctrlKey) {
                        editSegment(e.target.value);
                        setSaved(true);
                    }
                }}
            />
        </div>
    )
}