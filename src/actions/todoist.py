import requests
from typing import Dict, Any
from pprint import pprint
from uuid import uuid1 as uuid


class TodoistApi:
    headers: Dict[str, Any]
    api_url = "https://api.todoist.com/rest/v1"
    
    def __init__(self, token: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}"
        }
        
    def get(self, resource, headers={}, **kwargs):
        res = requests.get(
            url=f"{self.api_url}/{resource}",
            headers={
                **self.headers,
                **headers
            },
            **kwargs
        )
        assert res.status_code == 200
        
        if res.headers.get("Content-Type") == "application/json":
            return res.json()
        else:
            return res.text
            
    def post(self, resource, json, headers={}, **kwargs):
        res = requests.post(
            url=f"{self.api_url}/{resource}",
            headers={
                **self.headers,
                "Content-Type": "application/json",
                **headers
            },
            json=json,
            **kwargs
        )
        assert res.status_code == 204
        
        return res
        

def update_next_actions(token, next_action_label=None, debug=False):
    if next_action_label is None:
        next_action_label = "volgende-actie"
    
    api = TodoistApi(token)
    projects = api.get("projects")
    labels = api.get("labels")
    sections = api.get("sections")
    label_ids = {
        x["name"]: x["id"]
        for x in labels
    }
    _print = lambda message: print(message) if debug else None
    
    updated_tasks = []
    next_action_id = label_ids[next_action_label]
    
    for project in projects:
        if project['name'].endswith(" ·"):
            continue
            
        _print(f"project: {project['name']}")
        
        tasks = api.get("tasks", params={"project_id": project["id"]})
        project_sections = [
            x for x in sections 
            if x["project_id"] == project["id"]
        ]
        
        for section in [{"name": "No section", "id": 0}, *project_sections]:
            if section["name"].endswith(" ·"):
                continue
            
            _print(f"  section: {section['name']}")
            
            section_tasks = [
                x for x in tasks
                if x.get("section_id") == section["id"]
            ]
            section_tasks.sort(key=lambda x: x["order"])
            
            for i, task in enumerate(section_tasks):
                _print(f"    task: {task['content']}")
                
                if i == 0 and next_action_id not in task["label_ids"]:
                    task["label_ids"].append(next_action_id)
                    updated_tasks.append({
                        "id": task["id"],
                        "label_ids": task["label_ids"]
                    })
                
                elif i > 0 and next_action_id in task["label_ids"]:
                    task["label_ids"].remove(next_action_id)
                    updated_tasks.append({
                        "id": task["id"],
                        "label_ids": task["label_ids"]
                    })
    
    for task in updated_tasks:
        api.post(f"tasks/{task['id']}", task)

