from app.models.planet import Planet
import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_planets(app):
    # make planet
    planet_1 = Planet(description="Smallest planet and closest to the Sun. It has no moons, extreme temperature variations, and a heavily cratered surface.", name="Mars", radius=1516)
    
    planet_2 = Planet(description="Second planet from the Sun, with a thick carbon dioxide atmosphere that creates a severe greenhouse effect, making it the hottest planet.", name='Venus', radius=3760)

    #add to db
    db.session.add_all([planet_1, planet_2])
    
    # save to db
    db.session.commit()