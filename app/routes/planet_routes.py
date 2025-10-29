from flask import abort, Blueprint, make_response, request, Response
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
    query = db.select(Planet)

    name_param = request.args.get('name')
    if name_param:
        query = query.where(Planet.name == name_param)
    
    description_param = request.args.get('description')
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    # Find planets with radius in range
    min_radius = request.args.get('min_radius')
    max_radius = request.args.get('max_radius')
    if min_radius is not None:
        query = query.where(Planet.radius >= min_radius)
    if max_radius is not None:
        query = query.where(Planet.radius <= max_radius)

    # Exact match radius
    radius_param = request.args.get('radius')
    if radius_param:
        query = query.where(Planet.radius == radius_param)

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    result = []
    for planet in planets:
        result.append(dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius))

    return result

@planets_bp.get('/<planet_id>')
def get_single_planet(planet_id):
    planet = validate_planet(planet_id)

    response = dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius)

    return response, 200
        
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {'message': f'Planet id ({planet_id}) invalid'}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)
    
    if not planet:
        response = {'message': f'Planet id ({planet_id}) not found'}
        abort(make_response(response, 404))
    
    return planet

@planets_bp.put('/<planet_id>')
def replace_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()
    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius = request_body["radius"]

    db.session.commit()

    return Response(status=204, mimetype='application/json')



@planets_bp.delete('/<planet_id>')
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype='application/json')