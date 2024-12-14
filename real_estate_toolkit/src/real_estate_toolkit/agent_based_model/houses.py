from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore] = field(default=None)
    available: bool = True

    def calculate_price_per_square_foot(self) -> float:
        if self.area == 0:
            return 0.0
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        return (current_year - self.year_built) < 5

    def get_quality_score(self) -> None:
        if self.is_new_construction() and self.area >= 200:
            self.quality_score = QualityScore.EXCELLENT
        elif self.area >= 200 and self.year_built >= 150:
            self.quality_score = QualityScore.GOOD
        elif self.area >= 150 and self.year_built >= 100:
            self.quality_score = QualityScore.AVERAGE
        elif self.area < 150 or self.year_built < 80:
            self.quality_score = QualityScore.FAIR
        else:
            self.quality_score = QualityScore.POOR

    def sell_house(self) -> None:
        self.available = False
