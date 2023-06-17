import pygame as pg
import numpy as np
from matplotlib import pyplot as plt

grime = pg.surfarray.array3d(pg.image.load('grime.jpg')) / 255

grime = np.clip(grime, 0, 1)

plt.show(grime, cmap='gray')