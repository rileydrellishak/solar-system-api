from flask import Blueprint, request, Response
from ..db import db
from app.models.planet import Planet
from app.models.moon import Moon
from .route_utilities import validate_model

bp = Blueprint("planets", __name__, url_prefix="/planets")

@bp.post("")
def create_planet():
    request_body = request.get_json()

    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201

@bp.post('/<planet_id>/moons')
def add_moon_to_existing_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    moon_data = request.get_json()
    moon_data['planet_id'] = planet.id
    new_moon = Moon.from_dict(moon_data)
    db.session.add(new_moon)
    db.session.commit()
    return new_moon.to_dict(), 201

@bp.get('')
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)
    result = []
    for planet in planets:
        result.append(planet.to_dict())
    return result

@bp.get('/<planet_id>/moons')
def get_moons_for_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    query = db.select(Moon).where(Moon.planet_id == planet.id).order_by(Moon.id)
    moons = db.session.scalars(query)
    return [moon.to_dict() for moon in moons]

@bp.get('/<planet_id>')
def get_single_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict(), 200

@bp.put('/<planet_id>')
def replace_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius = request_body["radius"]

    db.session.commit()

    return Response(status=204, mimetype='application/json')



@bp.delete('/<planet_id>')
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype='application/json')