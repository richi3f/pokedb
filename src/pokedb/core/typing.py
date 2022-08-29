__all__ = ["PathLike"]

import os
from typing import Union


PathLike = Union[str, bytes, os.PathLike]
