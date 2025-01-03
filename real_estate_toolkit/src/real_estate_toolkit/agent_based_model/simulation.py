from enum import Enum, auto
from dataclasses import dataclass
from random import gauss, randint, shuffle
from typing import List, Dict, Any, Optional
from .houses import House
from .house_market import HousingMarket
from .consumers import Segment, Consumer

class CleaningMarketMechanism(Enum):
    INCOME_ORDER_DESCENDANT = auto()
    INCOME_ORDER_ASCENDANT = auto()
    RANDOM = auto()

@dataclass
class AnnualIncomeStatistics:
    minimum: float
    average: float
    standard_deviation: float
    maximum: float

@dataclass
class ChildrenRange:
    minimum: float = 0
    maximum: float = 5

@dataclass
class Simulation:
    housing_market_data: List[Dict[str, Any]]
    consumers_number: int
    years: int
    annual_income: AnnualIncomeStatistics
    children_range: ChildrenRange
    cleaning_market_mechanism: CleaningMarketMechanism
    down_payment_percentage: float = 0.2
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    
    def create_housing_market(self):
        self.housing_market = HousingMarket(
            [House(**data) for data in self.housing_market_data]
        )

    def create_consumers(self) -> None:
        self.consumers = []
        for _ in range(self.consumers_number):
            income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
            while income < self.annual_income.minimum or income > self.annual_income.maximum:
                income = gauss(self.annual_income.average, self.annual_income.standard_deviation)

            children = randint(self.children_range.minimum, self.children_range.maximum)
            segment = Segment(randint(1, len(Segment)))
            consumer = Consumer(
                id=len(self.consumers),
                annual_income=income,
                children_number=children,
                segment=segment,
                savings=income * self.saving_rate,
                saving_rate=self.saving_rate,
                interest_rate=self.interest_rate
            )
            self.consumers.append(consumer)

    def compute_consumers_savings(self) -> None:
        for consumer in self.consumers:
            Consumer.compute_savings(self.years)


    def clean_the_market(self) -> None:
        if self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_DESCENDANT:
            self.consumers.sort(key=lambda c: Consumer.annual_income, reverse=True)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_ASCENDANT:
            self.consumers.sort(key=lambda c: Consumer.annual_income)
        else:
            shuffle(self.consumers)

        for consumer in self.consumers:
            if not Consumer.house:
                Consumer.buy_a_house(self.housing_market)

    def compute_owners_population_rate(self) -> float:
        owners = sum(1 for c in self.consumers if Consumer.house)
        return owners / self.consumers_number

    def compute_houses_availability_rate(self) -> float:
        available_houses = sum(1 for house in self.housing_market.houses if house.available)
        return available_houses / len(self.housing_market.houses)
