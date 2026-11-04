"""Tests for engine/clock.py (M10)."""

from __future__ import annotations

import pytest

from engine.clock import Clock, Season, Weather


class TestClock:
    def test_initial_state(self):
        c = Clock(seed=1)
        assert c.hour == 6
        assert c.day == 0
        assert c.season == Season.SPRING
        assert c.weather == Weather.CLEAR

    def test_advance_hours(self):
        c = Clock()
        c.advance(3)
        assert c.hour == 9
        assert c.day == 0

    def test_advance_rolls_over_day(self):
        c = Clock()
        c.hour = 22
        c.advance(4)
        assert c.hour == 2
        assert c.day == 1

    def test_season_cycle(self):
        c = Clock()
        c.day = 27
        c.hour = 23
        c.advance(1)  # rolls to day 0 and advances season
        assert c.day == 0
        assert c.season == Season.SUMMER

    def test_is_night(self):
        c = Clock()
        c.hour = 3
        assert c.is_night()
        c.hour = 12
        assert not c.is_night()
        c.hour = 21
        assert c.is_night()

    def test_light_level(self):
        c = Clock()
        c.hour = 12
        assert c.light_level() > 0.9
        c.hour = 3
        assert c.light_level() <= 0.2

    def test_time_of_day(self):
        c = Clock()
        c.hour = 6
        c.minute = 30
        assert c.time_of_day() == "06:30"

    def test_update_weather_winter(self):
        c = Clock()
        c.season = Season.WINTER
        c.update_weather()
        assert c.weather in Weather.ALL
        assert c.temperature < 10.0

    def test_update_weather_summer(self):
        c = Clock()
        c.season = Season.SUMMER
        c.update_weather()
        assert c.temperature > 20.0

    def test_deterministic_with_seed(self):
        c1 = Clock(seed=42)
        c2 = Clock(seed=42)
        c1.advance(100)
        c2.advance(100)
        c1.update_weather()
        c2.update_weather()
        assert c1.weather == c2.weather
        assert c1.temperature == pytest.approx(c2.temperature)

    def test_to_from_dict_roundtrip(self):
        c = Clock(seed=7)
        c.advance(50)
        c.update_weather()
        d = c.to_dict()
        c2 = Clock.from_dict(d)
        assert c2.day == c.day
        assert c2.hour == c.hour
        assert c2.season == c.season
        assert c2.weather == c.weather
        assert c2.temperature == pytest.approx(c.temperature)