import time 
# from tests.conftest import test_client


def test_create_get_family(test_client, family_payload):
    response = test_client.post("/sales/family", json=family_payload)
    response_json = response.json()
    assert response.status_code == 201
    family_id = response_json.get("Family").get("id")

    #Get Created Family
    response = test_client.get(f"/sales/family/{family_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["Family"]["name"] == "Book"
