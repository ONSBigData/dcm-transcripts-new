import React from "react";
import { createContext } from "react";
import { render } from "react-dom";
import App from './components/App'
import './css/styles.scss';
import { AudioStatusProvider } from "./hooks/audio-status-hooks.js";


window.React = React;

if (document.getElementById("react-container")) {
    render(
        <AudioStatusProvider>
            <App />
        </AudioStatusProvider>
        , document.getElementById("react-container")   
    )    
}

window.onbeforeunload = function() {
    return "Are you sure?";
}
