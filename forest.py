import random
from ar import Square


class Forest:
    def __init__(self, size=5, forest_density=0.5, humidity=[0.0, 1.0], square_size=100):
        """
        :param size: array size
        :param forest_density: percent of green areas
        :param humidity:
        0 - humidity 0 - 33%
        1 - humidity 33 - 66%
        2 - humidity 66 - 99%
        """
        self.size = size
        self.forest_density = forest_density
        self.square_size = square_size
        self.forest = []

        for i in range(size):
            line = []
            for c in range(size):
                if random.random() < self.forest_density:
                    wood = 120 + random.random() * 240.0 / 100 * square_size
                    local_humidity = humidity[0] + random.random()*(humidity[1]-humidity[0])
                    line.append(Square(x=c, y=i, wood=wood, fire=0.0, humidity=local_humidity, square_size=square_size))
                else:
                    line.append(Square(x=c, y=i, wood=0.0, fire=0.0, humidity=0.0, square_size=square_size))
            self.forest.append(line)


