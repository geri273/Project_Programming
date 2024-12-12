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
        """
        Calculate and return the price per square foot.
        """
        if self.area == 0:
            return 0.0
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if house is considered new construction (< 5 years old).
        """
        return (current_year - self.year_built) < 5

    def get_quality_score(self) -> None:
        """
        Generate a quality score based on house attributes.

        - Excellent: New construction and large area
        - Good: Large area and modern build
        - Average: Balanced area and older build
        - Fair: Smaller area or older build
        - Poor: Very small area or very old build
        """
        if self.is_new_construction() and self.area >= 200:
            self.quality_score = QualityScore.Excellent
        elif self.area >= 200 and self.year_built >= 150:
            self.quality_score = QualityScore.Good
        elif self.area >= 150 and self.year_built >= 100:
            self.quality_score = QualityScore.Average
        elif self.area < 150 or self.year_built < 80:
            self.quality_score = QualityScore.Fair
        else:
            self.quality_score = QualityScore.Poor

    def sell_house(self) -> None:
        """
        Mark house as sold.
        """
        self.available = False
