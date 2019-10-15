import Sound from 'react-sound';
import { useAudioStatus } from "../hooks/audio-status-hooks.js";
import {getUrlParameter} from "../helpers/helper.js"


export default function Audio({

}) {
    let url = getUrlParameter('audio-url', 'input/raw.mp3');
    const { audioStatus, stopPlaying, updatePos } = useAudioStatus();

    const handlePlaying = (pos) => {
        if (pos.position > audioStatus.toPos) {
            stopPlaying();
        } 
        else {
            updatePos(pos.position);
        }
    };

    return (
        <>
            <div className="full-audio-control control-div">
                <b>Full audio</b><br/>
                <audio id='full-audio' src={url} controls />
            </div>
            <Sound
                url={url}
                playStatus={audioStatus.playing ? Sound.status.PLAYING : Sound.status.STOPPED}
                position={audioStatus.pos}
                onPlaying={handlePlaying}
            />
        </>
    )
}