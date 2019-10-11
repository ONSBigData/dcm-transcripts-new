import { useRef } from "react";

export default function FileLoader({
    setData = (data) => null
}) {
    const transcriptInput = useRef(null);
    // const audioInput = useRef(null);

    const onSubmit = (event) => {
        event.preventDefault();

        let transcriptFile = transcriptInput.current.files[0];
        
        let reader = new FileReader();
        reader.onloadend = () => {
            setData(JSON.parse(reader.result))
        }
        reader.readAsText(transcriptFile);
    };

    return (
        <form onSubmit={onSubmit} className="file-load">
            <label>Transcript: <input type="file" ref={transcriptInput} /></label><br/>
            {/* <label>Audio: <input type="file" ref={audioInput} /></label><br/> */}

            <button type="submit">Submit</button>
        </form>
    );    
}