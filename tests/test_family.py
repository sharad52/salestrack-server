from salestrack.domain.models import Family

# GET family (Success case)
def test_get_family_success(test_client, db_session, family_payload):
    family = Family(**family_payload)
    db_session.add(family)
    db_session.commit()
    response = test_client.get(f"sales/family/{family.id}")
    assert response.status_code == 200
    data = response.json()
    assert data['Status'] == 'Success'
    assert data['Family']['name'] == family_payload['name']

# GET family (Failure case - Family not found)
def test_get_family_not_found(test_client):
    response = test_client.get("sales/family/99999") 
    assert response.status_code == 404
    assert response.json()['detail'] == "No product found for id: 99999"

# POST family (Success case)
def test_create_family_success(test_client, family_payload):
    response = test_client.post("sales/family", json=family_payload)
    assert response.status_code == 201
    data = response.json()
    assert data['Status'] == 'Success'
    assert data['Family']['name'] == family_payload['name']

# POST family (Failure case - Invalid input)
def test_create_family_invalid_input(test_client):
    invalid_data = {
        "description": "Missing name"
    }
    response = test_client.post("sales/family", json=invalid_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Field required"
