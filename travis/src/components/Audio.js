import Sound from 'react-sound';
import { AudioContext } from "./";
import { useContext } from "react";


export default function Audio({
    playStatus,
    setPlayStatus
}) {
    let url = "sample-transcript/raw.mp3";
    const { audioStatus } = useContext(AudioContext);

    return (
        <>
            <audio id='full-audio' src={url} controls />
            <Sound
                url={url}
                playStatus={audioStatus.playing ? Sound.status.PLAYING : Sound.status.STOPPED}
                position={audioStatus.pos}
                // onPlaying={this.handleSongPlaying}
            />
        </>
    )
}