import json
import pytest
from pathlib import Path
from playwright.sync_api import APIRequestContext


DATA_FILE = Path(__file__).resolve().parent / "place_data.json"


@pytest.mark.dependency(depends=["add_place"], scope="session")
@pytest.mark.order(2)
def test_get_place(before_each_test: APIRequestContext):
    data = json.loads(DATA_FILE.read_text())
    place_id = data.get("place_id")
    assert place_id

    resp = before_each_test.get(
        "/maps/api/place/get/json",
        params={"key": "qaclick123", "place_id": place_id},
    )
    assert resp.status == 200
    body = resp.json()
    assert body.get("name") == "BajajFinSer"