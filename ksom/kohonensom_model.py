import numpy as np

from ksom.config import configurable
import matplotlib.pyplot as plt


def pairwise_dist(a, b, sqrt=True, p=2):
    """

    :param p:
    :param sqrt: if False return sum_of_square
    :param a: matrix with shape [batch_size, *shape_, dim]
    :param b: matrix with shape [*shape_, dim]
    :return: dist matrix with shape [batch_size, *shape_]
    """
    _d = a - b
    sum_of_square = np.sum(np.power(_d, p), axis=-1)
    if sqrt:
        return np.power(sum_of_square, 1 / p)
    else:
        return sum_of_square


class KohonenSOM:
    @configurable
    def __init__(self, w, h, d, init_lr=0.1, global_step=0, max_iter=100):
        """

        :param w: map width
        :param h: map height
        :param d: input vector dimension
        :param init_lr:
        :param global_step: always 0 except it loaded from a checkpoint
        :param max_iter:
        """
        # self._weight = np.random.uniform(low=-1, high=1, size=(h, w, d))
        self._weight = np.random.uniform(low=0, high=1, size=(h, w, d))
        self.init_lr = init_lr
        self.global_step = global_step
        self.max_iter = max_iter
        self.s0, self.lbd = self.calculate_initial_hparams(h, w)
        self.map_indices = np.stack(np.ones((h, w)).nonzero(), axis=-1)

    @classmethod
    def from_config(cls, cfg):
        return dict(
            w=cfg.SOM.W,
            h=cfg.SOM.H,
            d=cfg.SOM.D,
            init_lr=cfg.INIT_LR,
            global_step=0,
            max_iter=cfg.MAX_ITER)

    def calculate_initial_hparams(self, h, w):
        s0 = max(h, w) / 2
        lbd = self.max_iter / np.log(s0)
        return s0, lbd

    @property
    def weight(self):
        return self._weight

    @property
    def decay_factor(self):
        return np.exp(-self.global_step / self.lbd)

    def mapping_step(self, x: np.ndarray) -> np.ndarray:
        """
        The mapping step of SOM:
        quantize input vectors to the map codebook

        :param x: input vector matrix of size (batch_size, dim)
        :return: best matching units in shape (batch_size, 2)
        """
        x_ = np.expand_dims(x, axis=[1, 2])
        distances = pairwise_dist(x_, self._weight, sqrt=True)
        bmus = self.calculate_best_matching_units(distances)
        return bmus

    @staticmethod
    def calculate_best_matching_units(distances: np.ndarray) -> np.ndarray:
        """
        Find BMUs for with distance matrix
        :param distances matrix (batch, height, width)
        :return: BMUs (batch, 2)
        """

        batch_size = distances.shape[0]
        width = distances.shape[2]

        distances = distances.reshape((batch_size, -1))
        min_idxs = distances.argmin(-1)
        # Distances are flattened, so we need to transform 1d indices into 2d map locations
        bmus = np.stack([min_idxs // width, min_idxs % width], axis=1)
        return bmus

    def calculate_influence(self, bmus, sigma_t):
        """
        Calculate theta matrix at step t/self.global_step
        :param bmus:
        :param sigma_t: radius
        :return:
        """
        bmus_ = np.expand_dims(bmus, axis=1)
        distance_sum_of_square_map_node = pairwise_dist(bmus_, self.map_indices, sqrt=False)

        theta_t = np.exp(-distance_sum_of_square_map_node
                         / (2 * np.power(sigma_t, 2)))
        return theta_t

    def node_update_step(self, x, bmus):
        """
        The node updating step of SOM
        :param x: input vector matrix
        :param bmus:
        :return:
        """

        decay_factor = self.decay_factor

        # calculate radius
        sigma_t = self.s0 * decay_factor
        lr_t = self.init_lr * decay_factor

        # calclate influence
        _theta_shape = (x.shape[0], *self._weight.shape[:2], 1)
        theta_t = self.calculate_influence(bmus, sigma_t).reshape(_theta_shape)

        # update weight
        vw_diff_ = np.expand_dims(x, axis=[1, 2]) - self._weight
        self._weight += lr_t * np.average(theta_t * vw_diff_, axis=0)

    def run_step(self, x):
        """
        run single training step of som:
        1. mapping and calculate BMU
        2. update weights/codebook
        :param x: input data matrix (batch_size, dim)
        :return:
        """
        bmus = self.mapping_step(x)
        self.node_update_step(x=x, bmus=bmus)

    def visualise_weight(self):
        fig = plt.imshow(self._weight)
        plt.title(f"step: {self.global_step}")
        return fig
