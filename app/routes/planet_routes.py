from flask import abort, Blueprint, make_response, request
from ..db import db
from app.models.planet import Planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    name = request_body["name"]
    description = request_body["description"]
    radius = request_body["radius"]

    new_planet = Planet(name=name, description=description, radius=radius)

    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "radius": new_planet.radius
    }

    return response, 201

@planets_bp.get('')
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)
    result = []
    for planet in planets:
        result.append(dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius))
    return result

# Waves 1-2 Routes
# @planets_bp.get('/<planet_id>')
# def get_single_planet(planet_id):
#     planet = validate_planet(planet_id)
#     return dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius)
        
# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         response = {'message': f'Planet id ({planet_id}) invalid'}
#         abort(make_response(response, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
        
#     response = {'message': f'Planet id ({planet_id}) not found'}
#     abort(make_response(response, 404))