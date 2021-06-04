import glob

import imageio
import os
import matplotlib.pyplot as plt


class Hook:

    def before_step(self, model):
        pass

    def after_step(self, model):
        pass

    def before_train(self, model):
        pass

    def after_train(self, model):
        pass


class VisualLogHook(Hook):
    def __init__(self, log_dir):
        self.vlog_dir = os.path.join(log_dir, 'vlog')
        self.weight_images_dir = os.path.join(self.vlog_dir, 'images')
        os.makedirs(self.weight_images_dir, exist_ok=True)

    def before_step(self, model):
        fig = model.visualise_weight()
        fname = f'{str(model.global_step).zfill(6)}.png'
        plt.savefig(os.path.join(self.weight_images_dir, fname))

    def after_train(self, model):
        self.before_step(model)
        filenames = list(sorted(glob.glob(os.path.join(self.weight_images_dir, "*.png"))))
        v_log_path = os.path.join(self.vlog_dir, 'vlog.gif')
        with imageio.get_writer(v_log_path, mode='I', duration=0.5) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

