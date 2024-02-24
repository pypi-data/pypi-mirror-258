import dace
import platform

from daisytuner.profiling.metrics.compund_metric import CompoundMetric
from daisytuner.profiling.metrics.skylakeX.branches import Branches
from daisytuner.profiling.metrics.skylakeX.instructions import (
    Instructions,
)


class BranchRate(CompoundMetric):
    def __init__(self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None):
        super().__init__(
            metric_a=Branches(sdfg, hostname, cache=cache),
            metric_b=Instructions(sdfg, hostname, cache=cache),
        )
