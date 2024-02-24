import numpy as np
import dace
import platform


from daisytuner.profiling.metrics.metric import Metric


class Branches(Metric):
    def __init__(
        self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None
    ) -> None:
        super().__init__(
            sdfg,
            [
                "RETIRED_BRANCH_INSTR",
            ],
            "cpu",
            hostname,
            "zen",
            cache=cache,
        )

    def compute(self) -> float:
        counters = self.values()

        volume_branches = 0.0
        for state in self._sdfg.states():
            if not state in counters["RETIRED_BRANCH_INSTR"]:
                continue

            volume_branches += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["RETIRED_BRANCH_INSTR"][
                        state
                    ].items()
                ]
            )

        metric = volume_branches
        return metric

    def compute_per_thread(self) -> np.ndarray:
        counters = self.values()

        volume_branches = []
        for state in self._sdfg.states():
            if not state in counters["RETIRED_BRANCH_INSTR"]:
                continue

            volume_branches.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["RETIRED_BRANCH_INSTR"][
                            state
                        ].items()
                    ]
                )
            )

        metric = np.vstack(volume_branches).sum(axis=0, keepdims=False)
        return metric
