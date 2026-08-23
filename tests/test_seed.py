import random

import numpy as np

from settings import set_global_seed


def test_set_global_seed_reproducible():
    set_global_seed(12345)
    first = (
        random.random(),
        np.random.random(),
        np.random.randint(0, 100),
    )

    set_global_seed(12345)
    second = (
        random.random(),
        np.random.random(),
        np.random.randint(0, 100),
    )

    assert first == second
