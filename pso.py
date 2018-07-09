import datetime
import numpy as np
from matplotlib import pyplot as plt

now_date = datetime.datetime.now().strftime("%m%d_%H:%M")

p_qty = None
iter_num = None

inertia_weight = 0.9
const_vp = 2
const_vg = 2
p = []

fig = plt.figure(1, figsize=(12, 5))
ax = fig.add_subplot(1, 1, 1)


class Particle:
    shape = None
    init_pos = None
    init_vel = None
    # now_date = datetime.datetime.now().strftime("%m%d_%H:%M")

    def __init__(self, shape):
        Particle.shape = shape
        self.position = Particle.init_pos
        self.best_position = None
        self.velocity = Particle.init_vel
        self.fitness = None
        self.best_fitness = 0

    def update(self):
        rand1 = np.random.rand()
        rand2 = np.random.rand()
        pos = self.position
        vel = self.velocity
        pb = self.best_position
        gb = Gbest.position[-1]

        self.velocity = (inertia_weight * vel) + \
                 (rand1 * const_vp * (pb - pos)) + \
                 (rand2 * const_vg * (gb - pos))
        self.position = self.position + self.velocity

    def get_fitness(self, callback):
        self.fitness = callback()

    def get_best(self, p_index):
        # get personal best
        if self.fitness > self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = self.position
            print("P[%d]_best updated!!!" % p_index)
            # get global worst
            if self.fitness < Gbest.fitness[0]:
                Gbest.fitness[0] = self.fitness
                Gbest.position[0] = self.position
        else:
            print("P[%d]_best is still %.2f" % (p_index, self.best_fitness))

        # get global best
        if self.fitness > Gbest.fitness[-1]:
            Gbest.fitness.append(self.fitness)
            Gbest.position.append(self.position)
            print("\nUpdated Gb_fitness: %.2f!!!" % self.fitness)
        else:
            Gbest.fitness.append(Gbest.fitness[-1])
            print("Gb_fitness is still: %.2f" % Gbest.fitness[-1])


class Gbest:
    position = [np.zeros(Particle.shape, float)]
    fitness = [1, 0]


def spawn():
    # ax.set_xlim(0, iter_num)
    ax.set_ylim(0, 1)
    plt.ion()
    p[:] = [Particle(Particle.shape) for _ in range(p_qty)]
    return p


def draw_learning_curve(save=True):
    plt.figure(1)
    ax.plot(Gbest.fitness[2::p_qty], c='C0')
    if save:
        plt.savefig("learning_curve/"+now_date)
    plt.draw()
    plt.pause(0.3)


def iternum(action, fitness_fun=None, save=True):
    # epoch = 0
    for i in range(iter_num):
        print("--------\nIter %d\n--------" % i)
        for p_index, p_ in enumerate(p):

            action(p_)
            if fitness_fun is not None:
                p_.get_fitness(fitness_fun)
            print("p[%d]_fitness: %.2f" % (p_index, p_.fitness))
            p_.get_best(p_index)
            # p_.get_g_best()
            p_.update()

        # print("%s\n%s" %(g_best["fitness"], g_best["position"]))
        if save:
            np.save("training_record/"+now_date+".npy", np.array(Gbest.position))
        draw_learning_curve(save)



