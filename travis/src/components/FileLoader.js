import { useRef } from "react";

export default function FileLoader({
    updateTrData = () => null
}) {
    const transcriptInput = useRef(null);

    const onSubmit = (event) => {
        event.preventDefault();

        // transcript
        let transcriptFile = transcriptInput.current.files[0];
        
        let reader = new FileReader();
        reader.onloadend = () => {
            let json = JSON.parse(reader.result)
            updateTrData(json);
        }
        reader.readAsText(transcriptFile);
    };

    return (
        <div className="file-load-control control-div">
            <b>File loading</b>
            <form onSubmit={onSubmit} className="file-load">
                <label>Transcript: <input type="file" ref={transcriptInput} /></label><br/>

                <button type="submit">Submit</button>
            </form>
        </div>
    );    
}