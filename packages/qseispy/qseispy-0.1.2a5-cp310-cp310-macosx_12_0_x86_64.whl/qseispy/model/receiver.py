import numpy as np


class ReceiverModel(object):
    """
    Receiver model.

    Example:
    >>> from qseispy import ReceiverModel
    >>> receiver = ReceiverModel(dt=0.01,
                                npts=1024,
                                constant_factor=[1.0, 0.0],
                                root_positions=[[0.0, 0.0], [0.0, 0.0]],
                                pole_positions=[[-4.35425, 4.44222], [-4.35425,-4.44222]])
    >>> receiver.add(distance=np.array([1, 2, 3]), depth=0, unit="km")
    >>> receiver.add(distance=np.array([1, 2, 3]), depth=10, unit="deg")
    """

    def __init__(
        self,
        dt,
        npts,
        constant_factor=[1.0, 0.0],
        root_positions=[],
        pole_positions=[],
    ):
        self.dt = dt
        self.npts = npts
        self.constant_factor = constant_factor
        self.root_positions = root_positions
        self.pole_positions = pole_positions

        self.distances = []
        self.depths = []
        self.units = []
        self.num = 0

    def __repr__(self):
        stats = (
            "* ReceiverModel\n"
            f"                      dt: {self.dt}\n"
            f"                    npts: {self.npts}\n"
            f"         constant_factor: {self.constant_factor}\n"
            f"          root_positions: {self.root_positions}\n"
            f"          pole_positions: {self.pole_positions}\n"
            f"                     num: {self.num}\n"
            f"                   units: {self.units}\n"
            f"                  depths: {self.depths}\n"
            f"               distances: {self.distances}\n"
        )
        return stats

    def add(self, distance, depth, unit="km"):
        self.distances.append(distance)
        self.depths.append(float(depth))
        self.units.append(unit)
        self.num += len(distance)
