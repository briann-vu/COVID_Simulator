"""File: three_shapes_game.py

   Author: Russ Lewis
           (Updated by Brian Vu by adding draw_background(object), draw_person(object) 
           and display_stats(object) functions)

   Purpose: Defines the Game class, which provides the core mechanisms for the
            Three Shapes family of programs.
"""


import math        # for sqrt

from graphics import graphics


class Game:
    def __init__(self, title, frame_rate, wid, hei):
        """Constructor.  Initializes the game to have zero objets; call
           add_obj() to add objects to the system.

           Parameters: the width and height of the window
        """
        self._wid = wid
        self._hei = hei

        self._frame_rate = frame_rate

        self._win = graphics(wid, hei + 300, title)

        # this is a configuration setting - it changes how we calculate
        # the distance between objects in do_nearby_calls()
        self._account_for_radii_in_dist = False

        # the user must call add_obj() to add to this set
        self._active_objs = set()

        # see what remove_obj() and perform_moves() do, to understand this
        # variable.  UPDATE: Also, we're doing this for *adding*, otherwise
        # adding inside of move() will be impossible.
        self._pending_removes = set()
        self._pending_adds = set()

        # I plan to add a feature, where the user can mark the game as "over"
        self._game_over = False

    def config_set(self, param, val):
        """Function to set various config variables.  Right now, it only
           supports a single parameter; I might add more later.  Give the name
           of the parameter (as a string), then the value.

           Parmeters: config parameter to set, value

           Supported Config Options:
             "account_for_radii_in_dist" -> Boolean
        """
        if param == "account_for_radii_in_dist":
            self._account_for_radii_in_dist = val
        else:
            assert False   # unrecognized config parameter

    def set_game_over(self):
        self._game_over = True

    def is_over(self):
        return self._game_over

    def add_obj(self, new_obj):
        """Adds a new object to the game.  Can be called at any time, although
           if called in the middle of the nearby() or move() loops, may not be
           added to the ongoing loop.  The object must implement the standard
           methods required of any object: get_xy(), get_radius(), nearby(),
           move(), and draw().

           Parameters: the new object
        """
        assert new_obj not in self._active_objs
        assert new_obj not in self._pending_adds
        self._pending_adds.add(new_obj)

    # REMOVE LOGIC
    #
    # In the do_nearby_calls() and do_move_calls() methods, we loop over
    # lots of objects.  Inside those methods, the user may choose to call
    # remove_obj(); if they do, then ideally we would just remove it
    # immediately.  But we're in the middle of a loop: what if we call
    # nearby() or move() on a recently-removed object, or if we pass it as
    # a parameter to a nearby() call?
    #
    # One option would be to force the remove logic to exclude such objects
    # from the loop as it runs, but that's not the easiest thing in the
    # world.  Instead, remove_obj() will add an object to a set of "pending
    # removes" - none of these removals will take place until the game loop
    # calls execute_removes() - which happens *after* all of the nearby()
    # and move() calls have finished.
    #
    # When the user calls remove_obj(), it *MUST* be in the current set of
    # active objects.  It is *permissible* to call it multiple times in the
    # same game tick.

    def remove_obj(self, bad_obj):
        """Queues up an object to be removed from the game.  It is
           permissible to call this multiple times on the same object during
           one clock tick; all of the removals will take place at once,
           *after* all of the nearby() and move() calls have been completed,
           but *before* any draw() calls.  It is illegal to call this if the
           object is not currently in the game.

           Arguments: object to remove
        """
        assert bad_obj in self._active_objs
        self._pending_removes.add(bad_obj)

    def execute_removes(self):
        """Called by the game loop, after all of the nearby() and move() calls
           have completed; performs all of the pending remove operations.

           Arguments: None
        """
        self._active_objs -= self._pending_removes
        self._pending_removes = set()

        self._active_objs.update(self._pending_adds)
        self._pending_adds = set()

    def do_nearby_calls(self):
        """Figures out how close each object is to every other, sorts them by
           distance, and then performs all of the nearby() calls on the object
           pairs.  Makes all of the calls for a given "left-hand" object as a
           block; if the user returns False from any call, we terminate that
           inner loop, and then start delivering values for another left-hand
           value.

           Parameters: none
        """

        positions = []
        for o in self._active_objs:
            x, y = o.get_xy()
            positions.append((o, x, y))

        # Note that we're doing a 2D loop, but because we're only looking for
        # one version of each pair (not the reversed), notice that we do
        # something funny with the lower bound of the inner loop variable.
        distances = []
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                o1, x1, y1 = positions[i]
                o2, x2, y2 = positions[j]

                dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)

                if self._account_for_radii_in_dist:
                    dist -= o1.get_radius()
                    dist -= o2.get_radius()

                # we add two records to the 'distances' array, so that we can
                # simply *sort* that list at the end.  Note that the way that
                # we arrange this, we will organize first by the left-hand
                # object, then by the distance, and then by the right-hand
                # object (the last of which will rarely be an issue)
                #
                # UPDATE: Note that I wanted to use object references here -
                #         but then I realized that we couldn't sort by those!
                #         so I need to use the indices into the positions[]
                #         array instead.
                distances.append((i, dist, j))
                distances.append((j, dist, i))

        # now that we're done *creating* the distances, we can sort all of
        # them.
        distances.sort()

        # there should be exactly n(n-1) elements in the array - since every
        # object in the game will be paired with n-1 others.
        n = len(positions)
        assert len(distances) == n*(n-1)

        # this loop is weird - but we have n different objects, each of which
        # has n-1 partners.  So I will implement each inner loop as looping
        # over a slice of the distances array.
        for i in range(n):
            for entry in distances[(n-1)*i: (n-1)*(i+1)]:
                k1, dist, k2 = entry
                assert k1 == i

                left = positions[k1][0]
                right = positions[k2][0]

                # if the user returns False, then we will terminate this as a
                # left-hand element.
                if not left.nearby(right, dist, self):
                    break

    def do_move_calls(self):
        """Calls move() on every object in the game"""
        for o in self._active_objs:
            o.move(self)

    def do_edge_calls(self):
        """Finds any objects that are close to any edge - defined as within the
           radius of it (that is, touching or overlapping) - and calls edge()
           on them.

           Parameters: none
        """

        for o in self._active_objs:
            x, y = o.get_xy()
            rad = o.get_radius()

            if x < rad:
                o.edge("left", 0)
            if y < rad:
                o.edge("top", 0)

            if x+rad >= self._wid:
                o.edge("right", self._wid)
            if y+rad >= self._hei:
                o.edge("bottom", self._hei)

    def draw(self, population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks, og_infected_pop, cur_infected, newly_infected, infected_mask_type):
        """Calls draw() on every object in the game.  Also does the rest of the
           misc calls necessary to animate the window.
        """

        # if the window has been destroyed, then we will throw an exception when
        # we run clear() below.  So check for this condition first!
        if self._win.is_killed:
            self._game_over = True
            return

        self._win.clear()

        draw_background(self)

        # make another function?
        display_stats(self, population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks,
                      og_infected_pop, cur_infected, newly_infected, infected_mask_type)

        for o in self._active_objs:
            o.draw(self._win)

        self._win.update_frame(self._frame_rate)


def display_stats(object, population, cur_healthy, cur_healthy_masks, cur_healthy_no_masks,
                  og_infected_pop, infected_mask_type, cur_infected, newly_infected):
    """
    Draws the stats portion to display stats like; Total Number of People, Current 
    Number of Healthy people, Original Number of Healthy Mask Wearers, Original 
    Number of Healthy Non Mask Wearers, Number of Contagious People, mask status of 
    those infected, Current Number of Infected People and Number of Newly Infected People

    Takes in an object (usually a game object) to draw on its window/gui object
    """
    object._win.rectangle(0, 600, 600, 900, "#e6e047")
    object._win.line(0, 600, 600, 600)
    object._win.text(50, 615, "Statistics/Information:", "black", 25)
    object._win.text(50, 650, "Total Number of People: " + str(population))
    object._win.text(50, 670, "Current Number of Healthy people: " +
                     str(cur_healthy), "#181563")
    object._win.text(
        50, 690, "Original Number of Healthy Mask Wearers: " + str(cur_healthy_masks), "#181563")
    draw_person(object, 413, 698, True, "white")
    object._win.text(50, 710, "Original Number of Healthy Non Mask Wearers: " +
                     str(cur_healthy_no_masks), "#181563")
    draw_person(object, 450, 718, False, "white")
    object._win.text(50, 730, "Number of Contagious People : " +
                     str(og_infected_pop), "#66020a")
    draw_person(object, 322, 738, True, "#FC3547")
    draw_person(object, 347, 738, False, "#FC3547")
    object._win.text(
        50, 750, "Are the Contagious People Wearing Masks?: " + str(infected_mask_type), "#66020a")
    object._win.text(50, 770, "Current Number of Infected People : " +
                     str(cur_infected), "#66020a")
    object._win.text(
        50, 790, "Number of Newly Infected People : " + str(newly_infected), "#66020a")
    draw_person(object, 350, 798, True, "#FD878E")
    draw_person(object, 375, 798, False, "#FD878E")


def draw_person(object, x, y, mask, color):
    """
    Draws a "person" to represent the healthy and infected objects on the stats section

    Takes in an object (usually a game object) to draw on its window/gui object
    """
    if mask == True:
        object._win.ellipse(x, y, 20,
                            20, "white")
        object._win.rectangle(x - 8, y, 16, 8, "#417CF9")
        object._win.ellipse(x - 5, y - 5, 3,
                            3, "black")
        object._win.ellipse(x + 5, y - 5, 3,
                            3, "black")
    else:
        object._win.ellipse(x, y, 20,
                            20, color)
        object._win.ellipse(x - 5, y - 5, 3,
                            3, "black")
        object._win.ellipse(x + 5, y - 5, 3,
                            3, "black")
        object._win.ellipse(x, y + 4, 8,
                            2, "black")


def draw_background(object):
    """
    Draws the background for the covidSim.py program using multiple
    shapes. Background is supposed to look like a house for a party 
    with a living room, dining table, and bar area.

    Takes in an object (usually a game object) to draw on its window/gui object
    """
    # floor
    object._win.rectangle(0, 0, 600, 600, "#969595")
    # TV and stand
    object._win.rectangle(210, 20, 185, 18, "#713F1C")
    object._win.rectangle(225, 10, 150, 15, "black")
    # Sofa 1
    object._win.rectangle(80, 80, 70, 90, "#424241")
    object._win.rectangle(110, 98, 40, 54, "#4D4D4D")
    # Sofa 2
    object._win.rectangle(450, 80, 70, 90, "#424241")
    object._win.rectangle(450, 98, 40, 54, "#4D4D4D")
    # Sofa 3
    object._win.rectangle(210, 180, 185, 70, "#424241")
    object._win.rectangle(240, 180, 118, 50, "#4D4D4D")
    # Coffee table
    object._win.ellipse(300, 98, 140, 40, "#713F1C")
    object._win.text(300, 130, "Living Room")
    # Dining table
    object._win.ellipse(150, 450, 100, 180, "#713F1C")
    object._win.rectangle(50, 420, 30, 60, "#713F1C")
    object._win.rectangle(60, 420, 20, 40, "#969595")
    object._win.rectangle(220, 420, 30, 60, "#713F1C")
    object._win.rectangle(220, 420, 20, 40, "#969595")
    object._win.rectangle(135, 280, 30, 60, "#713F1C")
    object._win.rectangle(135, 280, 20, 40, "#969595")
    object._win.text(150, 570, "Dining Room")
    # Bar
    object._win.rectangle(590, 420, 10, 75, "#583116")
    object._win.rectangle(530, 405, 30, 105, "#583116")
    object._win.ellipse(515, 415, 22, 22, "#3A3A3A")
    object._win.ellipse(515, 450, 22, 22, "#3A3A3A")
    object._win.ellipse(515, 485, 22, 22, "#3A3A3A")
    object._win.text(465, 485, "Bar")
