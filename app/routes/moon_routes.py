from flask import Blueprint, request, Response
from ..db import db
from app.models.moon import Moon
from .route_utilities import validate_model

bp = Blueprint("moons", __name__, url_prefix="/moons")

@bp.get('')
def get_all_moons():
    query = db.select(Moon).order_by(Moon.id)
    moons = db.session.scalars(query)
    result = []
    for moon in moons:
        result.append(moon.to_dict())
    return result

@bp.post('')
def create_moon():
    request_body = request.get_json()

    new_moon = Moon.from_dict(request_body)

    db.session.add(new_moon)
    db.session.commit()

    return new_moon.to_dict(), 201