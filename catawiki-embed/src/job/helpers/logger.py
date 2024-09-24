"""logger initialization."""

import logging
import warnings


def init() -> None:
    """Set Logger and Filter Google SDK warnings."""
    log_format = (
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s"
    )
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    warnings.filterwarnings(
        "ignore",
        "Your application has authenticated using end user credentials",
    )
