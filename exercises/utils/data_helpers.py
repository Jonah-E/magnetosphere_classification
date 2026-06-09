"""
utils/data_helpers.py
---------------------
Small helper functions for dataset creation and inspection.

These are separated from the notebook to keep teaching code readable.
Functions here are either purely algorithmic (find_consecutive_window)
or involve boilerplate API calls (fetch_positions) that would distract
from the main narrative.
"""

import numpy as np
import pandas as pd


def find_consecutive_window(mask: np.ndarray, min_len: int):
    """Return (start, end) indices of the first run of True values in *mask*
    that is at least *min_len* steps long.

    Parameters
    ----------
    mask : 1-D boolean array
        True where the condition holds (e.g. a particular energy grid is active).
    min_len : int
        Minimum required length of the consecutive run.

    Returns
    -------
    (start, end) tuple of ints, or None if no qualifying run exists.
    The returned slice [start:end] has exactly min_len elements.
    """
    in_run, start = False, 0
    for i, val in enumerate(mask):
        if val and not in_run:
            in_run, start = True, i
        elif not val and in_run:
            if i - start >= min_len:
                return start, start + min_len
            in_run = False
    if in_run and len(mask) - start >= min_len:
        return start, start + min_len
    return None


def fetch_positions(cdas, dataset: str, variable: str, t0, t1,
                    epoch_var: str = 'Epoch', re_km: float = 6371.0) -> pd.DataFrame:
    """Download spacecraft position data from CDAWeb and convert to Earth radii.

    Parameters
    ----------
    cdas : CdasWs
        An initialised CdasWs client.
    dataset : str
        CDAWeb dataset identifier, e.g. 'MMS1_MEC_SRVY_L2_EPHTS04D'.
    variable : str
        Variable name within the dataset, e.g. 'mms1_mec_r_gse'.
    t0, t1 : datetime
        Start and end of the requested time range.
    epoch_var : str
        Name of the time coordinate in the returned data (default 'Epoch').
    re_km : float
        Earth radius in km used for the unit conversion (default 6371.0).

    Returns
    -------
    pd.DataFrame with columns ['x', 'y', 'z'] in units of R_E,
    indexed by UTC timestamps.  Returns an empty DataFrame on failure.
    """
    status, data = cdas.get_data(dataset, [variable], t0, t1)
    print(status)
    if not data or variable not in data:
        return pd.DataFrame(columns=['x', 'y', 'z'])

    times = data[epoch_var].values
    xyz   = data[variable].values / re_km          # km → R_E
    return pd.DataFrame(xyz, columns=['x', 'y', 'z'], index=pd.to_datetime(times))
