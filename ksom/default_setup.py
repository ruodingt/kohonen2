import hashlib

from datetime import datetime

import shutil

import os

import re

from ksom.config import get_cfg_defaults

LIB_ROOT = os.path.dirname(os.path.dirname(__file__))


def default_setup(config_file=None, max_iter=None, batch_size=None, verbose=True):
    cfg = get_cfg_defaults()
    cfg.EXP_NAME = f'default_exp_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[-6:]}'
    if config_file is not None:
        if config_file.startswith("som://"):
            config_file = re.sub("som:/", LIB_ROOT, config_file)
        cfg.merge_from_file(config_file)
        exp_name = os.path.split(config_file)[-1].split('.')[0]
        cfg.EXP_NAME = exp_name
    cfg.LOG_DIR = os.path.join(LIB_ROOT, 'logs', cfg.EXP_NAME)
    shutil.rmtree(cfg.LOG_DIR, ignore_errors=True)
    os.makedirs(cfg.LOG_DIR, exist_ok=True)
    if max_iter:
        cfg.MAX_ITER = max_iter
    if batch_size:
        cfg.DATA.BATCH_SIZE = batch_size
    # cfg.freeze()
    if verbose:
        print(cfg)
    return cfg
