## Installation

* cd to `src` dir
* `sudo pip3 install -U virtualenv` - system-wide install of virtual env (if not installed)
* `virtualenv --system-site-packages -p python3 ../venv` - create a new virtual env
* `source ../venv/bin/activate` in the `src` dir to activate the venv
    * `pip install -r requirements.txt`
    * ignore Pipfile - pipenv is too slow for now
    * manually install pyAudioAnalysis as per https://github.com/tyiannak/pyAudioAnalysis#installation
* install `ffmpeg` https://tecadmin.net/install-ffmpeg-on-linux/
    * if problems with `apt` - follow https://stackoverflow.com/a/44612200/1913724
*
