import requests
from backend.cookie_reader import get_toolbox_cookie
from backend.models import Task

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
        """
        Fetch tasks assigned to the current user.
        Using real endpoint:
        GET https://api-c-toolbox.3cis.net/api/v1/dashboard/tasks
        """

        params = {
            "page": 1,
            "perPage": 20,
            "user": "true",
            "status": 1,
            "sortBy": "due_date",
            "sortDirection": "closest",
        }

        url = f"{BASE_URL}/dashboard/tasks"
        resp = self.session.get(url, params=params)

        if resp.status_code != 200:
            print("❌ Error fetching tasks:", resp.status_code)
            print(resp.text)
            return []

        json_data = resp.json()

        # The structure is:  { "data": { "data": [] } }
        task_list = json_data.get("data", {}).get("data", [])

        tasks = []

        for item in task_list:
            # Title
            title = (
                item.get("name") or
                item.get("project_name") or
                item.get("batch_name") or
                "Untitled Task"
            )

            # Tags from status_name and type_name
            tags = []
            if item.get("status_name"):
                tags.append(item["status_name"])
            if item.get("type_name"):
                tags.append(item["type_name"])

            # Date
            date = item.get("target_date") or item.get("due_date")

            # Note
            note = item.get("note") or "No note"

            # Task detail URL
            task_id = item.get("id")
            if task_id:
                url = f"https://c-toolbox.3cis.net/batches/{task_id}"
            else:
                url = None

            tasks.append(
                Task(
                    title=title,
                    tags=tags,
                    date=date,
                    note=note,
                    url=url
                )
            )

        return tasks
