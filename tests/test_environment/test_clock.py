
from engine.clock import SimulationClock


def test_initial_clock():
    clock = SimulationClock()

    assert clock.tick == 0
    assert clock.day == 1
    assert clock.time_of_day == "Dawn"
    assert clock.season == "Spring"


def test_day_and_night_cycle():
    clock = SimulationClock()

    clock.advance(60)
    assert clock.time_of_day == "Day"

    clock.advance(120)
    assert clock.time_of_day == "Dusk"

    clock.advance(36)
    assert clock.time_of_day == "Night"


def test_new_day():
    clock = SimulationClock()

    clock.advance(240)

    assert clock.day == 2
    assert clock.time_of_day == "Dawn"


def test_season_change():
    clock = SimulationClock()

    clock.advance(30 * 240)

    assert clock.day == 31
    assert clock.season == "Summer"


def test_negative_steps():
    clock = SimulationClock()

    try:
        clock.advance(-1)
        assert False, "Negative steps should raise ValueError"
    except ValueError:
        pass


def test_weather_system():
    clock = SimulationClock()

    assert clock.weather == "Rain"

    clock.advance(30 * 240)

    assert clock.season == "Summer"
    assert clock.weather == "Clear"
