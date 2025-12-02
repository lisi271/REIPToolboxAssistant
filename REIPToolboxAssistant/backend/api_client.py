import requests
from .cookie_reader import get_toolbox_cookie
from .models import Task


BASE_URL = "https://c-toolbox.3cis.net"


class ToolboxAPI:
    def __init__(self):
        self.session = requests.Session()

        cookie_name, cookie_value = get_toolbox_cookie()
        if cookie_name:
            self.session.cookies.set(cookie_name, cookie_value, domain=".3cis.net")

    def get_tasks(self):
        url = f"{BASE_URL}/api/tasks/my"  # placeholder until we confirm endpoint

        response = self.session.get(url)
        if response.status_code != 200:
            return []

        tasks_json = response.json()

        tasks = []
        for item in tasks_json:
            tasks.append(
                Task(
                    title=item.get("title"),
                    tags=item.get("tags", []),
                    date=item.get("date"),
                    note=item.get("note"),
                    url=item.get("url"),
                )
            )
        return tasks
