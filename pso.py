import datetime

import numpy as np
from matplotlib import pyplot as plt

from particle import Particle

now_date = datetime.datetime.now().strftime("%m%d_%H:%M")
fig = plt.figure(figsize=(6, 8))
ax1 = fig.add_subplot(211)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax2 = fig.add_subplot(212)
ax2.set_title("Learning Curve of Global Best Fitness")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Fitness")
ax1.grid()
ax2.grid()
plt.tight_layout()


class PSO:

    def __init__(self, p_qty, iter_num):
        self.p_qty = p_qty
        self.iter_num = iter_num
        # ax.set_xlim(0, iter_num)
        self.p_shape = Particle.shape
        ax2.set_ylim(0, 1)
        self.p = [Particle(Particle.shape) for _ in range(p_qty)]
        self.prev_fitness = None

    def draw_learning_curve(self, i, save=False):
        if self.prev_fitness is not None:
            ax2.plot((i - 1, i), (self.prev_fitness, Particle.g_fitness[-1]), c='C0')
        self.prev_fitness = Particle.g_fitness[-1]
        if save:
            plt.savefig("learning_curve/" + now_date)

    def iterate(self, action, save=False):
        # epoch = 0
        for i in range(self.iter_num):
            ax1.set_title("iteration %d, best_fitness: %.4f" % (i, Particle.g_fitness[-1]))
            for p_index, p_ in enumerate(self.p):
                action(p_)
                p_.get_best(p_index)
                # p_.get_g_best()
                p_.update()

            # print("%s\n%s" %(g_best["fitness"], g_best["position"]))
            if save:
                np.save("training_record/" + now_date + ".npy", np.array(Particle.g_position))
            self.draw_learning_curve(i, save)

            plt.draw()
            plt.pause(0.3)
