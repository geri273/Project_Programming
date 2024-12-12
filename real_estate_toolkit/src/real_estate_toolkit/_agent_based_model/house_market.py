from typing import List, Optional
from .houses import House

class HousingMarket:
    def __init__(self, houses: List[House]):
        self.houses: List[House] = houses

    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve specific house by ID.
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        return None

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate average house price, optionally filtered by number of bedrooms.
        """
        filtered_houses = [house for house in self.houses if house.available]
        if bedrooms is not None:
            filtered_houses = [house for house in filtered_houses if house.bedrooms == bedrooms]

        if not filtered_houses:
            return 0.0
        return round(sum(house.price for house in filtered_houses) / len(filtered_houses), 2)

    def get_houses_that_meet_requirements(self, max_price: int, segment: str) -> List[House]:
        """
        Filter houses based on buyer requirements.
        """
        filtered_houses = [house for house in self.houses if house.available and house.price <= max_price]
        return filtered_houses
