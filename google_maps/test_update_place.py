import json
import pytest
from pathlib import Path
from playwright.sync_api import APIRequestContext


DATA_FILE = Path(__file__).resolve().parent / "place_data.json"


@pytest.mark.dependency(depends=["add_place"], scope="session")
@pytest.mark.order(3)
def test_update_place(before_each_test: APIRequestContext):
    data = json.loads(DATA_FILE.read_text())
    place_id = data.get("place_id")
    assert place_id

    new_address = "70 Summer walk, USA"
    payload = {"place_id": place_id, "address": new_address, "key": "qaclick123"}

    resp = before_each_test.put(
        "/maps/api/place/update/json",
        params={"key": "qaclick123"},
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 200

    # verify via GET
    resp_get = before_each_test.get(
        "/maps/api/place/get/json",
        params={"key": "qaclick123", "place_id": place_id},
    )
    assert resp_get.status == 200
    body = resp_get.json()
    assert body.get("address") == new_address