import requests
import logging


class JournalApi:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        try:
            payload = '{"application_key":"6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6","id_city":null,"password":"' + password + '","username":"' + login +'"}'
            headers = {
                "referer": "https://journal.top-academy.ru/",
                "Content-type": "application/json"
            }
            r = requests.post("https://msapi.top-academy.ru/api/v2/auth/login", data=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            self.token = data['access_token']
            if self.token not in [None, ""]:
                self.session = requests.Session()
                self.session.headers.update({
                    "authorization": f"Bearer {self.token}",
                    "referer": "https://journal.top-academy.ru/"
                })
        except requests.RequestException as e:
            logging.error(f"Error while authorization: {e}")

    def _get(self, endpoint, method):
        url = f"https://msapi.top-academy.ru/api/v2/{endpoint}"
        try:
            r = self.session.request(method, url=url)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')

    def get_token(self):
        return self.token

    def get_future_exams(self):
        return self._get("dashboard/info/future-exams", "GET")

    def get_attendance(self):
        return self._get("dashboard/chart/attendance", "GET")

    def get_schedule_month(self, date):
        return self._get(f"schedule/operations/get-month?date_filter={date}", "GET")

    def get_schedule_day(self, date):
        return self._get(f"schedule/operations/get-by-date?date_filter={date}", "GET")

    def get_user_info(self):
        return self._get("settings/user-info", "GET")

    def get_average_grade(self):
        return self._get("dashboard/chart/average-progress", "GET")

    def get_group_leaders(self):
        return self._get("dashboard/progress/leader-group", "GET")

    def get_homework_counters(self):
        return self._get("count/homework", "GET")


class OmniApi():
    def __init__(self, cookie):
        self.cookie = cookie

    def get_rooms(self): # TODO
        pass

    def get_schedule(self): # TODO
        pass
