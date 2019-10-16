## Usage

- TraVis tool: [](https://onsbigdata.github.io/dcm-transcripts-new/travis/dist/)

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
    * [](https://librosa.github.io/librosa/)
* pydub
    * audio manipulation. E.g `audio[30000:59000].export(...)` and things like that
    * [](https://github.com/jiaaro/pydub)
* speechrecognition
    * package for speech reco. Is more of a unified wrapper for several APIs
    * not sure we will use much
    * [](https://realpython.com/python-speech-recognition/)
* inaSpeechSegmenter
    * Neural network based segmentation tool. Works nicely!
    * Needs Tensorflow and ffmpeg
    * [](https://github.com/ina-foss/inaSpeechSegmenter))
* pyAudioAnalysis
    * another one for feature extraction, segmentation, classification...
    * this one has diarization too. Does not work too well, but the methodology
    seems sound.
        * [](https://github.com/tyiannak/pyAudioAnalysis/wiki)
        * paper - [](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144610)
* google-cloud-speech
    * the python API for GCP speech2text
    * currently, I use a test tier on GCP where I put my own debit card
    which has a free credit for a year.