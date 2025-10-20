from flask import abort, Blueprint, make_response
from app.models.planet import planets

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.get('')
def get_all_planets():
    result = []
    for planet in planets:
        result.append(dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius))
    return result

@planets_bp.get('/<planet_id>')
def get_single_planet(planet_id):
    planet = validate_planet(planet_id)
    return dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius)
        
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {'message': f'Planet id ({planet_id}) invalid'}
        abort(make_response(response, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet
        
    response = {'message': f'Planet id ({planet_id}) not found'}
    abort(make_response(response, 404))