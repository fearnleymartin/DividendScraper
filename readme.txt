#Git Bash
## Setup

Open git bash

```
git clone https://github.com/fearnleymartin/DividendScraper.git
cd DividendScraper
py -m pip install virtualenv
py -m virtualenv venv
source venv/Scripts/activate
py -m pip install -r requirements.txt
```


## Run

```
cd DividendScraper
source venv/Scripts/activate
py -u dividend_scraper.py


##Commands
ls: list file in directory 
pwd: present working directory
cd: change directory

pwd
```

## Modify dividend scraper

Open `dividend_scraper.py` and update params

## Update
git pull

other codes:
git commit -m 'update readme'
git checkout -- dividend_scraper.py

#AWS
## Setup
sudo yum update
sudo yum install git
sudo yum install python3

git clone https://github.com/fearnleymartin/DividendScraper.git
sudo python3 -m pip install virtualenv
sudo python3 -m virtualenv venv
sudo python3 -m pip install -r requirements.txt

##Run
cd DividendScraper
source venv/bin/activate
sudo python3 -u dividend_scraper.py




