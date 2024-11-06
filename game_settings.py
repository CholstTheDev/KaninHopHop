"""Defines possible settings of the game in a dataclass and with an enum"""
from dataclasses import dataclass
from enum import Enum


class Variant(Enum):
    NORMAL = 0
    FAST = 1
    SLOW = 2


@dataclass
class Simulation_Settings:
    player_count: int = 3
    rabbit_count: int = 20
    simulation_iterations: int = 1000
    variant: Variant = Variant.NORMAL