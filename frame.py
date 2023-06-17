from numba import njit
import numpy as np


@njit(cache=True)
def new_frame(posx, posy, rot, frame, sky, floor, wall, hres, halfvres,
              pixel_fov, maze, map_size, mapc, grimes, grime_map):
    """
    Compute a new frame
    :param posx: x camera position
    :param posy: y camera position
    :param rot: camera rotation
    :param frame: frame to draw on
    :param sky: sky texture
    :param floor: floor texture
    :param hres: horizontal resolution
    :param halfvres: half vertical resolution
    :param pixel_fov: scaling factor (fov in pixels)
    :param maze: maze map
    :param map_size: size of the map
    :param wall: wall texture
    :param mapc: map color
    :param grimes: grime textures
    :param grime_map: grime map
    
    :return: drawn frame
    """
    # Iterate through each column
    for i in range(hres):
        # Calculate the angle of the ray
        rot_i = rot + np.deg2rad(i / pixel_fov - 30)

        # Calculate the sin and cos of the angle
        sin, cos = np.sin(rot_i), np.cos(rot_i)

        # The cos2 is for the fish eye effect
        cos2 = np.cos(np.deg2rad(i / pixel_fov - 30))

        # Draw the sky on all the columns
        frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:]

        # Declare the variables for the ray casting
        x, y = posx, posy

        # Calculate the position of the first wall the ray hits
        while maze[int(x) % (map_size - 1)][int(y) % (map_size - 1)] == 0:
            x, y = x + 0.01 * cos, y + 0.01 * sin

        # Calculate the distance to the wall
        wall_dist = abs((x - posx) / cos)

        # Calculate the height of the wall based on the distance
        # Check if the distance is 0 to avoid division by 0
        if wall_dist * cos2 == 0:
            wall_height = int(halfvres / (wall_dist * cos2 + 0.001))
        else:
            wall_height = int(halfvres / (wall_dist * cos2))

        # Calculate the position of the wall texture on the screen
        xx_wall = int(x * 3 % 1 * (floor.shape[0] - 1))
        if x % 1 < 0.02 or x % 1 > 0.98:
            xx_wall = int(y * 3 % 1 * (floor.shape[0] - 1))

        yy_wall = np.linspace(0, 3, wall_height * 2) \
                  * (wall.shape[0] - 1) % (wall.shape[0] - 1)

        # Get the dirt level of the wall
        grime_level = grime_map[int(x) % (map_size - 1)][int(y) % (map_size - 1)]
        grime = grimes[grime_level]

        if grime_level < 3:
            # Calculate the position of the grime mask on the wall
            xx_grime = int(x * 3 % 1 * (grime.shape[0] - 1))
            if x % 1 < 0.02 or x % 1 > 0.98:
                xx_grime = int(y * 2 % 1 * (grime.shape[0] - 1))

            yy_grime = np.linspace(0, 1, wall_height * 2) * \
                         (grime.shape[0] - 1) % (grime.shape[0] - 1)

        # Calculate the shade of the floor
        shade = 0.3 + 0.7 * (wall_height / halfvres)
        if shade > 1:
            shade = 1

        # Calculate the shade of the wall
        wall_shade = 0
        if maze[int(x - 0.01) % (map_size - 1)][int(y - 0.01) % (map_size - 1)]:
            shade *= 0.5

        elif maze[int(x - 0.33) % (map_size - 1)][int(y - 0.33) % (map_size - 1)]:
            wall_shade = 1

        # Calculate the color of the wall
        wall_color = shade * mapc[int(x) % (map_size - 1)][int(y) % (map_size - 1)]

        # Draw the walls, shades included, on the screen
        for k in range(wall_height * 2):
            # Check if the wall is in the screen
            if 0 <= halfvres - wall_height + k < 2 * halfvres:
                # Check if the wall is in the shade
                if wall_shade == 1 and \
                        k / (2 * wall_height) < xx_wall / wall.shape[0]:
                    wall_color, wall_shade = 0.5 * wall_color, 0

                # Draw the wall/grime texture on the wall
                if grime_level < 3:
                    frame[i][halfvres - wall_height + k] = \
                        np.clip(wall_color * wall[xx_wall][int(yy_wall[k])] - 1 + grime[xx_grime][int(yy_grime[k])], 0, 1)
                else:
                    frame[i][halfvres - wall_height + k] = \
                        wall_color * wall[xx_wall][int(yy_wall[k])]

                # Draw the wall/grime texture reflection on the floor
                if halfvres + 3 * wall_height - k < halfvres * 2:
                    if grime_level < 3:
                        frame[i][halfvres + 3 * wall_height - k] = \
                            np.clip(wall_color * wall[xx_wall][int(yy_wall[k])] - 1 + grime[xx_grime][int(yy_grime[k])], 0, 1)
                    else:
                        frame[i][halfvres + 3 * wall_height - k] = \
                            wall_color * wall[xx_wall][int(yy_wall[k])]

        for j in range(halfvres - wall_height):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx_floor = int(x * 2 % 1 * floor.shape[0])
            yy_floor = int(y * 2 % 1 * floor.shape[1])
            
            # Calculate the shade of the floor depending on the distance
            # The further closer the point is from the middle of the screen,
            # The further it is from the player if no wall is encountered
            shade = 0.2 + 0.8 * (1 - j / halfvres)

            # Check if there is a wall in the diagonal of the floor point
            shade_cond1 = maze[int(x - 0.33) % (map_size - 1)][int(y - 0.33) % (map_size - 1)]
            # Check if there is a wall in the horizontal y of the floor point
            shade_cond2 = maze[int(x) % (map_size - 1)][int(y - 0.33) % (map_size - 1)] and x % 1 > y % 1
            # Check if there is a wall in the horizontal x of the floor point
            shade_cond3 = maze[int(x - 0.33) % (map_size - 1)][int(y) % (map_size - 1)] and y % 1 > x % 1

            # Apply the shade to the floor
            if shade_cond1 or shade_cond2 or shade_cond3:
                shade *= 0.5

            # Mix the texture of the floor with the texture of the sky to
            # produce a reflection effect
            frame[i][halfvres * 2 - j - 1] = \
                shade * (floor[xx_floor][yy_floor] +
                         frame[i][halfvres * 2 - j - 1]) / 2

    return frame


@njit()
def wash(grime_map, posx, posy, rot, map_size, maze, pixel_fov):
    """
    Washes the grime off the walls the player is looking at

    :param grime_map: grime map
    :param posx: camera x position
    :param posy: camera y position
    :param rot: camera rotation
    :param map_size: size of the map
    :param maze: maze map
    :param pixel_fov: field of view in pixels

    :return: updated grime map
    """
    x, y = posx, posy
    center = rot + np.deg2rad(100 / pixel_fov - 30)
    cos, sin = np.cos(center), np.sin(center)
    
    # Calculate the position of the first wall the ray hits
    # (center of the screen ray)
    while maze[int(x) % (map_size - 1)][int(y) % (map_size - 1)] == 0:
        x, y = x + 0.01 * cos, y + 0.01 * sin

    if grime_map[int(x) % (map_size - 1)][int(y) % (map_size - 1)] < 3:
        grime_map[int(x) % (map_size - 1)][int(y) % (map_size - 1)] += 1

    return grime_map
