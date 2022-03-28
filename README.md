# S&P 500 DEF 14A Tracker
Tracker to check and update a local version of the S&P 500 [list from Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) 
and check each on the SEC website to see if a DEF 14A has been updated in the past 
24 hours. The easiest way to run is using Docker:

```shell
docker build -t snp git@github.com:andrewtplatt/SNP500_DEF14A_Tracker.git
docker run -d snp
```

Or alternatively, run it yourself in the shell:

```shell
python3 -m venv .env
source .env/bin/activate.sh
pip install -r requirements.txt
python daemon.py
```