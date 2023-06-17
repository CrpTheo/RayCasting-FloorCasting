import numpy as np
import pygame as pg

from frame import new_frame, wash
from map import generate_maze, load_textures
from movement import move


def main():
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((800, 600))
    running = True
    clock = pg.time.Clock()
    pg.mouse.set_visible(False)

    # Horizontal resolution
    hres = 200

    # Vertical resolution/2
    halfvres = 150

    # Scaling factor (60° fov)
    pixel_fov = hres / 60

    map_size = 25

    # Generate the maze
    maze = generate_maze(map_size)
    while maze is None:
        maze = generate_maze(map_size)

    posx, posy, rot, maph, mapc = maze

    # Generate the grime map (0 no grime, 1,2 grime levels)
    grime_map = np.random.randint(5, size=(map_size, map_size))

    # Initialize the frame
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))

    # Load the textures
    sky, floor, wall, grimes = load_textures(halfvres)

    pg.event.set_grab(True)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            if pg.mouse.get_pressed()[0]:
                grime_map = wash(grime_map, posx, posy, rot, map_size, maph,
                                 pixel_fov)

        # Update the frame
        frame = new_frame(posx, posy, rot, frame, sky, floor, wall, hres, halfvres,
                          pixel_fov, maph, map_size, mapc, grimes,
                          grime_map)

        # Update the screen surface
        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (800, 600))

        # Display the FPS and the title
        fps = int(clock.get_fps())
        pg.display.set_caption("ISIM Floor and RayCasting - FPS: " + str(fps))

        # Display the frame
        screen.blit(surf, (0, 0))
        pg.display.update()

        # Update player position and rotation
        posx, posy, rot = move(posx, posy, rot, maph, clock.tick() / 500)


if __name__ == '__main__':
    main()
    pg.quit()
