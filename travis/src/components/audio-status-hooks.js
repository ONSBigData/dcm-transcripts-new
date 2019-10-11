import React, { createContext, useState, useContext } from "react";
import { v4 } from "uuid";

const AudioStatusContext = createContext();

export const AudioStatusProvider = ({ children }) => {
    const [audioStatus, setAudioStatus] = useState({
        playing: false,
        pos: 0,
        fromPos: 0,
        toPos: 0,
        segId: null,
    });

    const startPlaying = (startSec, endSec, segId) => {
        let newAudioStatus = {...audioStatus};
        newAudioStatus['pos'] = startSec*1000;
        newAudioStatus['toPos'] = endSec*1000;
        newAudioStatus['playing'] = true;
        newAudioStatus['segId'] = segId;
        setAudioStatus(newAudioStatus);
    };

    const stopPlaying = () => {
        let newAudioStatus = {...audioStatus};
        newAudioStatus['playing'] = false;
        setAudioStatus(newAudioStatus);
    }

    const updatePos = (pos) => {
        let newAudioStatus = {...audioStatus};
        newAudioStatus['pos'] = pos;
        setAudioStatus(newAudioStatus);
    }
  
    let expose = { audioStatus, startPlaying, stopPlaying, updatePos }

    return (
        <AudioStatusContext.Provider value={expose}>
            {children}
        </AudioStatusContext.Provider>
    );
  };

export const useAudioStatus = () => useContext(AudioStatusContext);