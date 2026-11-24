
"""Simulation clock — day/night cycle, weather, and seasons.

Deterministic: the clock advances by tick count, no RNG.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationClock:
    tick: int = 0
    ticks_per_day: int = 240
    days_per_season: int = 30

    @property
    def day(self):
        return (self.tick // self.ticks_per_day) + 1

    @property
    def time_of_day(self):
        progress = (self.tick % self.ticks_per_day) / self.ticks_per_day

        if progress < 0.25:
            return "Dawn"
        elif progress < 0.75:
            return "Day"
        elif progress < 0.9:
            return "Dusk"
        return "Night"

    @property
    def season(self):
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        season_index = (self.day - 1) // self.days_per_season % 4
        return seasons[season_index]

    
    @property
    def weather(self):
        weather_patterns = {
            "Spring": ["Rain", "Cloudy", "Clear"],
            "Summer": ["Clear", "Clear", "Rain"],
            "Autumn": ["Cloudy", "Rain", "Clear"],
            "Winter": ["Snow", "Cloudy", "Clear"],
        }

        pattern = weather_patterns[self.season]
        return pattern[(self.day - 1) % len(pattern)]


    def advance(self, steps=1):
        if steps < 0:
            raise ValueError("Steps cannot be negative")

        self.tick += steps
