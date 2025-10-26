"""Tasks package for travel assistant"""

from .flight_task import task_flights
from .hotel_task import task_hotels
from .tour_task import task_tour
from .advice_task import task_advice

__all__ = ['task_flights', 'task_hotels', 'task_tour', 'task_advice']
