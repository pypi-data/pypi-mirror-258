import numpy as np
import dace
import platform


from daisytuner.profiling.metrics.metric import Metric


class Instructions(Metric):
    def __init__(
        self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None
    ) -> None:
        super().__init__(
            sdfg,
            [
                "SMSP_INST_EXECUTED_AVG",
            ],
            "gpu",
            hostname,
            "nvidia_cc_ge_7",
            cache=cache,
        )

    def compute(self) -> float:
        counters = self.values()

        volume = 0.0
        for state in self._sdfg.states():
            if state not in counters["SMSP_INST_EXECUTED_AVG"]:
                continue

            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["SMSP_INST_EXECUTED_AVG"][
                        state
                    ].items()
                ]
            )

        metric = volume
        return metric

    def compute_per_thread(self) -> np.ndarray:
        counters = self.values()

        volume = []
        for state in self._sdfg.states():
            if state not in counters["SMSP_INST_EXECUTED_AVG"]:
                continue

            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters[
                            "SMSP_INST_EXECUTED_AVG"
                        ][state].items()
                    ]
                )
            )

        metric = np.vstack(volume).sum(axis=0, keepdims=False)
        return metric
