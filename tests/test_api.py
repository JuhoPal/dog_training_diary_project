from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Koiran treenipäiväkirjan API"}


def test_create_and_get_dog():
    create_response = client.post(
        "/dogs",
        json={
            "name": "Rekku",
            "breed": "Labradorinnoutaja",
            "birth_date": "2021-05-12",
            "notes": "Rauhallinen ja motivoitunut",
        },
    )
    assert create_response.status_code == 201

    dog = create_response.json()
    get_response = client.get(f"/dogs/{dog['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Rekku"


def test_create_training_for_existing_dog():
    dog_response = client.post(
        "/dogs",
        json={
            "name": "Nelli",
            "breed": "Bordercollie",
            "birth_date": "2020-02-01",
            "notes": None,
        },
    )
    dog_id = dog_response.json()["id"]

    training_response = client.post(
        "/trainings",
        json={
            "dog_id": dog_id,
            "date": "2026-03-10",
            "duration_minutes": 45,
            "training_type": "Toko",
            "location": "Koulutuskenttä",
            "notes": "Kontaktiharjoituksia",
        },
    )

    assert training_response.status_code == 201
    assert training_response.json()["dog_id"] == dog_id
    assert training_response.json()["training_type"] == "Toko"


def test_ui_api_lists_trainings_with_dog_data():
    dog_response = client.post(
        "/dogs",
        json={
            "name": "Sisu",
            "breed": "Suomenlapinkoira",
            "birth_date": "2019-01-01",
            "notes": "Innostuu helposti",
        },
    )
    assert dog_response.status_code == 201

    dog_id = dog_response.json()["id"]

    training_response = client.post(
        "/trainings",
        json={
            "dog_id": dog_id,
            "date": "2026-04-01",
            "duration_minutes": 30,
            "training_type": "Agility",
            "location": "Metsä",
            "notes": "Seuraamisharjoitus",
        },
    )
    assert training_response.status_code == 201

    ui_response = client.get("/ui/api/trainings")
    assert ui_response.status_code == 200
    data = ui_response.json()

    assert "trainings" in data
    assert data["count"] >= 1
    assert any(item["dog"]["id"] == dog_id for item in data["trainings"])
    assert any(
        item["dog"]["id"] == dog_id and item["training_type"] == "Agility"
        for item in data["trainings"]
    )


def test_ui_page_returns_html():
    response = client.get("/ui")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Koiran treenit ja harjoitukset" in response.text
