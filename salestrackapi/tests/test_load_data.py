import io
import pandas as pd


def test_load_data(test_client, excel_load_data_payload):
    df = pd.DataFrame(excel_load_data_payload)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)

    response = test_client.post(
        "sales/load-data",
        files={"file": ("test_data.xlsx", excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"type": "monthly"}
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json['status_code'] == 201
    assert response_json["message"] == "excel data loaded successfully"
