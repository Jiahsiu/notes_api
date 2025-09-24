from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    rv = client.get("/openapi.json")
    assert rv.status_code == 200