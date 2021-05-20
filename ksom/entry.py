import click

from ksom.default_setup import default_setup
from ksom.trainer import Trainer


def run_som_training_(config_file):
    """

    :param config_file:
    :param max_iter: overwrite max_iter in config
    :param batch_size: overwrite batch_size in config
    :return:
    """
    cfg_ = default_setup(config_file=config_file, verbose=True)
    trainer = Trainer(cfg_)
    trainer.train()
    return trainer.model


@click.group()
def cli():
    pass


@click.command()
@click.option("--config-file", default="som://configs/exp1.yaml")
def train(config_file):
    run_som_training_(config_file)


cli.add_command(train)

if __name__ == "__main__":
    run_som_training_(config_file="som://configs/exp1.yaml")
