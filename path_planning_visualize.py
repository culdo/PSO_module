import numpy as np
import matplotlib.pyplot as plt

from particle import Particle
from pso import PSO, ax1

goal = [0.8, 0.8]

pso = PSO(p_qty=3, iter_num=200)
x_y_lim = (0, 1), (0, 1)

# Initialize the particles in random positions and with
for p_init in pso.p:
    p_init.position = np.random.uniform(0, 1, pso.p_shape)
    # p_init.velocity = np.zeros(Particle.shape)
    p_init.velocity = np.random.uniform(-1, 1, pso.p_shape) * 0.6

# Create new Figure and an Axes which fills it.
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)

scat = ax1.scatter([], [])
g_best = ax1.scatter([], [], s=200, marker='+', c='green')
ax1.scatter(*goal, s=200, marker='*', c='xkcd:light orange')


def action(p_):
    _shift2limit(p_)
    # Constrict particles according /
    # Poli, R., Kennedy, J., & Blackwell, T. (2007) [sec 2.4]

    points = [p_r.position for p_r in pso.p]
    scat.set_offsets(points)
    g_best.set_offsets(Particle.g_position[-1])
    p_.get_fitness(fitness_fun)


def fitness_fun(pos):
    return 1 / ((((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5) + 1)


def _shift2limit(p_):
    for i, v in enumerate(p_.position):
        if v > x_y_lim[i][1]:
            p_.position[i] = x_y_lim[i][1]
        elif v < x_y_lim[i][0]:
            p_.position[i] = x_y_lim[i][0]


pso.iterate(action)
