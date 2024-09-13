import time
from salestrackapi.domain.models import Product, Family


def test_get_product_success(test_client, db_session, product_payload, family_payload):
    product = Product(**product_payload)
    family = Family(**family_payload)
    #Create family first
    db_session.add(family)
    db_session.commit()
    test_client.get(f"/sales/family/{family.id}")
    # Now Create Product
    db_session.add(product)
    db_session.commit()
    response = test_client.get(f"sales/product/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["Status"] == "Success"
    assert data["Product"]["name"] == product_payload["name"]


# GET product (Failure case - Product not found)
def test_get_product_not_found(test_client):
    response = test_client.get("sales/product/98478") 
    assert response.status_code == 404
    assert response.json()['detail'] == "No product found for id: 98478"


# POST Product (Success case)
def test_create_product_success(test_client, db_session, family_payload, product_payload):
    # create family first
    family=Family(**family_payload)
    db_session.add(family)
    db_session.commit()
    response = test_client.post("sales/product", json=product_payload)
    data = response.json()
    assert data['Status'] == 'Success'
    assert data['Product']['name'] == product_payload['name']
    assert data["Product"]['family_id'] == family_payload['id']
    assert data["Product"]['price'] == product_payload['price']


# Update Product (Success- Case)
def test_update_product_success(test_client, db_session, family_payload, product_payload, product_payload_updated):
    family = Family(**family_payload)
    db_session.add(family)
    db_session.commit()
    response = test_client.post("sales/product", json=product_payload)
    response_json = response.json()
    assert response.status_code == 201

    # Update the created Product
    time.sleep(1)
    response = test_client.patch(
        f"sales/product/{product_payload['id']}", json=product_payload_updated
    )
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["Status"] == "Success"
    assert response_json["Product"]["id"] == product_payload["id"]
    assert response_json["Product"]["name"] == "Ikigai"