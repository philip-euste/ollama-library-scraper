from colorama import Fore as F
from typing import TypedDict


class ModelData(TypedDict):
    full_name: str
    family: str
    variant: str | None
    storage: str | None
    context: str | None
    capabilities: list[str]
    modalities: list[str]

class NormalizedModelData(TypedDict):
    full_name: str
    family: str
    variant: str | None
    storage: float 
    context: float
    capabilities: list[str]
    modalities: list[str]
    parameter: float
    parameter_normalized: float
    context_normalized: float
    parameter_efficiency: float
    context_efficiency: float
    additive_normalized_efficiency: float
    multiplicative_normalized_efficiency: float


# =========================================================
# COLORIZING
# =========================================================

FF: str = F.RESET
FC: str = F.CYAN
FG: str = F.GREEN
FR: str = F.RED

def print_stats(string: str, color: str = FC) -> None:
    print(f"{color}{string}{FF}")


def print_breakline(number: int, color: str = FF) -> None:
    print(f"{color}{'-' * number}{FF}")

