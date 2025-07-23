from dataclasses import dataclass

import numpy as np


@dataclass
class Stroke:

    X: np.ndarray  # NxD, where D=2 or D=3

    @property
    def dimension(self) -> int:
        return self.X.shape[1]
    
    def __len__(self) -> int:
        return self.X.shape[0]
