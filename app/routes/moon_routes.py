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