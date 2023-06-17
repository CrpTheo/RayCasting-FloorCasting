import numpy as np
import pygame as pg


def move(posx, posy, rot, maze, et):
    """
    Move the player based on the pressed keys and mouse movement
    
    :param posx: camera x position
    :param posy: camera y position
    :param rot: camera rotation angle
    :param maze: map of the maze
    :param et: elapsed time

    :return: updated position and rotation angle
    """
    # Declare the variables to be used
    x, y, diag = posx, posy, rot

    # Get the pressed keys
    pressed_keys = pg.key.get_pressed()

    # Get the mouse movement since last function call
    p_mouse = pg.mouse.get_rel()

    # Update the rotation angle based on mouse movement
    # Clip the value to avoid too fast rotation (max 0.2 rad/frame)
    rot = rot + np.clip((p_mouse[0]) / 200, -0.2, .2)

    # Update the position based on the pressed keys
    if pressed_keys[pg.K_UP] or pressed_keys[pg.K_z]:
        x, y, diag = x + et * np.cos(rot), y + et * np.sin(rot), 1

    elif pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_s]:
        x, y, diag = x - et * np.cos(rot), y - et * np.sin(rot), 1

    if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_q]:
        et = et / (diag + 1)
        x, y = x + et * np.sin(rot), y - et * np.cos(rot)

    elif pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_d]:
        et = et / (diag + 1)
        x, y = x - et * np.sin(rot), y + et * np.cos(rot)

    if x > 24.5 or x < 0.5 or y > 24.5 or y < 0.5:
        x, y = posx, posy

    # Check if the new position is valid and update the position if it is
    if not (maze[int(x - 0.2)][int(y)] or maze[int(x + 0.2)][int(y)] or
            maze[int(x)][int(y - 0.2)] or maze[int(x)][int(y + 0.2)]):
        posx, posy = x, y

    elif not (maze[int(posx - 0.2)][int(y)] or maze[int(posx + 0.2)][int(y)] or
              maze[int(posx)][int(y - 0.2)] or maze[int(posx)][int(y + 0.2)]):
        posy = y

    elif not (maze[int(x - 0.2)][int(posy)] or maze[int(x + 0.2)][int(posy)] or
              maze[int(x)][int(posy - 0.2)] or maze[int(x)][int(posy + 0.2)]):
        posx = x

    return posx, posy, rot
