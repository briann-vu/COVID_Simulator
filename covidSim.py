'''
Brian Vu
covidSim.py

Description:
'''

import random
from three_shapes_game import *


def main():
    print("Welcome to the COVID-19 Simulator")
    print("Please fill out this form:")
    print()

    # fix string input on int(input())
    population = int(input("Population size (50 looks fine): "))
    infected_pop = int(input("Number of people already carrying COVID-19: "))
    population -= infected_pop

    infected_mask_type = None
    while True:
        type1 = input(
            "Are these infected people wearing masks? (yes or no): ")
        if type1.upper() == "YES":
            infected_mask_type = "mask"
            break
        elif type1.upper() == "NO":
            infected_mask_type = "none"
            break
        else:
            continue

    while True:
        healthy_masks = int(input(
            "How many healthy people are wearing masks? (" + str(population) + " people left): "))
        if healthy_masks == population:
            break
        elif healthy_masks > population:
            continue
        elif healthy_masks < 0:
            continue
        else:
            break
    healthy_no_masks = population - healthy_masks
    print("This leaves " + str(healthy_no_masks) +
          " healthy people without masks")

    print("healthy: " + str(healthy_masks))
    print("healthyNo: " + str(healthy_no_masks))
    print("infected: " + str(infected_pop))

    dummy = input("Press 'ENTER' to continue")

    wid = 600
    hei = 600

    # This creates the Game object. The first param is the window name;
    # the second is the framerate you want (20 frames per second, in this
    # example); the last is the window / game space size.
    game = Game("COVID-19 Simulator", 40, wid, hei)
    background = Background()
    # This affects how the distance calculation in the "nearby" calls
    # works; the default is to measure center-to-center. But if anybody
    # wants to measure edge-to-edge, they can turn on this feature.
    # game.config_set("account_for_radii_in_dist", True)

    # spawn_background(game)

    i = 0
    while i < healthy_masks:  # fix spawn ammount
        spawn_healthy(game, wid, hei, "mask")
        print("Spawned healthy masker number", i + 1)
        i += 1

    l = 0
    while l < healthy_no_masks:
        spawn_healthy(game, wid, hei, "none")
        print("Spawned healthy no masker number", l + 1)
        l += 1

    j = 0
    while j < infected_pop:
        spawn_infected(game, wid, hei, infected_mask_type)
        print("Spawned infected number", j + 1)
        j += 1

    # game loop. Runs forever, unless the game ends.
    count = 0
    while not game.is_over():
        game.do_nearby_calls()
        game.do_move_calls()
        game.do_edge_calls()
        game.execute_removes()
        game.draw()


def spawn_background(game):
    background = Background()
    game.add_obj(background)


def spawn_healthy(game, wid, hei, mask_type):
    '''
    Function creates a crewmate object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    healthy = Healthy(wid, hei, mask_type)
    game.add_obj(healthy)


def spawn_infected(game, wid, hei, mask_type):
    '''
    Function creates an imposter object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    infected = Infected(wid, hei, mask_type)
    game.add_obj(infected)


class Healthy:
    '''
    This class represents crewmates and what they are allowed
    to do and when they are allowed to do so.

    The constructor builds a crewmate; the crewmate is represented
    by a circle and the color white with the size of 20. The crewmate
    also spawns in random areas of the canvas.

    Methods:
        get_xy: gettors for the coordinates of the object
        get_radius: gettors for the radius of the object
        nearby: allows interactions between two objects that are nearby
        move: determines what direction the object will move across the campus
        edge: determines the direction of movement for the object based on
        which edge it's near.
        draw: draws the object onto the canvas
    '''

    def __init__(self, wid, hei, mask_type):
        self.x = random.randint(0, wid)
        self.y = random.randint(0, hei)
        self.diameter = 20
        self.number = random.randint(1, 8)
        self.mask = None
        self.mask_type = mask_type
        self.color = "white"
        if mask_type == "mask":
            self.mask = True
            self.mask_color = '#417CF9'
        elif mask_type == "none":
            self.mask = False

    def get_xy(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.diameter / 2

    def nearby(self, other, dist, game):
        pass

    def move(self, game):
        if self.number == 1:
            self.y -= 2
        elif self.number == 2:
            self.x += 2
            self.y -= 2
        elif self.number == 3:
            self.x += 2
        elif self.number == 4:
            self.x += 2
            self.y += 2
        elif self.number == 5:
            self.y += 2
        elif self.number == 6:
            self.x -= 2
            self.y += 2
        elif self.number == 7:
            self.x -= 2
        elif self.number == 8:
            self.x -= 2
            self.y -= 2

    def edge(self, dirr, position):
        if dirr == 'top':
            if position == 0:
                self.number = random.randint(3, 7)
        elif dirr == 'left':
            if position == 0:
                self.number = random.randint(1, 5)
        elif dirr == 'bottom':
            if position == 600:
                self.number = random.choice([1, 2, 3, 7, 8])
        elif dirr == 'right':
            if position == 600:
                self.number = random.choice([1, 5, 6, 7, 8])

    def draw(self, win):
        if self.mask == True:
            win.ellipse(self.x, self.y, self.diameter,
                        self.diameter, self.color)
            win.rectangle(self.x - 8, self.y, 16, 8, self.mask_color)
            win.ellipse(self.x - 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x + 5, self.y - 5, 3,
                        3, "black")
        else:
            win.ellipse(self.x, self.y, self.diameter,
                        self.diameter, self.color)
            win.ellipse(self.x - 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x + 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x, self.y + 4, 8,
                        2, "black")


class Infected:
    '''
    This class represents imposters and how they change and how they
    interact with the crewmates.

    The constructor builds an imposter; the imposter is represented
    by a circle and the color white with the size of 20. The imposteer
    also spawns in random areas of the canvas.

    Methods:
        get_xy: gettors for the coordinates of the object
        get_radius: gettors for the radius of the object
        nearby: allows interactions between two objects that are nearby
        move: determines what direction the object will move across the campus
        edge: determines the direction of movement for the object based on
        which edge it's near.
        draw: draws the object onto the canvas
    '''

    def __init__(self, wid, hei, mask_type):
        self.x = random.randint(0, wid)
        self.y = random.randint(0, hei)
        self.diameter = 20
        self.number = random.randint(1, 8)
        self.mask_type = mask_type
        self.mask = None
        self.color = "#FC3547"
        if mask_type == "mask":
            self.mask = True
            self.mask_color = '#417CF9'
        elif mask_type == "none":
            self.mask = False

    def get_xy(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.diameter / 2

    def nearby(self, other, dist, game):
        if dist <= 20:
            if isinstance(other, Healthy):
                if self.mask_type == "none" and other.mask_type == "none":
                    if random.randint(0, 100) < 95:
                        other.color = "#FD878E"
                    else:
                        pass
                elif self.mask_type == "none" and other.mask_type == "mask":
                    if random.randint(0, 100) < 70:
                        other.color = "#FD878E"
                    else:
                        pass
                elif self.mask_type == "mask" and other.mask_type == "none":
                    if random.randint(0, 100) < 5:
                        other.color = "#FD878E"
                    else:
                        pass
                elif self.mask_type == "mask" and other.mask_type == "mask":
                    if random.randint(0, 100) < 2:
                        other.color = "#FD878E"
                    else:
                        pass

    def move(self, game):
        if self.number == 1:
            self.y -= 2
        elif self.number == 2:
            self.x += 2
            self.y -= 2
        elif self.number == 3:
            self.x += 2
        elif self.number == 4:
            self.x += 2
            self.y += 2
        elif self.number == 5:
            self.y += 2
        elif self.number == 6:
            self.x -= 2
            self.y += 2
        elif self.number == 7:
            self.x -= 2
        elif self.number == 8:
            self.x -= 2
            self.y -= 2

    def edge(self, dirr, position):
        if dirr == 'top':
            if position == 0:
                self.number = random.randint(3, 7)
        elif dirr == 'left':
            if position == 0:
                self.number = random.randint(1, 5)
        elif dirr == 'bottom':
            if position == 600:
                self.number = random.choice([1, 2, 3, 7, 8])
        elif dirr == 'right':
            if position == 600:
                self.number = random.choice([1, 5, 6, 7, 8])

    def draw(self, win):
        if self.mask == True:
            win.ellipse(self.x, self.y, self.diameter,
                        self.diameter, self.color)

            win.ellipse(self.x - 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x + 5, self.y - 5, 3,
                        3, "black")
            # eyes
            win.rectangle(self.x - 8, self.y, 16, 8, self.mask_color)
            # mask
        else:
            win.ellipse(self.x, self.y, self.diameter,
                        self.diameter, self.color)
            win.ellipse(self.x - 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x + 5, self.y - 5, 3,
                        3, "black")
            win.ellipse(self.x, self.y + 4, 8,
                        2, "black")


class Background:
    def __init__(self) -> None:
        pass

    def get_xy(self):
        return (0, 0)

    def get_radius(self):
        return 0

    def nearby(self, other, dist, game):
        pass

    def move(self, game):
        pass

    def edge(self, dirr, position):
        pass

    def draw(self, win):
        # floor
        win.rectangle(0, 0, 600, 600, "#969595")
        # TV and stand
        win.rectangle(210, 20, 185, 18, "#713F1C")
        win.rectangle(225, 10, 150, 15, "black")
        # Sofa 1
        win.rectangle(80, 80, 70, 90, "#424241")
        win.rectangle(110, 98, 40, 54, "#4D4D4D")
        # Sofa 2
        win.rectangle(450, 80, 70, 90, "#424241")
        win.rectangle(450, 98, 40, 54, "#4D4D4D")
        # Sofa 3
        win.rectangle(210, 180, 185, 70, "#424241")
        win.rectangle(240, 180, 118, 50, "#4D4D4D")
        # Coffee table
        win.ellipse(300, 98, 140, 40, "#713F1C")
        win.text(300, 130, "Living Room")
        # Dining table
        win.ellipse(150, 450, 100, 180, "#713F1C")
        win.rectangle(50, 420, 30, 60, "#713F1C")
        win.rectangle(60, 420, 20, 40, "#969595")
        win.rectangle(220, 420, 30, 60, "#713F1C")
        win.rectangle(220, 420, 20, 40, "#969595")
        win.rectangle(135, 280, 30, 60, "#713F1C")
        win.rectangle(135, 280, 20, 40, "#969595")
        win.text(150, 570, "Dining Room")
        # Bar
        win.rectangle(590, 420, 10, 75, "#583116")
        win.rectangle(530, 405, 30, 105, "#583116")
        win.ellipse(515, 415, 22, 22, "#3A3A3A")
        win.ellipse(515, 450, 22, 22, "#3A3A3A")
        win.ellipse(515, 485, 22, 22, "#3A3A3A")
        win.text(465, 485, "Bar")


if __name__ == "__main__":
    main()
