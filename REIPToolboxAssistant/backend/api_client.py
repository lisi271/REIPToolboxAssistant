import requests
import urllib3

from backend.cookie_reader import get_toolbox_cookie
from backend.models import Task

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://api-c-toolbox.3cis.net/api/v1"


class ToolboxAPI:
    def __init__(self):
        self.session = requests.Session()

        cookie_name, cookie_value = get_toolbox_cookie()
        if cookie_name:
            self.session.cookies.set(cookie_name, cookie_value, domain=".3cis.net")
        else:
            print("❌ No toolbox cookie found!")

    def get_tasks(self):

        params = {
            "page": 1,
            "perPage": 20,
            "user": "true",
            "status": 1,
            "sortBy": "due_date",
            "sortDirection": "closest",
        }

        url = f"{BASE_URL}/dashboard/tasks"

        try:
            resp = self.session.get(url, params=params, verify=False)
        except Exception as e:
            print("❌ Error during request:", e)
            return []

        if resp.status_code != 200:
            print("❌ Error fetching tasks:", resp.status_code)
            print(resp.text)
            return []

        json_data = resp.json()

        task_list = json_data.get("data", {}).get("data", [])

        tasks = []

        for item in task_list:
            title = (
                item.get("name")
                or item.get("project_name")
                or item.get("batch_name")
                or "Untitled Task"
            )

            tags = []
            if item.get("status_name"):
                tags.append(item["status_name"])
            if item.get("type_name"):
                tags.append(item["type_name"])

            date = item.get("target_date") or item.get("due_date")

            note = item.get("note") or "No note"

            task_id = item.get("id")
            if task_id:
                detail_url = f"https://c-toolbox.3cis.net/batches/{task_id}"
            else:
                detail_url = None

            tasks.append(
                Task(
                    title=title,
                    tags=tags,
                    date=date,
                    note=note,
                    url=detail_url,
                )
            )

        return tasks
