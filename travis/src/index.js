import React from "react";
import { render } from "react-dom";
import './css/styles.scss';
import FileLoader from './components/FileLoader'


window.React = React;

if (document.getElementById("react-file-load-container")) {
    render(
        <FileLoader />
        , document.getElementById("react-file-load-container")   
    )    
}

window.onbeforeunload = function() {
    return "Are you sure?";
}
