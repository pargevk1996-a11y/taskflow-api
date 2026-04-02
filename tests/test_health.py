from app.api.v1.endpoints.health import health_check


def test_health_ok():
    assert health_check() == {"status": "ok"}
