from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    radius: Mapped[int]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    @classmethod
    def from_dict(cls, planet_data):
        new_planet = cls(
            name=planet_data['name'],
            description=planet_data['description'],
            radius=planet_data['radius']
            )
        return new_planet
    
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "radius": self.radius
        }