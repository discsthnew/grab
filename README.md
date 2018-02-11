# Overview
Statistics website resource size distribution. mainly use scrapy and sqlalchemy.

# Installation
```
  # git clone https://github.com/discsthnew/grab.git
  # cd grab
  # pip install -r requirements.txt
```

# Configuration
## db
open `grab/settings.py`, go to the last line and you will found a dict name `MYSQL`. take the place of your own confiugration.
```
#MYSQL CONNECTOR

MYSQL = {
   'user': 'walker',
   'password': 'password',
   'host': '127.0.0.1',
   'port': '3306',
   'db': 'test'
}
```
## Others
for more details, please see [scrapy document](https://doc.scrapy.org/en/latest/topics/broad-crawls.html)

# Run
```
  python run.py
```

> ***Notice***: 
> 1. if you want do collect another web site resource, just edit the `run.py`, and add the domain you want to visited.
> 2. after you run this command, a table named `resource` will be created automatically. 

