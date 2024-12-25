"""
StayUp - A modern Python package to prevent system sleep by simulating mouse movements
"""

from .core import KeepAwake
from .cli import main

__version__ = "0.1.0"
__all__ = ["KeepAwake", "main"]
