# S&P 500 DEF 14A Tracker
Tracker to check and update a local version of the S&P 500 [list from Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) 
and check each on the SEC website to see if a DEF 14A has been updated in the past 
24 hours. You can run it directly if you have python3 installed on your machine:

```shell
python3 -m venv .env
source .env/bin/activate.sh
pip install -r requirements.txt
python daemon.py
```

## Build
Building an executable can be done using e.g. [PyInstaller](https://pypi.org/project/pyinstaller/):

```shell
python3 -m venv .env
source .env/bin/activate.sh
pip install -r requirements.txt
pip install pyinstaller
pyinstaller ./daemon.py
```

This will create an executable file in the newly created `dist` folder.