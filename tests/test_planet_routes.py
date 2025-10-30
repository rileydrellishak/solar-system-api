def test_get_all_planets_no_content(client):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet_with_content(client, two_planets):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == dict(id=1, description="Smallest planet and closest to the Sun. It has no moons, extreme temperature variations, and a heavily cratered surface.", name="Mars", radius=1516)

def test_get_one_planet_no_content(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response_body == {'message': f'Planet id (1) not found'}
    assert response.status_code == 404

def test_post_one_planet_success(client):
    response = client.post("/planets", json={
        "description": "Smallest planet and closest to the Sun. It has no moons, extreme temperature variations, and a heavily cratered surface.",
        "name": "Mercury",
        "radius": 1516
    })

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "description": "Smallest planet and closest to the Sun. It has no moons, extreme temperature variations, and a heavily cratered surface.",
        "name": "Mercury",
        "radius": 1516,
        'id': 1
    }