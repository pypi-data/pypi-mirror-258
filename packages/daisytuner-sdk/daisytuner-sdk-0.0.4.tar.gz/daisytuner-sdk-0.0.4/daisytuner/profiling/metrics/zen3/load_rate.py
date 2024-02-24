import dace
import platform

from daisytuner.profiling.metrics.compund_metric import CompoundMetric
from daisytuner.profiling.metrics.zen3.loads import Loads
from daisytuner.profiling.metrics.zen3.instructions import Instructions


class LoadRate(CompoundMetric):
    def __init__(self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None):
        super().__init__(
            metric_a=Loads(sdfg, hostname, cache=cache),
            metric_b=Instructions(sdfg, hostname, cache=cache),
        )
