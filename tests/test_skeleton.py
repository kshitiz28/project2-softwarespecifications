from fastapi.testclient import TestClient
from app.main import create_app

def test_all_contract_routes_return_501():
    with TestClient(create_app()) as client:
        response = client.request('GET', '/referrals/sample/appointment-slots')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referrals/sample/appointments')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/booking-attempts/sample/reconcile')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('PATCH', '/appointments/sample')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/appointments/sample/history')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
