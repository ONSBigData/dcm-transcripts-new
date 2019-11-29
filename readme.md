# Overview

This repo contains code for two main parts:
- **TraGen** - the part of the solution focused on generating transcript from an audio recording of interview/focus group. 
  - essentially everything except for `travis` folder is falling under TraGen
- **TraVis** - the part of the solution focused on visualising the output of TraGen (the transcript).
  - all of TraVis is in `travis` foldern
  - TraVis is a web app, written in JavaScript, using React, CSS, HTML ... (no Python)
  - TraVis is hosted on GitHub pages for this repo - https://onsbigdata.github.io/dcm-transcripts-new/travis/dist/index.html 


# TraGen

TraGen - Transcript Generator, is written in Python.

It is not only about generating transcripts, but also about evaluating
the segmentation, diarization and transcription.

The main idea is that we have implementations of:
- segmentation
- diarization
- transcription

All of these can then be chained to form a *pipeline*, e.g. the only working
implemented pipeline is "ina-dummy-aws", meaning
- INA speech segmenting
- dummy diarization (diarizing only based on sex information from INA)
- AWS transcribing

The file `ina_dummy_aws.py` can then be simply run (modifying the bit
of code at the end, which determines which audio and how much of it will
be transcribed). In the process of running the code:
- a new folder in `../data/pipelines` would be created, initially with the
raw recording audio file (`raw.mp3`)
- subsequently, audio segments would appear after the segmentation stage,
diarization info would be added, transcription and eventually a `final.json`
file would be created, containing all the information from the process.

The `raw.mp3` and `final.json` are then inputs for TraVis app.

## Installation

The basic structure of this project is:
* `root_project_folder`
    * `src` - source files (**this is version controlled** - the rest isn't)
        * `notebooks` - jupyter notebooks
        * `requirements.txt`, `.gitignore`...
        * other files...
    * `data` - recordings and other data..
    *  other files...

So start off by creating the root folder and the src & data folders. Then
* cd to `src` dir
* install `pipenv` if not installed (`pip install pipenv`)
    * we won't use pipenv to install packages (takes freaking long time), just
    to easily create/activate virtual environment
* run `pipenv --python 3.6.8 shell` - will create/activate a new virtual env
    * we use this version - 3.6.8. This is cause
        * 3.6 is what is used on ONS machines
        * some packages rely on Tensorflow which had troubles running with 3.7
    * now install `pip install -r requirements.txt`
    * ignore the Pipfile created by pipenv - pipenv is too slow for now
    * manually install pyAudioAnalysis as per https://github.com/tyiannak/pyAudioAnalysis#installation
* install `ffmpeg` https://tecadmin.net/install-ffmpeg-on-linux/
    * if having problems with `apt` like `No module named apt_pkg`, follow
    https://stackoverflow.com/a/44612200/1913724
    * ffmpeg is used by https://github.com/ina-foss/inaSpeechSegmenter -
    audio segmenting package
* the project also needs to be setup to be able to connect to AWS. After installing boto3 package, one
should be able to do this from the command line. (same for GCP cloud, although that one is not used
by this solution at the moment)

Alternative to pipenv is virtualenv:
* `virtualenv --system-site-packages -p python3 ../venv` - create a new virtual env
* `source ../venv/bin/activate` in the `src` dir to activate the venv

## Data

Download the "recordings" folder from https://drive.google.com/open?id=18KeJYoHWOeWEMKHhZoLl9hBT8ptaBml-

Then unzip and move the recordings folder to the `data` folder. I.e.:

* root_project_folder
    * data
        * recordings
            * harvard
            * bbc_interview
            * ...

## Main audio libraries used - overview

* librosa
    * package for audio analysis, feature extraction etc.
    * "provides the building blocks necessary to create music information
    retrieval systems".
    * [link](https://librosa.github.io/librosa/)
* pydub
    * audio manipulation. E.g `audio[30000:59000].export(...)` and things like that
    * [link](https://github.com/jiaaro/pydub)
* speechrecognition
    * package for speech reco. Is more of a unified wrapper for several APIs
    * not sure we will use much
    * [link](https://realpython.com/python-speech-recognition/)
* inaSpeechSegmenter
    * Neural network based segmentation tool. Works nicely!
    * Needs Tensorflow and ffmpeg
    * [link](https://github.com/ina-foss/inaSpeechSegmenter))
* pyAudioAnalysis
    * another one for feature extraction, segmentation, classification...
    * this one has diarization too. Does not work too well, but the methodology
    seems sound.
        * [link](https://github.com/tyiannak/pyAudioAnalysis/wiki)
        * paper - [link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144610)
* google-cloud-speech
    * the python API for GCP speech2text
    * currently, I use a test tier on GCP where I put my own debit card
    which has a free credit for a year.
    
# TraVis

The TraVis - Transcript Visualiser - is a JavaScript web app based on React.

Using React makes for a nice file structure that easily corresponds to the
visuals on the [webpage](https://onsbigdata.github.io/dcm-transcripts-new/travis/dist/index.html)

It is recommended to use VS code to develop this app.

The `raw.mp3` and `final.json` (the JSON file made using TraGen
from the `raw.mp3`) are the inputs for TraVis app.


## Installation & run

The dependencies are managed via NPM. Thus going into the `travis` dir, one should:
- install the packages with `npm install`
- run with `bash run-dev.sh` and access the app in the browser

The solution uses Webpack to build the final `bundle.js`, compile SCSS
stylesheets etc.