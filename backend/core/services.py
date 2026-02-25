from global_settings.constants import (
    STATUS_VEHICLE,
    COLOR_VEHICLE,
    FUEL_TYPE,
    BRAND_VEHICLE,
)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Car


class CarService:
    def __init__(self):
        self.status_vehicle = STATUS_VEHICLE
        self.color_vehicle = COLOR_VEHICLE
        self.fuel_type = FUEL_TYPE
        self.brand_vehicle = BRAND_VEHICLE

    def filter_cars(self, cars, status=None, brand=None, color=None, fuel_type=None):
        if status:
            if status in self.status_vehicle:
                cars = cars.filter(status=status)
        if brand:
            if brand in self.brand_vehicle:
                cars = cars.filter(brand=brand)
        if color:
            if color in self.color_vehicle:
                cars = cars.filter(color=color)
        if fuel_type:
            if fuel_type in self.fuel_type:
                cars = cars.filter(fuel_type=fuel_type)
        return cars


def update_car_location(*, car: Car, location):
    """
    - updates DB
    - triggers real‑time broadcast
    """
    car.location = location
    car.save(update_fields=["location"])
    if location:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"car_{car.id}",
            {
                "type": "car_location_update",
                "location": location,
            },
        )
    return car
