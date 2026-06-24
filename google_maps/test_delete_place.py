import json
import pytest
from pathlib import Path
from playwright.sync_api import APIRequestContext


DATA_FILE = Path(__file__).resolve().parent / "place_data.json"


@pytest.mark.dependency(depends=["add_place"], scope="session")
@pytest.mark.order(4)
def test_delete_place(before_each_test: APIRequestContext):
    data = json.loads(DATA_FILE.read_text())
    place_id = data.get("place_id")
    assert place_id

    payload = {"place_id": place_id}

    resp = before_each_test.delete(
        "/maps/api/place/delete/json",
        params={"key": "qaclick123"},
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 200
    body = resp.json()
    assert body.get("status") == "OK"