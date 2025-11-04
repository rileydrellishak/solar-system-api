from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    radius: Mapped[int]
    description: Mapped[str]
    year_discovered: Mapped[int]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey('planet.id'))
    planet: Mapped[Optional['Planet']] = relationship(back_populates='moons')

    @classmethod
    def from_dict(cls, moon_data):
        new_moon = cls(
            name=moon_data['name'],
            description=moon_data['description'],
            radius=moon_data['radius'],
            year_discovered=moon_data['year_discovered'],
            planet_id=moon_data.get('planet_id', None)
            )
        return new_moon
    
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "radius": self.radius,
        "year_discovered": self.year_discovered,
        "planet": self.planet.name if self.planet_id else None
        }