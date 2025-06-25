import pytest

from car import Car


def test_car_constructor():
    car_name = "Car"
    initial_pos = "1 2 N"
    commands = "FFRFFFFRRL"

    car = Car(car_name, initial_pos, commands)

    assert car.name == car_name
    assert car.position == (1, 2)
    assert car.direction == "N"
    assert car.commands == ['F', 'F', 'R', 'F', 'F', 'F', 'F', 'R', 'R', 'L']


class TestGetPathAndDestination:
    @pytest.mark.parametrize(
        "car, expected_path, expected_destination", [
            (
                Car("test car", "1 2 N", "FFRFFFFRRL"),
                [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)],
                "(5, 4) S"
            ),
            (
                Car("Drumstick", "3 2 S", "LFFRRFFFLF"),
                [(3, 2), (3, 2), (4, 2), (5, 2), (5, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 2), (2, 1)],
                "(2, 1) S"
            ),
            (
                Car("Chicken", "4 4 N", "RFFLFFLFFR"),
                [(4, 4), (4, 4), (5, 4), (6, 4), (6, 4), (6, 5), (6, 6), (6, 6), (5, 6), (4, 6), (4, 6)],
                "(4, 6) N"
            ),
        ])
    def test_get_path_(self, car, expected_path, expected_destination):

        result_path, result_destination = car.get_path_and_destination()

        assert result_path == expected_path
        assert result_destination == expected_destination


class TestMoveForward:
    @pytest.mark.parametrize(
        "direction, expected_x, expected_y", [
            ("N", 1, 2),
            ("E", 2, 1),
            ("S", 1, 0),
            ("W", 0, 1),
        ])
    def test_should_move_forward(
            self, direction, expected_x, expected_y
    ):
        test_car = Car("test", f"1 1 {direction}", "")

        test_car._move_forward()

        assert test_car.position == (expected_x, expected_y)


class TestTurnLeft:
    @pytest.mark.parametrize(
        "initial_direction, final_direction", [
            ("N", "W"),
            ("W", "S"),
            ("S", "E"),
            ("E", "N"),
        ])
    def test_should_turn_left(self, initial_direction, final_direction):
        test_car = Car("test", f"0 0 {initial_direction}", "")
        test_car._turn_left()
        assert test_car.direction is final_direction


class TestTurnRight:
    @pytest.mark.parametrize(
        "initial_direction, final_direction", [
            ("N", "E"),
            ("E", "S"),
            ("S", "W"),
            ("W", "N"),
        ])
    def test_should_turn_right(self, initial_direction, final_direction):
        test_car = Car("test", f"0 0 {initial_direction}", "")
        test_car._turn_right()
        assert test_car.direction is final_direction
