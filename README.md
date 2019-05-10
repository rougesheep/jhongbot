# Wish Wall

Discord bot that links wishing wall solutions for The Last Wish raid in Destiny 2

## Setup

Install Python 3

```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -U discord.py
```

Add your bot token to `config.json`

## Running

```
python .\wishingwall.py
```

Or run with supervisor

```
sudo apt install supervisor
ln -s supervisor.conf /etc/supervisor/conf.d/wishwall.conf
sudo systemctl restart supervisor
```

## ToDo

* rewrite using `@command` decorator
* do proper logging instead of stdout
* maybe daemonise it?
* rename?