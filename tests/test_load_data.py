import io
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import based on your project structure
from app import models  # Adjust the import based on your project structure
from sqlalchemy.orm import Session
from unittest.mock import patch

client = TestClient(app)

@pytest.mark.asyncio
async def test_load_data():
    # Create a mock Excel file
    data = {
        'Family': ['Electronics', 'Books'],
        'Product Name': ['Laptop', 'Python Book'],
        'Product ID': [101, 102],
        'Price': [999.99, 29.99],
        '2024-01-01': [10, 5],
        '2024-02-01': [15, 10]
    }
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)

    # Mock the database session
    with patch('app.routers.load_data.get_db') as mock_get_db:
        mock_db = Session()  # Use a mock database session or an in-memory database
        mock_get_db.return_value = mock_db

        # Perform the request
        response = client.post(
            "/load-data",
            files={"file": ("test_data.xlsx", excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"type": "test_type"}
        )

        # Assert response status
        assert response.status_code == 200
        assert response.json() == "Success!!!"

        # Add more assertions to check if the data was processed correctly
        # For example, verify that the correct entries were added to the database
        # Example:
        # family = mock_db.query(models.Family).filter(models.Family.name == 'Electronics').first()
        # assert family is not None
        # product = mock_db.query(models.Product).filter(models.Product.name == 'Laptop').first()
        # assert product is not None
        # sales = mock_db.query(models.Sales).filter(models.Sales.product_id == product.id).all()
        # assert len(sales) == 2
