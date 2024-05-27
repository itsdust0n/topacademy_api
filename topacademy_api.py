import requests


class JournalApi():
    def __init__(self, authorization):
        self.headers = {
            "authorization": f"{authorization}",
            "referer": "https://journal.top-academy.ru/"
        }

    def get_future_exams(self):
        url = "https://msapi.top-academy.ru/api/v2/dashboard/info/future-exams"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_attendance(self):
        url = "https://msapi.top-academy.ru/api/v2/dashboard/chart/attendance"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_schedule_month(self, date):
        url = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={date}"
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_schedule_day(self, date):
        url = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date?date_filter={date}"
        r = requests.get(url, headers=self.headers)
        return r.json()


class OmniApi():
    def __init__(self, cookie):
        self.cookie = cookie

    def get_rooms(self): # TODO
        pass

    def get_schedule(self): # TODO
        pass