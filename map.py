import numpy as np
import pygame as pg
import random as rand


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generate_maze(map_size):
    """
    Generates a maze using a randomized version of the Prim's algorithm

    :param map_size: map size
    :return: a tuple containing the starting position, starting rotation,
             the maze and maze colors
    """
    # Initialize our matrix
    maze = np.ones((map_size, map_size), dtype=int)

    startX = 1
    startY = 1
    endX = 1
    endY = 1

    # Create a random starting point and ending point to generate the maze
    while startX == endX or startY == endY or abs(startX - endX) < (
            map_size / 2) or abs(startY - endY) < (map_size / 2):
        rand.seed()
        startX = rand.randint(1, map_size - 2)
        startY = rand.randint(1, map_size - 2)
        endX = rand.randint(1, map_size - 2)
        endY = rand.randint(1, map_size - 2)

    # Rot in radians
    rot = 0
    currX = startX
    currY = startY

    options = []
    # Make sure the points around starting point are not walls
    maze[startX, startY] = 0

    # Start creating the maze halls
    while currY != endY or currX != endX:

        if currX > 1 and maze[currX - 1][currY] != 0:  # Left
            options.append(Point(currX - 1, currY))

        if currX + 2 < map_size and maze[currX + 1][currY] != 0:  # Right
            options.append(Point(currX + 1, currY))

        if currY + 2 < map_size and maze[currX][currY + 1] != 0:  # Up
            options.append(Point(currX, currY + 1))

        if currY > 1 and maze[currX][currY - 1] != 0:  # Down
            options.append(Point(currX, currY - 1))

        if len(options) == 0:  # No options means nowhere to go
            return None

        rand.seed()
        rand_opt = rand.randint(0, len(options) - 1)
        go_to_point = options.pop(rand_opt)

        while True:
            zeros = 0
            if maze[go_to_point.x - 1][go_to_point.y] == 0:
                zeros += 1
            if maze[go_to_point.x + 1][go_to_point.y] == 0:
                zeros += 1
            if maze[go_to_point.x][go_to_point.y + 1] == 0:
                zeros += 1
            if maze[go_to_point.x][go_to_point.y - 1] == 0:
                zeros += 1

            if zeros == 1:
                break
            if len(options) == 0:
                break

            rand_opt = rand.randint(0, len(options) - 1)
            go_to_point = options.pop(rand_opt)

        currX = go_to_point.x
        currY = go_to_point.y
        maze[currX][currY] = 0

    # Generate random colors for visualization
    mazec = np.random.uniform(0, 1, (map_size, map_size, 3))

    maze[startX + 1, startY] = 0
    maze[startX - 1, startY] = 0
    maze[startX, startY + 1] = 0
    maze[startX, startY - 1] = 0

    return startX, startY, rot, maze, mazec


def load_textures(halfvres):
    """
    Loads the textures and creates a masks list for the grime levels textures

    :param halfvres: half of the vertical resolution

    :return: a tuple containing the sky, floor, wall and grime textures
    """
    # Load the sky texture and scale it to the right size (skybox)
    sky = pg.image.load('assets/sky.jpg')
    sky = pg.surfarray.array3d(
        pg.transform.scale(sky, (360, halfvres * 2))) / 255

    # Load the floor texture
    floor = pg.surfarray.array3d(pg.image.load('assets/mirror.jpg')) / 255

    # Load the wall texture
    wall = pg.surfarray.array3d(pg.image.load('assets/wall.jpg')) / 255

    # Load the grime texture and create a mask out of it
    grime = pg.surfarray.array3d(pg.image.load('assets/dirty.jpg')) / 255
    grimes = np.array([np.clip(grime, 0, 1), np.clip(grime / 0.8, 0, 1),
                       np.clip(grime / 0.5, 0, 1)])

    return sky, floor, wall, grimes
