import React from "react";
import { createContext } from "react";
import { render } from "react-dom";
import App from './components/App'
import './css/styles.scss';

window.React = React;

export const AudioContext = createContext();

render(
    <AudioContext.Provider>
        <App />
    </AudioContext.Provider>
    , document.getElementById("react-container")   
)