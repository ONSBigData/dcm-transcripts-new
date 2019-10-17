import { useState, useEffect } from "react";

export default function EditSegment({
    initEditBoxText,
    editSegment,
    editBoxText,
    setEditBoxText
}) {
    return (
        <div className="edit-segment">
            <textarea 
                className={`edit-area ${editBoxText !== initEditBoxText ? 'edit-area-unsaved' : ''}`}
                defaultValue={initEditBoxText} 
                rows={4} 
                onChange={(e) => setEditBoxText(e.target.value)}
                onKeyPress={(e) => {
                    e.persist();
                    let shouldSave = ((e.key === 'Enter') && e.ctrlKey);
                    shouldSave = shouldSave || ((e.keyCode == 13) && e.ctrlKey);

                    if (shouldSave) {
                        editSegment(editBoxText);
                    }
                }}
            />
        </div>
    )
}