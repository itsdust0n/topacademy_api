import requests


class JournalApi():
    def __init__(self, authorization):
        self.headers = {
            "authorization": "",
            "referer": "https://journal.top-academy.ru/"
        }
        self.headers["authorization"] = authorization