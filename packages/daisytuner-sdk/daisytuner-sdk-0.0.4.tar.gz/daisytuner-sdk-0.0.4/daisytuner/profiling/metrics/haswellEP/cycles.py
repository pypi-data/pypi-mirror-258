import numpy as np
import dace
import platform


from daisytuner.profiling.metrics.metric import Metric


class Cycles(Metric):
    def __init__(
        self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None
    ) -> None:
        super().__init__(
            sdfg,
            [
                "CPU_CLK_UNHALTED_CORE",
            ],
            "cpu",
            hostname,
            "haswellEP",
            cache=cache,
        )

    def compute(self) -> float:
        counters = self.values()

        volume = 0.0
        for state in self._sdfg.states():
            volume += max(
                [
                    measurements[0]
                    for thread_id, measurements in counters["CPU_CLK_UNHALTED_CORE"][
                        state
                    ].items()
                ]
            )

        metric = volume
        return metric

    def compute_per_thread(self) -> float:
        counters = self.values()

        volume = []
        for state in self._sdfg.states():
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters[
                            "CPU_CLK_UNHALTED_CORE"
                        ][state].items()
                    ]
                )
            )

        metric = np.vstack(volume).sum(axis=0, keepdims=False)
        return metric
