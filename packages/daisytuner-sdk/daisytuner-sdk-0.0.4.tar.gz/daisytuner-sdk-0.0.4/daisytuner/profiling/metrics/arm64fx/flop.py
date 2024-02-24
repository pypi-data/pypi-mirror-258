import dace
import platform
import numpy as np

from daisytuner.profiling.metrics.metric import Metric


class FLOP(Metric):
    def __init__(
        self, sdfg: dace.SDFG, hostname: str = platform.node(), cache=None
    ) -> None:
        super().__init__(
            sdfg,
            [
                "FP_DP_FIXED_OPS_SPEC",
                "FP_DP_SCALE_OPS_SPEC",
                "FP_HP_FIXED_OPS_SPEC",
                "FP_HP_SCALE_OPS_SPEC",
                "FP_SP_FIXED_OPS_SPEC",
                "FP_SP_SCALE_OPS_SPEC",
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
                    for thread_id, measurements in counters["FP_DP_FIXED_OPS_SPEC"][
                        state
                    ].items()
                ]
            )
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["FP_DP_SCALE_OPS_SPEC"][
                        state
                    ].items()
                ]
            ) * (512 / 128)
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["FP_HP_FIXED_OPS_SPEC"][
                        state
                    ].items()
                ]
            )
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["FP_HP_SCALE_OPS_SPEC"][
                        state
                    ].items()
                ]
            ) * (512 / 128)
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["FP_SP_FIXED_OPS_SPEC"][
                        state
                    ].items()
                ]
            )
            volume += sum(
                [
                    measurements[0]
                    for thread_id, measurements in counters["FP_SP_SCALE_OPS_SPEC"][
                        state
                    ].items()
                ]
            ) * (512 / 128)

        metric = 1e-6 * volume
        return metric

    def compute_per_thread(self) -> np.ndarray:
        counters = self.values()

        volume = []
        for state in self._sdfg.states():
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_DP_FIXED_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
            )
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_DP_SCALE_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
                * (512 / 128)
            )
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_HP_FIXED_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
            )
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_HP_SCALE_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
                * (512 / 128)
            )
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_SP_FIXED_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
            )
            volume.append(
                np.array(
                    [
                        measurements[0]
                        for thread_id, measurements in counters["FP_SP_SCALE_OPS_SPEC"][
                            state
                        ].items()
                    ]
                )
                * (512 / 128)
            )

        metric = 1e-6 * np.vstack(volume).sum(axis=0, keepdims=False)
        return metric
