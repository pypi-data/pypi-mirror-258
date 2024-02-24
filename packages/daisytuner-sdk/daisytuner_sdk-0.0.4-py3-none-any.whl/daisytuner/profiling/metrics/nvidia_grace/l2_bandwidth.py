import dace
import platform

from daisytuner.profiling.metrics.compund_metric import CompoundMetric
from daisytuner.profiling.metrics.nvidia_grace.l2_volume import L2Volume
from daisytuner.profiling.metrics.nvidia_grace.runtime import Runtime


class L2Bandwidth(CompoundMetric):
    def __init__(self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None):
        super().__init__(
            metric_a=L2Volume(sdfg, hostname), metric_b=Runtime(sdfg, hostname)
        )
