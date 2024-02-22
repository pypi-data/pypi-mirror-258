"""
Backend implementations.
"""
from __future__ import annotations
from .gpg import GpgBackend
from .secretservice import SecretServiceBackend
from .wincred import WincredBackend

__all__ = (
    'GpgBackend',
    'SecretServiceBackend',
    'WincredBackend',
)
