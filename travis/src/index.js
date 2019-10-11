import React from "react";
import { createContext } from "react";
import { render } from "react-dom";
import App from './components/App'
import './css/styles.scss';
import { AudioStatusProvider } from "./components/audio-status-hooks.js";


window.React = React;

render(
    <AudioStatusProvider>
        <App />
    </AudioStatusProvider>
    , document.getElementById("react-container")   
)