from dataclasses import dataclass
from abc import ABC


class ExTask(ABC):
    """Exchange task for DLMS client"""


class InitType(ExTask):
    """nothing params"""


@dataclass
class ReadAttribute(ExTask):
    ln: str
    index: int


