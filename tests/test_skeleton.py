from fastapi.testclient import TestClient
from app.main import create_app

def test_all_contract_routes_return_501():
    with TestClient(create_app()) as client:
        response = client.request('POST', '/tasks')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/patients/sample/tasks')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/tasks/sample/documents')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/tasks/sample/documents/sample')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/tasks/sample/complete')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/tasks/sample')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
