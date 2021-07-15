import dataclasses
from dataclasses import dataclass
from random import randint
from typing import List

import requests

_BASE_URL = "https://bourgeoisie-birds.herokuapp.com"


@dataclass
class HighScore:
    initials: str
    score: int


def wake_up():
    """
    Wakes up the heroku server
    """
    url = _BASE_URL + '/wake-up'
    requests.get(url)


def get_high_scores() -> List[HighScore]:
    """
    Gets highest high scores from the heroku server
    """
    url = _BASE_URL + '/high-score'
    data = requests.get(url).json()
    return list(map(lambda d: HighScore(d['initials'], d['score']), data))


def put_high_score(high_score: HighScore) -> bool:
    """
    Creates and entry for the new high score and returns if successful
    """
    url = _BASE_URL + '/high-score'
    data = requests.put(url, data=dataclasses.asdict(high_score)).json()
    if "message" in data and data["message"] == "inserted":
        return True
    return False


if __name__ == "__main__":
    print("testing")
    print(put_high_score(HighScore("ADS", randint(1, 100))))
    print(get_high_scores())
