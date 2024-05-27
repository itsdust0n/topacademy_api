import requests
import logging


class JournalApi:
    def __init__(self, authorization):
        self.session = requests.Session()
        self.session.headers.update({
            "authorization": f"{authorization}",
            "referer": "https://journal.top-academy.ru/"
        })

    def _get(self, endpoint, method):
        url = f"https://msapi.top-academy.ru/api/v2/{endpoint}"
        try:
            r = self.session.request(method, url=url)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')

    def get_future_exams(self):
        return self._get("dashboard/info/future-exams", "GET")

    def get_attendance(self):
        return self._get("dashboard/chart/attendance", "GET")

    def get_schedule_month(self, date):
        return self._get(f"schedule/operations/get-month?date_filter={date}", "GET")

    def get_schedule_day(self, date):
        return self._get(f"schedule/operations/get-by-date?date_filter={date}", "GET")


class OmniApi():
    def __init__(self, cookie):
        self.cookie = cookie

    def get_rooms(self): # TODO
        pass

    def get_schedule(self): # TODO
        pass
