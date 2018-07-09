import numpy as np
import matplotlib.pyplot as plt
import pso
from pso import Particle

goal = [0.8, 0.8]

pso.iter_num = 200
pso.p_qty = 3
Particle.shape = (2,)
p = pso.spawn()
x_y_lim = (0, 1), (0, 1)

# Initialize the particles in random positions and with
for p_init in p:
    p_init.position = np.random.uniform(0, 1, Particle.shape)
    # p_init.velocity = np.zeros(Particle.shape)
    p_init.velocity = np.random.uniform(-1, 1, Particle.shape) * 0.6

# Create new Figure and an Axes which fills it.
fig = plt.figure(2)
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

scat = ax.scatter([], [])
ax.scatter(*goal, s=200, marker='*', c='xkcd:light orange')


def action(p_):
    shift2limit(p_)                       # Constrict particles according Poli, R., Kennedy, J., & Blackwell, T. (2007) [sec 2.4]

    plt.figure(2)
    points = [p_r.position for p_r in p]
    scat.set_offsets(points)
    plt.draw()
    p_.get_fitness(fitness_fun)


def fitness_fun(pos):
    return 1 / ((((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) ** 0.5) + 1)


def shift2limit(p_):
    for i, v in enumerate(p_.position):
        if v > x_y_lim[i][1]:
            p_.position[i] = x_y_lim[i][1]
        elif v < x_y_lim[i][0]:
            p_.position[i] = x_y_lim[i][0]


plt.figure(2)
plt.ion()

pso.iterate(action)
