import random
from forest import Forest
import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors


def mph_to_kmh(mph):
    return mph * 1.609


def kmh_to_mph(kmh):
    return kmh / 1.609


def fire_speed(kmh):
    mph = kmh_to_mph(kmh)
    y = -1.27206625 * 10 ** (-3) * mph ** 3 + 6.74299842 * 10 ** (-2) * mph ** 2 - 7.45760798 * 10 ** (
        -1) * mph + 3.1844528
    speed = mph_to_kmh(y)
    return speed


class BurnTheForest:
    def __init__(self, forest, wind_power=0, wind_direction='N'):
        self.forest = forest
        self.wind_power = wind_power
        self.square_size = self.forest.forest[0][0].square_size
        self.wind_direction = wind_direction
        self.f_speed_squares = 0

    def start_fire(self, power):
        """
        :param power:
        n - fire random(10n, 10(n+1))
        """
        ar = random.choice([a for a in sum(self.forest.forest, []) if a.wood > 0])
        ar.fire = 10 * power + random.random() * 10

    def burn(self):
        for row in self.forest.forest:
            for ar in row:
                if ar.fire > 0:
                    ar.wood -= math.log(ar.fire)
                    ar.fire += math.log(ar.fire)
                    if self.f_speed_squares < 0:
                        ar.fire += self.f_speed_squares
                        if ar.fire < 0:
                            ar.fire = 0
                    if ar.wood <= 0:
                        ar.wood = 0
                        ar.fire = 0
                        ar.humidity = 0
                    elif ar.fire > 1000:
                        ar.fire = 1000

    def wind_range(self):
        f_speed = fire_speed(self.wind_power)
        f_speed_squares = math.ceil(f_speed / 6.0 * 1000 / self.square_size)
        scope = []
        if self.wind_power < 10:
            scope = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), ]
        elif f_speed_squares > 0:
            x_range = int(math.ceil(f_speed_squares / 2.))
            y_range = int(math.ceil(f_speed_squares / 4.))
            for x in range(-x_range, x_range + 1):
                for y in range(-y_range, y_range + 1):
                    if (1.0 * x / x_range) ** 2 + (1.0 * y / y_range) ** 2 <= 1:
                        power = 1 - math.sqrt(x ** 2 + y ** 2) / x_range
                        scope.append((x, y, power))
            if self.wind_direction == 'W':
                scope = [(y + x_range + 1, x, power) for (x, y, power) in scope]
            elif self.wind_direction == 'E':
                scope = [(x - x_range + 1, y, power) for (x, y, power) in scope]
            elif self.wind_direction == 'S':
                scope = [(y, x - x_range + 1, power) for (x, y, power) in scope]
            else:
                scope = [(x, y + x_range + 1, power) for (x, y, power) in scope]
        elif self.wind_power >= 110:
            destroy_trees = int(-f_speed)
            for i in range(destroy_trees):
                x = random.randint(0, self.forest.size - 1)
                y = random.randint(0, self.forest.size - 1)
                self.forest.forest[x][y].wood -= 30
                if self.forest.forest[x][y].wood <= 0:
                    self.forest.forest[x][y].wood = 0
                    self.forest.forest[x][y].fire = 0

        for i in range(int(0.2 * len(scope))):
            a = random.choice(range(len(scope)))
            area = list(scope[a])
            area[0] += random.choice([-2, -1, 1, 2])
            area[1] += random.choice([-2, -1, 1, 2])
            scope[a] = tuple(area)
        scope = [(x, y, power) for (x, y, power) in scope if not (x == 0 and y == 0)]
        self.f_speed_squares = f_speed_squares
        return scope

    def next_step(self):
        new_to_burn = self.wind_range()
        self.wind_power += 2
        for burning_ar in [a for a in sum(self.forest.forest, []) if a.fire > 10]:
            for areas in new_to_burn:
                x = burning_ar.x + areas[0]
                y = burning_ar.y + areas[1]
                if 0 <= x < self.forest.size and 0 <= y < self.forest.size:
                    if self.forest.forest[y][x].wood > 0:
                        burn_prop = random.random()
                        if burn_prop > self.forest.forest[x][y].humidity:
                            self.forest.forest[y][x].fire += (burning_ar.fire * areas[2])
                            if self.forest.forest[y][x].fire > 1000:
                                self.forest.forest[y][x].fire = 1000

    def prepare_data_to_draw(self):
        data = []
        for row in self.forest.forest:
            line = []
            for ar in row:
                if ar.fire > 0:
                    line.append(-ar.fire)
                else:
                    line.append(ar.wood)
            data.append(line)

        df = pd.DataFrame(data)
        return df

    def animate(self, steps=10, start_fire_power=0):
        fig = plt.figure()

        colors = ['#990000', '#CC0000', '#FF0000', '#FF8000', '#FFFF00',
                  '#AFCB96',
                  '#66FF66', '#33FF33', '#00FF00', '#00CC00', '#009900']
        scale = [-1000, -80, -60, -40, -20, -0.1, 0.1, 50, 100, 200, 400, 1000]
        cmap, norm = mcolors.from_levels_and_colors(scale, colors)

        df = self.prepare_data_to_draw()
        images = [[plt.pcolor(df, cmap=cmap, norm=norm)]]

        self.start_fire(start_fire_power)
        df = self.prepare_data_to_draw()
        images.append([plt.pcolor(df, cmap=cmap, norm=norm)])
        drzewa = [sum([x.wood for x in sum(self.forest.forest, [])])]
        ogien = [sum([x.fire for x in sum(self.forest.forest, [])])]
        for i in range(steps):
            print i
            self.next_step()
            self.burn()
            drzewa.append(sum([x.wood for x in sum(self.forest.forest, [])]))
            ogien.append(sum([x.fire for x in sum(self.forest.forest, [])]))
            df = self.prepare_data_to_draw()
            images.append([plt.pcolor(df, cmap=cmap, norm=norm,)])

        ani = animation.ArtistAnimation(fig, images, interval=500, repeat_delay=0, repeat=True)
        plt.show()

        plt.plot(range(0, steps + 1), drzewa)
        plt.show()

        plt.plot(range(0, steps + 1), ogien)
        plt.show()


def run(size=100, forest_density=0.80, humidity=None, square_size=100, wind_power=0, wind_direction='N',
            steps=80, start_power=1):
    if humidity is None:
        humidity = [0.0, 0.99]
    f = Forest(size=size, forest_density=forest_density, humidity=humidity, square_size=square_size)
    btf = BurnTheForest(f, wind_power=wind_power, wind_direction=wind_direction)
    btf.animate(steps=steps, start_fire_power=start_power)
run()