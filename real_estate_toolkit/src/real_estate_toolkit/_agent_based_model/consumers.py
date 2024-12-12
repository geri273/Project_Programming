from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from .houses import House
from .house_market import HousingMarket

class Segment(Enum):
    FANCY = auto()
    OPTIMIZER = auto()
    AVERAGE = auto()

@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    house: Optional[House] = None

    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time using compound interest.
        """
        for _ in range(years):
            self.savings += self.annual_income * self.saving_rate
            self.savings *= (1 + self.interest_rate)

    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house based on preferences.
        """
        if self.house:
            return  # Consumer already owns a house

        affordable_houses = housing_market.get_houses_that_meet_requirements(max_price=self.savings, segment=self.segment.name)
        if not affordable_houses:
            return

        house_to_buy = affordable_houses[0]  # Simplified selection
        house_to_buy.sell_house()
        self.house = house_to_buy
