"""Environmental clock: day/night cycle, weather, and seasons (M10).

The clock advances deterministically with the simulation tick.  Each tick
advances the in-game clock by a configurable amount of minutes.  Seasons
cycle every N ticks; weather changes are probabilistic but seeded for
determinism.
"""

from __future__ import annotations

from typing import Optional

from dsa.hash_table import HashTable


# In-game minutes per real-world second when the sim is running.
DEFAULT_TICK_MINUTES = 15.0
# Ticks per in-game day.
TICKS_PER_DAY = 24  # one tick == one hour by default
MINUTES_PER_DAY = 24 * 60
HOURS_PER_DAY = 24


class Season:
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

    ALL = (SPRING, SUMMER, AUTUMN, WINTER)


class Weather:
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    SNOW = "snow"
    STORM = "storm"

    ALL = (CLEAR, CLOUDY, RAIN, SNOW, STORM)


class Clock:
    """A deterministic in-game clock.

    State is stored as (day, hour, minute) plus the current season and
    weather.  All state is derived from the simulation tick and a seed, so
    repeated runs with the same seed produce identical results.
    """

    def __init__(self, seed: int = 0) -> None:
        self._seed = seed
        self.day = 0
        self.hour = 6  # start at dawn
        self.minute = 0
        self.season = Season.SPRING
        self.weather = Weather.CLEAR
        self.temperature = 20.0  # Celsius
        # Ticks per season; 28 days per season by default.
        self.ticks_per_season = 28 * TICKS_PER_DAY
        self._tick_index = 0

    # ------------------------------------------------------------------ time
    def advance(self, ticks: int = 1) -> None:
        """Advance the clock by *ticks* simulation ticks (one hour each)."""
        self._tick_index += ticks
        self.hour += ticks
        while self.hour >= HOURS_PER_DAY:
            self.hour -= HOURS_PER_DAY
            self.day += 1
        # Season cycle.
        if self.day >= 28:
            self.day = 0
            self._advance_season()

    def _advance_season(self) -> None:
        idx = Season.ALL.index(self.season)
        self.season = Season.ALL[(idx + 1) % len(Season.ALL)]

    # ------------------------------------------------------------------ weather
    def update_weather(self, rng=None) -> None:
        """Recompute weather and temperature for the current season.

        Uses a seeded RNG when supplied so the simulation stays deterministic.
        """
        import random
        if rng is None:
            rng = random.Random(self._seed + self._tick_index)
        # Temperature varies by season.
        base = {
            Season.SPRING: 15.0,
            Season.SUMMER: 28.0,
            Season.AUTUMN: 14.0,
            Season.WINTER: 2.0,
        }[self.season]
        self.temperature = base + rng.uniform(-3.0, 3.0)

        # Weather depends on season and a random draw.
        if self.season == Season.WINTER:
            choices = [Weather.CLEAR, Weather.CLOUDY, Weather.SNOW, Weather.STORM]
        elif self.season == Season.SUMMER:
            choices = [Weather.CLEAR, Weather.CLOUDY, Weather.RAIN, Weather.STORM]
        else:
            choices = [Weather.CLEAR, Weather.CLOUDY, Weather.RAIN]
        self.weather = rng.choice(choices)

    # ------------------------------------------------------------------ accessors
    def time_of_day(self) -> str:
        """Return a human-readable time string, e.g. '06:30'."""
        return f"{self.hour:02d}:{self.minute:02d}"

    def is_night(self) -> bool:
        return self.hour < 6 or self.hour >= 20

    def light_level(self) -> float:
        """Return a 0..1 light multiplier for the current time of day."""
        if self.is_night():
            return 0.15
        # Peak at noon.
        noon = 12.0
        return 0.55 + 0.45 * (1.0 - abs(self.hour - noon) / 6.0)

    def to_dict(self) -> dict:
        return {
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "season": self.season,
            "weather": self.weather,
            "temperature": self.temperature,
            "tick_index": self._tick_index,
            "seed": self._seed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Clock":
        c = cls(seed=data.get("seed", 0))
        c.day = data.get("day", 0)
        c.hour = data.get("hour", 6)
        c.minute = data.get("minute", 0)
        c.season = data.get("season", Season.SPRING)
        c.weather = data.get("weather", Weather.CLEAR)
        c.temperature = data.get("temperature", 20.0)
        c._tick_index = data.get("tick_index", 0)
        return c