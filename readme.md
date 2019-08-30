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