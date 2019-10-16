import { useRef } from "react";
import App from './App'
import { AudioStatusProvider } from "../hooks/audio-status-hooks.js";
import { render } from "react-dom";


export default function FileLoader({

}) {
    const transcriptInput = useRef(null);
    const audioInput = useRef(null);

    const renderTranscriptReact = (transcriptUrl, audioUrl) => {
        if (document.getElementById("react-transcript-container")) {
            render(
                <AudioStatusProvider>
                    <App transcriptUrl={transcriptUrl} audioUrl={audioUrl}/>
                </AudioStatusProvider>
                , document.getElementById("react-transcript-container")   
            )    
        }
        
        window.onbeforeunload = function() {
            return "Are you sure?";
        }

        document.getElementById('react-file-load-container').hidden = true;
    }

    const onSubmit = (event) => {
        event.preventDefault();

        let audioFile = audioInput.current.files[0];
        let transcriptFile = transcriptInput.current.files[0];

        let transcriptReader = new FileReader();
        transcriptReader.onloadend = () => {
            var transcriptUrl = transcriptReader.result;

            let audioReader = new FileReader();
            audioReader.onloadend = () => {
                var audioUrl = audioReader.result;

                renderTranscriptReact(transcriptUrl, audioUrl);
            }

            audioReader.readAsDataURL(audioFile);
        }

        transcriptReader.readAsDataURL(transcriptFile);
    };

    return (
        <div className="file-load-control control-div">
            <b>File loading</b>
            <form onSubmit={onSubmit} className="file-load">
                <label>Transcript: <input type="file" ref={transcriptInput} accept=".json" /></label><br/>
                <label>Audio: <input type="file" ref={audioInput} accept=".mp3" /></label><br/>

                <button type="submit">Submit</button>
            </form>
            <span className="see-example" onClick={() => renderTranscriptReact('input/final.json', 'input/raw.mp3')}>See example</span>
        </div>
    );    
}