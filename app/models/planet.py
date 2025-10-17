# 1. Define a `Planet` class with the attributes `id`, `name`, and `description`, and one additional attribute
#Create a list of `Planet` instances

class Planet:
    def __init__(self, id, name, description, radius):
        self.id = id
        self.name = name
        self.description = description
        self.radius = radius

planets = [
    Planet(1, 'Mercury', 'Smallest planet and closest to the Sun. It has no moons, extreme temperature variations, and a heavily cratered surface.', 1516),
    Planet(2, 'Venus', 'Second planet from the Sun, with a thick carbon dioxide atmosphere that creates a severe greenhouse effect, making it the hottest planet.', 3760),
    Planet(3, 'Earth', 'The third planet from the Sun and where we live! It has a solid surface, liquid water, and a protective atmosphere.', 3963)
]