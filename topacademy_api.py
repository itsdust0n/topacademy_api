import requests


class JournalApi:
    def __init__(self, authorization):
        self.BASE_URL = 'https://msapi.top-academy.ru/api/v2'
        self.session = requests.Session()
        self.session.headers.update({
            "authorization": f"{authorization}",
            "referer": "https://journal.top-academy.ru/"
        })

    def get_future_exams(self):
        r = self.session.get(f"{self.BASE_URL}/dashboard/info/future-exams")
        r.raise_for_status()
        return r.json()

    def get_attendance(self):
        r = self.session.get(f"{self.BASE_URL}/dashboard/chart/attendance")
        r.raise_for_status()
        return r.json()

    def get_schedule_month(self, date):
        r = self.session.get(f"{self.BASE_URL}/schedule/operations/get-month?date_filter={date}")
        r.raise_for_status()
        return r.json()

    def get_schedule_day(self, date):
        r = self.session.get(f"{self.BASE_URL}/schedule/operations/get-by-date?date_filter={date}")
        r.raise_for_status()
        return r.json()


class OmniApi():
    def __init__(self, cookie):
        self.cookie = cookie

    def get_rooms(self): # TODO
        pass

    def get_schedule(self): # TODO
        pass
