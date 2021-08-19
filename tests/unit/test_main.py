from src.main import ping


def test_ping():
    assert ping() == "pong"
