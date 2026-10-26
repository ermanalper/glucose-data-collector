from dataclasses import dataclass

@dataclass
class PolyResult:
    coefficients: list[float]  # highest degree first
    degree: int