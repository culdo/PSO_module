import numpy as np

inertia_weight = 0.7298
const_vp = 1.49618
const_vg = 1.49618


class Particle:
    shape = (2,)
    init_pos = None
    init_vel = None
    # now_date = datetime.datetime.now().strftime("%m%d_%H:%M")
    g_position = [np.zeros(shape, float)]
    g_fitness = [1, 0]

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
        gb = Particle.g_position[-1]

        self.velocity = (inertia_weight * vel) + \
                        (rand1 * const_vp * (pb - pos)) + \
                        (rand2 * const_vg * (gb - pos))
        self.position = self.position + self.velocity

    def get_fitness(self, callback):
        self.fitness = callback(self.position)

    def get_best(self, p_index):
        # get personal best
        if self.fitness > self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = self.position
            print("P[%d]_best updated!!!" % p_index)
              # get global worst
            if self.fitness < Particle.g_fitness[0]:
                Particle.g_fitness[0] = self.fitness
                Particle.g_position[0] = self.position
        else:
            print("P[%d]_best is still %.2f" % (p_index, self.best_fitness))

        # get global best
        if self.fitness > Particle.g_fitness[-1]:
            Particle.g_fitness.append(self.fitness)
            Particle.g_position.append(self.position)
            print("\nUpdated Gb_fitness: %.2f!!!" % self.fitness)
        else:
            Particle.g_fitness.append(Particle.g_fitness[-1])
            print("Gb_fitness is still: %.2f" % Particle.g_fitness[-1])

