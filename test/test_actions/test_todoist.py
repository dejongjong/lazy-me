import pytest
from actions.todoist import prioritise_actions


@pytest.fixture
def successful_mocks(requests_mock):
    requests_mock.get(
        "https://api.todoist.com/rest/v1/projects",
        headers={"Content-Type": "application/json"},
        json=[
            {
                "id": 220474322,
                "name": "Inbox",
                "comment_count": 10,
                "order": 1,
                "color": 47,
                "shared": False,
                "sync_id": 0,
                "favorite": False,
                "inbox_project": True,
                "url": "https://todoist.com/showProject?id=220474322",
            }
        ],
    )
    requests_mock.get(
        "https://api.todoist.com/rest/v1/labels",
        headers={"Content-Type": "application/json"},
        json=[
            {
                "id": 2156154810,
                "name": "volgende-actie",
                "color": 47,
                "order": 1,
                "favorite": False,
            },
            {
                "id": 2156154845,
                "name": "wachtend",
                "color": 47,
                "order": 1,
                "favorite": True,
            },
        ],
    )
    requests_mock.get(
        "https://api.todoist.com/rest/v1/sections",
        headers={"Content-Type": "application/json"},
        json=[],
    )
    requests_mock.get(
        "https://api.todoist.com/rest/v1/tasks?project_id=220474322",
        headers={"Content-Type": "application/json"},
        json=[],
    )


def test_prioritise_actions(successful_mocks):  # pylint: disable=W0613,W0621
    prioritise_actions("fake-token")
