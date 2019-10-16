import { useState, useEffect } from "react";
import {textFromWords} from '../helpers/helper.js'

export default function EditSegment({
    editSegment,
    words = [],
    edited
}) {
    let defText = typeof edited !== 'undefined' ? edited : textFromWords(words);

    const [saved, setSaved] = useState(true);

    return (
        <div className="edit-segment">
            <textarea 
                className={`edit-area ${!saved ? 'edit-area-unsaved' : ''}`}
                defaultValue={defText} 
                rows={4} 
                onChange={() => setSaved(false)}
                onKeyPress={(e) => {
                    console.log(e);
                    let shouldSave = ((e.key === 'Enter') && e.ctrlKey);
                    shouldSave = shouldSave || ((e.keyCode == 13) && e.ctrlKey);

                    if (shouldSave) {
                        editSegment(e.target.value);
                        setSaved(true);
                    }
                }}
            />
        </div>
    )
}