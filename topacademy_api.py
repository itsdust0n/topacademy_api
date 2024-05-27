import requests


class JournalApi():
    def __init__(self, authorization):
        self.headers = {
            "authorization": "",
            "referer": "https://journal.top-academy.ru/"
        }
        self.headers["authorization"] = authorization

    def get_future_exams(self):
        url = "https://msapi.top-academy.ru/api/v2/dashboard/info/future-exams"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_schedule_month(self, date):
        url = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={date}"
        r = requests.get(url, headers=self.headers)
        return r.json()