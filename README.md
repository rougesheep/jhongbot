# Wish Wall

Discord bot that links wishing wall solutions for The Last Wish raid in Destiny 2

## Setup

Install Python 3

Windows:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux/WSL:
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Add your bot token to `config.json` and flag it as unchanged

```
git update-index --assume-unchanged config.json
```

## Running

```
python jhongbot.py
```

Or background it

```
./wrapper.sh daemon
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