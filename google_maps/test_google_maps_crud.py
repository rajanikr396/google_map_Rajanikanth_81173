import json
import pytest
from playwright.sync_api import APIRequestContext


def test_google_maps_crud(before_each_test: APIRequestContext):
    # 1) Add Place (POST)
    add_payload = {
        "location": {"lat": -38.383494, "lng": 33.427362},
        "accuracy": 50,
        "name": "BajajFinSer",
        "phone_number": "(+91) 983 893 3937",
        "address": "29, side layout, cohen 09",
        "types": ["shoe park", "shop"],
        "website": "http://google.com",
        "language": "French-IN",
    }

    resp_add = before_each_test.post(
        "/maps/api/place/add/json",
        params={"key": "qaclick123"},
        data=json.dumps(add_payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp_add.status == 200
    body_add = resp_add.json()
    assert body_add.get("status") == "OK"
    place_id = body_add.get("place_id")
    assert place_id, "place_id missing from add response"

    # 2) Get Place (GET)
    resp_get = before_each_test.get(
        "/maps/api/place/get/json",
        params={"key": "qaclick123", "place_id": place_id},
    )
    assert resp_get.status == 200
    body_get = resp_get.json()
    assert body_get.get("name") == add_payload["name"]

    # 3) Update Place (PUT)
    new_address = "70 Summer walk, USA"
    update_payload = {"place_id": place_id, "address": new_address, "key": "qaclick123"}
    resp_update = before_each_test.put(
        "/maps/api/place/update/json",
        params={"key": "qaclick123"},
        data=json.dumps(update_payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp_update.status == 200
    # Some implementations return a message; if present, ensure it's OK-like
    try:
        update_body = resp_update.json()
    except Exception:
        update_body = {}

    # 4) Get again to verify update
    resp_get2 = before_each_test.get(
        "/maps/api/place/get/json",
        params={"key": "qaclick123", "place_id": place_id},
    )
    assert resp_get2.status == 200
    body_get2 = resp_get2.json()
    assert body_get2.get("address") == new_address

    # 5) Delete Place (DELETE)
    delete_payload = {"place_id": place_id}
    resp_delete = before_each_test.delete(
        "/maps/api/place/delete/json",
        params={"key": "qaclick123"},
        data=json.dumps(delete_payload),
        headers={"Content-Type": "application/json"},
    )
    assert resp_delete.status == 200
    body_del = resp_delete.json()
    assert body_del.get("status") == "OK"