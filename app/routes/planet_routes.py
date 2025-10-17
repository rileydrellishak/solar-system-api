# 1. ...to get all existing `planets`, so that I can see a list of `planets`, with their `id`, `name`, `description`, and other data of the `planet`.
from flask import Blueprint
from app.models.planet import planets

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.get('')
def get_all_planets():
    result = []
    for planet in planets:
        result.append(dict(id=planet.id, name=planet.name, description=planet.description, radius=planet.radius))
    return result