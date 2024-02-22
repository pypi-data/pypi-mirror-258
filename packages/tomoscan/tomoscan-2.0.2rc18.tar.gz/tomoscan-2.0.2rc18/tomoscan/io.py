# coding: utf-8

"""Module dedicated to input / output utils"""

from typing import Optional
import logging
import os
from silx.io.h5py_utils import File as HDF5File

_logger = logging.getLogger(__name__)

_DEFAULT_SWMR_MODE = None


def get_swmr_mode() -> Optional[bool]:
    """
    Return True if the swmr should be used in the tomoools scope
    """
    swmr_mode = os.environ.get("TOMOTOOLS_SWMR", _DEFAULT_SWMR_MODE)
    if swmr_mode in (None, "None", "NONE"):
        return None
    else:
        return swmr_mode in (
            True,
            "True",
            "true",
            "TRUE",
            "1",
            1,
        )


def check_virtual_sources_exist(fname, data_path):
    """
    Check that a virtual dataset points to actual data.

    :param str fname: HDF5 file path
    :param str data_path: Path within the HDF5 file

    :return bool res: Whether the virtual dataset points to actual data.
    """
    with HDF5File(fname, "r", swmr=get_swmr_mode()) as f:
        if data_path not in f:
            _logger.error(f"No dataset {data_path} in file {fname}")
            return False
        dptr = f[data_path]
        if not dptr.is_virtual:
            return True
        for vsource in dptr.virtual_sources():
            vsource_fname = os.path.join(
                os.path.dirname(dptr.file.filename), vsource.file_name
            )
            if not os.path.isfile(vsource_fname):
                _logger.error(f"No such file: {vsource_fname}")
                return False
            elif not check_virtual_sources_exist(vsource_fname, vsource.dset_name):
                _logger.error(f"Error with virtual source {vsource_fname}")
                return False
    return True
