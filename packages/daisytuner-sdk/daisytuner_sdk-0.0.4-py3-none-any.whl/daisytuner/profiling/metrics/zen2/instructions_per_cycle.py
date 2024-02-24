import dace
import platform

from daisytuner.profiling.metrics.compund_metric import CompoundMetric
from daisytuner.profiling.metrics.zen2.instructions import Instructions
from daisytuner.profiling.metrics.zen2.cycles import Cycles


class InstructionsPerCycle(CompoundMetric):
    def __init__(self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None):
        super().__init__(
            metric_a=Instructions(sdfg, hostname, cache=cache),
            metric_b=Cycles(sdfg, hostname, cache=cache),
        )
