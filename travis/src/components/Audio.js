import Sound from 'react-sound';
import { useAudioStatus } from "./audio-status-hooks";


export default function Audio({

}) {
    let url = "dist/input/raw.mp3";
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
                <b>Full audio control</b><br/>
                <audio id='full-audio' src={url} controls />
            </div>
            <div className="seg-audio-control control-div">
                <b>Segment audio</b><br/>
                {
                    audioStatus.playing ? 
                    `Playing segment ${audioStatus.segId}` : 
                    "No segment playing"
                }
                <span 
                    className="seg-audio-stop" 
                    hidden={!audioStatus.playing}
                    onClick={() => stopPlaying()}
                >
                    &#11035;
                </span>
                <br/>
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