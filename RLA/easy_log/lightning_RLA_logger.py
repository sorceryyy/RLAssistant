from lightning.pytorch.loggers.logger import Logger, rank_zero_experiment
from lightning.pytorch.utilities import rank_zero_only
from typing import Optional

from RLA.easy_log.time_step import time_step_holder
from RLA.easy_log import logger
from RLA.easy_log.const import *

class Lightning_RLA_Logger(Logger):
    def __init__(self, name_prefix: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_prefix = name_prefix

    @property
    def name(self):
        return "Lightning_RLA_Logger"

    @property
    def version(self):
        # Return the experiment version, int or str.
        return "0.1"

    @rank_zero_only
    def log_hyperparams(self, params):
        # params is an argparse.Namespace
        # your code to record hyperparameters goes here
        pass

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # metrics is a dictionary of metric names and values
        # your code to record metrics goes here
        if self.name_prefix is not None:
            metrics = {f"{self.name_prefix}{k}": v for k, v in metrics.items()}

        for k, v in metrics.items():
            logger.logkv(k, v)
        time_step_holder.set_time(step)
        logger.dumpkvs()

    @rank_zero_only
    def save(self):
        # Optional. Any code necessary to save logger data goes here
        pass

    @rank_zero_only
    def finalize(self, status):
        # Optional. Any code that needs to be run after training
        # finishes goes here
        pass