from yacs.config import CfgNode as CN

_C = CN()

_C.INIT_LR = 0.1
_C.MAX_ITER = 100
_C.CALLBACK_PERIOD = 2

_C.SOM = CN()
_C.SOM.H = 10
_C.SOM.W = 10
_C.SOM.D = 3

_C.DATA = CN()
_C.DATA.LENGTH = 100
_C.DATA.DIM = 3
_C.DATA.BATCH_SIZE = 1

_C.LOG_DIR = 'logs'


def configurable(init_fn, *, from_config=None):
    def wrap(self, *args, **kwargs):
        _cfg = [c for c in args if isinstance(c, CN)]
        if _cfg:
            cfg = _cfg[0]
            d = type(self).from_config(cfg)
            d.update(**kwargs)
            return init_fn(self, **d)
        else:
            return init_fn(self, *args, **kwargs)

    return wrap


def get_cfg_defaults():
    """
    get the default config node
    :return:
    """
    return _C.clone()
