### Prepare system & tools

For Debian/Ubuntu:
* some platform-specific things(for Qt): `apt install libqt5x11extras5`
* and python (if not preinstalled): `apt install python3.8-full`
* * or `apt install python3 python3-pip`
* `pip3 install virtualenv`

For Windows:
* download and install python3
* * download python v3.x (https://www.python.org/downloads/)
* * run .exe installator with default options, but **tick "Add Python 3.x to PATH"**. Accept all conditions and finish installation

### Prepare repository
* download this repo: use "code" menu button -> "Download ZIP"
* * next unpack zip archive, open project folder and open in terminal
* * or open the terminal and `git clone https://github.com/ivanka6342/py-idiom-parser.git`
* create new virtual environment: `virtualenv -p python3 venv`
* * activate it: `. ./venv/bin/activate` (`. .\venv\Scripts\activate` on Windows)
* install all dependencies: `pip3 install -Ur requirements.txt`

### Run the project
Just run the project in terminal (venv): `python3 main.py` (`python main.py` on Windows)
> For double left-click run you need to install all deps system-wide (without venv)
