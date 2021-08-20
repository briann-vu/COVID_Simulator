'''
Brian Vu
covidSim.py

Description: soon to come

Goals: add picture of each type of person next to stat

Issues: fix string input on int(input())
infinite number of infect actions (add a tagged field)
fix rest of text
'''

import random
from three_shapes_game import *


def main():

    global population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks, infected_pop, cur_infected, newly_infected, answer

    print("Welcome to the COVID-19 Simulator")
    print("Please fill out this form:")
    print()

    population = int(input("Population size (50 looks fine): "))
    infected_pop = int(input("Number of people already carrying COVID-19: "))
    population -= infected_pop

    infected_mask_type = None
    while True:
        answer = input(
            "Are these infected people wearing masks? (yes or no): ")
        if answer.upper() == "YES":
            infected_mask_type = "mask"
            break
        elif answer.upper() == "NO":
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

    dummy = input("Press 'ENTER' to continue")

    wid = 600
    hei = 600

    # This creates the Game object. The first param is the window name;
    # the second is the framerate you want (20 frames per second, in this
    # example); the last is the window / game space size.
    game = Game("COVID-19 Simulator", 40, wid, hei)

    # This affects how the distance calculation in the "nearby" calls
    # works; the default is to measure center-to-center. But if anybody
    # wants to measure edge-to-edge, they can turn on this feature.
    # game.config_set("account_for_radii_in_dist", True)

    i = 0
    while i < healthy_masks:  # fix spawn ammount
        spawn_healthy(game, wid, hei, "mask")
        i += 1

    l = 0
    while l < healthy_no_masks:
        spawn_healthy(game, wid, hei, "none")
        l += 1

    j = 0
    while j < infected_pop:
        spawn_infected(game, wid, hei, infected_mask_type)
        j += 1

    cur_healthy = healthy_no_masks + healthy_masks
    cur_infected = infected_pop
    newly_infected = 0
    #global population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks, infected_pop, cur_infected, newly_infected, answer
    # population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks, og_infected_pop, cur_infected, newly_infected, infected_mask_type):

    # game loop. Runs forever, unless the game ends.
    count = 0
    while not game.is_over():
        game.do_nearby_calls()
        game.do_move_calls()
        game.do_edge_calls()
        game.execute_removes()
        game.draw(population + infected_pop, cur_healthy, healthy_masks,
                  healthy_no_masks, infected_pop, answer, cur_infected, newly_infected)


def spawn_healthy(game, wid, hei, mask_type):
    '''
    Function creates a healthy object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    healthy = Healthy(wid, hei, mask_type)
    game.add_obj(healthy)


def spawn_infected(game, wid, hei, mask_type):
    '''
    Function creates an infected object and adds it to the
    game object

    game: game object
    wid: int representing the width of the canvas
    hei: int representing the height of the canvas
    '''
    infected = Infected(wid, hei, mask_type)
    game.add_obj(infected)


class Healthy:
    '''
    This class represents healthy people.

    The constructor builds a crewmate; the healthy person is represented
    by a circle and the color white with the size of 20. The person
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
        self.tagged = False
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
    This class represents infected people and how they
    interact with and affect the healthy people.

    The constructor builds an infected person; the person is represented
    by a circle and the color red with the size of 20. The person
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
        new_infection = False
        if dist <= 20:
            if isinstance(other, Healthy) and other.tagged == False:
                if self.mask_type == "none" and other.mask_type == "none":
                    if random.randint(0, 100) < 95:
                        other.color = "#FD878E"
                        other.tagged = True
                        new_infection = True
                    else:
                        pass
                elif self.mask_type == "none" and other.mask_type == "mask":
                    if random.randint(0, 100) < 70:
                        other.color = "#FD878E"
                        other.tagged = True
                        new_infection = True
                    else:
                        pass
                elif self.mask_type == "mask" and other.mask_type == "none":
                    if random.randint(0, 100) < 5:
                        other.color = "#FD878E"
                        other.tagged = True
                        new_infection = True
                    else:
                        pass
                elif self.mask_type == "mask" and other.mask_type == "mask":
                    if random.randint(0, 100) < 2:
                        other.color = "#FD878E"
                        other.tagged = True
                        new_infection = True
                    else:
                        pass
        if new_infection:
            global cur_healthy, cur_infected, newly_infected
            cur_healthy -= 1
            cur_infected += 1
            newly_infected += 1

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


if __name__ == "__main__":
    main()
