from fastapi.testclient import TestClient
from app.main import create_app

def test_all_contract_routes_return_501():
    with TestClient(create_app()) as client:
        response = client.request('POST', '/referrals')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referrals/sample/reviews')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referrals/sample/findings')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/referrals')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referrals/sample/information-requests')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referrals/sample/information-requests/sample/response')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('POST', '/referral-events')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
        response = client.request('GET', '/referrals/sample')
        assert response.status_code == 501
        assert response.json() == {"error":"not_implemented","message":"CarePath behavior is not implemented."}
