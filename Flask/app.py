from flask import Flask, render_template
from functools import lru_cache
import subprocess
import re
import time


@lru_cache()
def fetch_fanduel(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="fanduel")

@lru_cache()
def fetch_draftkings(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="draftkings")

@lru_cache()
def fetch_betmgm(ttl_hash=None):
    del ttl_hash
    return fetch_game_data(sportsbook="betmgm")

def fetch_game_data(sportsbook="fanduel"):
    cmd = ["python", "main.py", "-xgb", f"-odds={sportsbook}"]
    stdout = subprocess.check_output(cmd, cwd="../").decode()
    data_re = re.compile(r'\n(?P<away_team>[\w ]+)(\((?P<away_confidence>[\d+\.]+)%\))? vs (?P<home_team>[\w ]+)(\((?P<home_confidence>[\d+\.]+)%\))?: (?P<ou_pick>OVER|UNDER) (?P<ou_value>[\d+\.]+) (\((?P<ou_confidence>[\d+\.]+)%\))?', re.MULTILINE)
    ev_re = re.compile(r'(?P<team>[\w ]+) EV: (?P<ev>[-\d+\.]+)', re.MULTILINE)
    games = []
    for match in data_re.finditer(stdout):
        game_dict = {'away_team': match.group('away_team').strip(),
                     'home_team': match.group('home_team').strip(),
                     'away_confidence': match.group('away_confidence'),
                     'home_confidence': match.group('home_confidence'),
                     'ou_pick': match.group('ou_pick'),
                     'ou_value': match.group('ou_value'),
                     'ou_confidence': match.group('ou_confidence')}
        for ev_match in ev_re.finditer(stdout):
            print(ev_match.group('team'), game_dict['home_team'])
            if ev_match.group('team') == game_dict['away_team']:
                game_dict['away_team_ev'] = ev_match.group('ev')
            if ev_match.group('team') == game_dict['home_team']:
                game_dict['home_team_ev'] = ev_match.group('ev')
        print(game_dict)
        games.append(game_dict)

    print(games)
    return games


def get_ttl_hash(seconds=600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


app = Flask(__name__)

@app.route("/")
def index():
    #fanduel = fetch_fanduel(ttl_hash=get_ttl_hash())
    draftkings = fetch_draftkings(ttl_hash=get_ttl_hash())
    betmgm = fetch_betmgm(ttl_hash=get_ttl_hash())
    return render_template('index.html', data={"fanduel": fanduel, "draftkings": draftkings, "betmgm": betmgm})