import pytest
@pytest.mark.smoke
def test_health_returns_ok(session, base_url):
    response = session.get(f"{base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}