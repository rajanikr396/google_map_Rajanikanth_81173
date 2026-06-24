import json
import pytest
from pathlib import Path
from playwright.sync_api import APIRequestContext


DATA_FILE = Path(__file__).resolve().parent / "place_data.json"


@pytest.mark.dependency(name="add_place", scope="session")
@pytest.mark.order(1)
def test_add_place(before_each_test: APIRequestContext):
    payload = {
        "location": {"lat": -38.383494, "lng": 33.427362},
        "accuracy": 50,
        "name": "BajajFinSer",
        "phone_number": "(+91) 983 893 3937",
        "address": "29, side layout, cohen 09",
        "types": ["shoe park", "shop"],
        "website": "http://google.com",
        "language": "French-IN",
    }

    resp = before_each_test.post(
        "/maps/api/place/add/json",
        params={"key": "qaclick123"},
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status == 200
    body = resp.json()
    assert body.get("status") == "OK"
    place_id = body.get("place_id")
    assert place_id

    # persist place_id for other tests
    DATA_FILE.write_text(json.dumps({"place_id": place_id}, indent=2))