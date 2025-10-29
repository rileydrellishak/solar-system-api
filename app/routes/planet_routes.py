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


