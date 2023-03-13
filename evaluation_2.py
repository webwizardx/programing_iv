from datetime import datetime
from typing import Tuple


class Boat:
    def __init__(self, license_plate: str, length: int, year_of_manufacture: int):
        self.license_plate = license_plate
        self.length = length
        self.year_of_manufacture = year_of_manufacture

    def calculate_rent(self) -> int:
        return 10 * self.length * 8

    def __repr__(self) -> str:
        return str(vars(self))


class Sailboat(Boat):
    def __init__(self, masts: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.masts = masts

    def calculate_rent(self) -> int:
        return super().calculate_rent() + self.masts


class MotorSportBoat(Boat):
    def __init__(self, housepower: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.housepower = housepower

    def calculate_rent(self) -> int:
        return super().calculate_rent() + self.housepower


class Yacht(MotorSportBoat):
    def __init__(self, cabins: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cabins = cabins

    def calculate_rent(self) -> int:
        return super().calculate_rent() + self.cabins


class Rent:
    def __init__(self, name: str, client_id: str, start_date: datetime, end_date: datetime,  mooring_position: Tuple[int, int], ship: Boat):
        self.name = name
        self.client_id = client_id
        self.start_date = start_date
        self.end_date = end_date
        self.mooring_position = mooring_position
        self.ship = ship

    def calculate_rent(self):
        days = (self.end_date - self.start_date).days + 1
        return days * self.ship.calculate_rent()

    def set_ship(self, ship: Boat):
        self.ship = ship


if __name__ == '__main__':
    name = 'John'
    client_id = '123'
    start_date = datetime(2023, 3, 11)
    end_date = datetime(2023, 3, 18)
    mooring_position = (0, 0)

    ship = Boat(license_plate='AABBCC', length=10, year_of_manufacture=2023)
    rent = Rent(name=name, client_id=client_id, start_date=start_date,
                end_date=end_date, mooring_position=mooring_position, ship=ship)
    rent_value = rent.calculate_rent()
    assert rent_value == 6400
    #
    ship = Sailboat(license_plate='AABBCC', length=10,
                    year_of_manufacture=2023, masts=10)
    rent.set_ship(ship)
    rent_value = rent.calculate_rent()
    assert rent_value == 6480
    #
    ship = MotorSportBoat(license_plate='AABBCC', length=10,
                          year_of_manufacture=2023, housepower=10)
    rent.set_ship(ship)
    rent_value = rent.calculate_rent()
    assert rent_value == 6480
    #
    ship = Yacht(license_plate='AABBCC', length=10,
                 year_of_manufacture=2023, housepower=10, cabins=10)
    rent.set_ship(ship)
    rent_value = rent.calculate_rent()
    assert rent_value == 6560
