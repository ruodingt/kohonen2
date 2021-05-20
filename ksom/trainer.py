import time

from ksom.dataset import Dataset
from ksom.default_setup import default_setup
from ksom.hooks import VisualLogHook
from ksom.kohonensom_model import KohonenSOM
from ksom.logger import setup_logger


class Trainer:
    def __init__(self, cfg):
        self.checkpoint_dir = None
        self.max_iter = cfg.MAX_ITER
        self.start_iter = 0
        self.model = KohonenSOM(cfg)
        self.data_iter = iter(Dataset(length=cfg.DATA.LENGTH, d=cfg.DATA.DIM, batch_size=cfg.DATA.BATCH_SIZE))
        self.callback_period = cfg.CALLBACK_PERIOD
        self.video_buffer = []
        self.log_dir = cfg.LOG_DIR
        self.hooks = [VisualLogHook(cfg.LOG_DIR)]
        self.logger = setup_logger(name=f"KohonenSOM.{cfg.EXP_NAME}")

    def after_step(self):
        for h in self.hooks:
            if self.model.global_step % self.callback_period == 0:
                h.after_step(self.model)
                self.logger.info(f"global_step: {self.model.global_step}/{self.max_iter}")

    def before_step(self):
        for h in self.hooks:
            if self.model.global_step % self.callback_period == 0:
                h.before_step(self.model)

    def after_train(self):
        for h in self.hooks:
            h.after_train(self.model)

    def train(self):
        t0 = time.perf_counter()
        for self.model.global_step in range(self.start_iter, self.max_iter):
            self.before_step()
            self.run_step()
            self.after_step()
        t1 = time.perf_counter()
        self.logger.info(f"Training completed within: {t1-t0}s")
        self.after_train()

    def run_step(self):
        batched_data = next(self.data_iter)
        self.model.run_step(batched_data)


if __name__ == '__main__':
    cfg_ = default_setup(config_file="som://configs/exp1.yaml")
    trainer = Trainer(cfg_)
    trainer.train()
