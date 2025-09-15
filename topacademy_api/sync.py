import requests
import logging


class JournalApi:
    BASE_URL = "https://msapi.top-academy.ru/api/v2"
    APP_KEY = "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6"

    def __init__(self):
        self.token = None
        self.session = requests.Session()

    # ----------------- Authorization as teacher -----------------
    def authorize_as_teacher(self, id_city: int, login: str, password: str):
        payload = {
            "application_key": self.APP_KEY,
            "id_city": id_city,
            "username": login,
            "password": password
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": "Bearer null",
            "content-type": "application/json",
            "referer": "https://journal.top-academy.ru/",
            "x-cache-client": "600"
        }
        r = self.session.post(f"{self.BASE_URL}/auth/login-admin", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        self.token = data.get("access_token")
        if not self.token:
            raise RuntimeError("Teacher login failed: no token")
        self.session.headers.update({
            "authorization": f"Bearer {self.token}",
            "referer": "https://journal.top-academy.ru/",
            "x-cache-client": "600"
        })

        # logout_as_student must be after login-admin
        self.logout_as_student()

    # ----------------- Logout as student -----------------
    def logout_as_student(self):
        if not hasattr(self, "session") or self.session is None:
            raise RuntimeError("Not authorized as admin")

        headers = {"content-type": "application/json", "x-cache-client": "600"}
        r = self.session.post(f"{self.BASE_URL}/auth/logout-as-student", json={}, headers=headers)

        # code 205 is okay, ignore it
        if r.status_code not in (200, 205):
            raise RuntimeError(f"logout_as_student failed: {r.status_code}")

        try:
            return r.json()
        except ValueError:
            return None

    # ----------------- Get groups linked to teacher -----------------
    def get_teacher_groups(self):
        r = self.session.get(f"{self.BASE_URL}/settings/admin-groups")
        r.raise_for_status()
        return r.json()

    # ----------------- Get students in group -----------------
    def get_group_students(self, group_id: int):
        r = self.session.get(f"{self.BASE_URL}/settings/admin-group-students?id={group_id}")
        r.raise_for_status()
        return r.json()

    # ----------------- Login as student -----------------
    def login_as_student(self, student_id: int):
        self.logout_as_student()

        payload = {"id": student_id}
        headers = {"x-cache-client": "600"}

        r = self.session.post(f"{self.BASE_URL}/auth/login-as-student", json=payload, headers=headers)

        # code 205 is okay, ignore it
        if r.status_code not in (200, 205):
            raise RuntimeError(f"login_as_student failed: {r.status_code}")

        try:
            data = r.json()
        except ValueError:
            data = None

        if data is not None and "access_token" in data:
            self.token = data["access_token"]
            self.session.headers.update({"authorization": f"Bearer {self.token}"})

        # get student info
        r_info = self.session.get(f"{self.BASE_URL}/settings/user-info")
        try:
            student_info = r_info.json()
        except ValueError:
            student_info = None

        return student_info

    def _get(self, endpoint, method):
        url = f"https://msapi.top-academy.ru/api/v2/{endpoint}"
        try:
            r = self.session.request(method, url=url)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')

    # ----------------- Regular API methods -----------------
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
