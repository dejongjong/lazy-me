import pytest
from actions import todoist


@pytest.fixture
def requests_mocks(requests_mock):
    requests_mock.get(
        "https://api.todoist.com/rest/v1/projects",
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
        json=[],
    )
    requests_mock.get("https://api.todoist.com/rest/v1/sections", json=[])


def test_update_next_actions(requests_mocks):  # pylint: disable=W0613,W0621
    todoist.update_next_actions("fake-token")
