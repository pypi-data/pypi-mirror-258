import dace
import platform
import numpy as np

from daisytuner.profiling.metrics.metric import Metric


class Stores(Metric):
    def __init__(
        self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None
    ) -> None:
        super().__init__(
            sdfg,
            [
                "ST_SPEC",
            ],
            "cpu",
            hostname,
            "arm64fx",
            cache=cache,
        )

    def compute(self) -> float:
        counters = self.values()

        volume = 0.0
        for state in self._sdfg.states():
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["ST_SPEC"][state].items()
                ]
            )

        metric = volume
        return metric

    def compute_per_thread(self) -> np.ndarray:
        counters = self.values()

        volume = []
        for state in self._sdfg.states():
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["ST_SPEC"][
                            state
                        ].items()
                    ]
                )
            )

        metric = np.vstack(volume).sum(axis=0, keepdims=False)
        return metric
