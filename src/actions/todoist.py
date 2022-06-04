from datetime import datetime
from typing import Any, Dict

import requests
from requests.models import Response
from typeguard import typechecked


@typechecked
class TodoistApi:
    headers: Dict[str, str]
    api_url: str = "https://api.todoist.com/rest/v1"

    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": f"Bearer {token}"}

    def get(
        self, resource, headers: Dict[str, str] | None = None, **kwargs
    ) -> str | Any:
        headers = headers or {}
        res = requests.get(
            url=f"{self.api_url}/{resource}",
            headers={**self.headers, **headers},
            **kwargs,
        )
        assert res.status_code == 200, res.text

        if res.headers.get("Content-Type") == "application/json":
            return res.json()
        else:
            return res.text

    def post(
        self, resource, json, headers: Dict[str, str] | None = None, **kwargs
    ) -> Response:
        headers = headers or {}
        res = requests.post(
            url=f"{self.api_url}/{resource}",
            headers={**self.headers, "Content-Type": "application/json", **headers},
            json=json,
            **kwargs,
        )
        assert res.status_code == 204, res.text

        return res


@typechecked
def update_next_actions(
    token: str, next_action_label: str | None = None, debug: bool | None = False
) -> None:
    if next_action_label is None:
        next_action_label = "volgende-actie"

    api = TodoistApi(token)
    projects = api.get("projects")
    labels = api.get("labels")
    sections = api.get("sections")
    label_ids = {x["name"]: x["id"] for x in labels}

    progress_messages = []
    _progress = lambda message: progress_messages.append(message)

    updated_tasks = []
    next_action_id = label_ids[next_action_label]

    for project in projects:
        if project["name"].endswith(" ·"):
            continue

        _progress(f"project: {project['name']}")

        tasks = api.get("tasks", params={"project_id": project["id"]})
        project_sections = [x for x in sections if x["project_id"] == project["id"]]

        for section in [{"name": "No section", "id": 0}, *project_sections]:
            if section["name"].endswith(" ·"):
                continue

            _progress(f"  section: {section['name']}")

            section_tasks = [x for x in tasks if x.get("section_id") == section["id"]]
            section_tasks.sort(key=lambda x: x["order"])

            for i, task in enumerate(section_tasks):
                _progress(f"    task: {task['content']}")

                due_date_str = task.get("due", {}).get("date", "")[:10]
                far_in_the_future = False

                if due_date_str:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                    days_until_due = (due_date.date() - datetime.today().date()).days
                    _progress(f"      days_until_due: {days_until_due}")

                    if days_until_due > 1:
                        far_in_the_future = True

                if (
                    i == 0
                    and next_action_id not in task["label_ids"]
                    and not far_in_the_future
                ):
                    task["label_ids"].append(next_action_id)
                    updated_tasks.append(
                        {"id": task["id"], "label_ids": task["label_ids"]}
                    )

                elif next_action_id in task["label_ids"]:
                    task["label_ids"].remove(next_action_id)
                    updated_tasks.append(
                        {"id": task["id"], "label_ids": task["label_ids"]}
                    )

    for task in updated_tasks:
        api.post(f"tasks/{task['id']}", task)

    return progress_messages
