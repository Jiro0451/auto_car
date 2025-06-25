from field import Field
from car import Car


class TestAddCar:
    def test_should_add_car_given_car_object(self):
        car_name = "Car"
        initial_pos = "1 2 N"
        commands = "FFRFFFFRRL"

        test_field = Field(10, 10)
        test_field.add_car(car_name, initial_pos, commands)

        assert len(test_field.cars) is 1
        assert isinstance(test_field.cars[0], Car)


class TestIsCarNameUsed:
    def test_should_return_true_given_car_name_in_already_exists(self):
        test_field = Field(10, 10)
        test_field.add_car("Test Car A", "1 2 N", "FLFRF")
        test_field.add_car("Test Car B", "3 4 W", "FLFRF")
        test_field.add_car("Test Car C", "5 6 S", "FLFRF")
        car_name = "Test Car A"

        result = test_field.is_car_name_used(car_name)

        assert result is True

    def test_should_return_true_given_car_name_in_already_exists(self):
        test_field = Field(10, 10)
        test_field.add_car("Test Car A", "1 2 N", "FLFRF")
        test_field.add_car("Test Car B", "3 4 W", "FLFRF")
        test_field.add_car("Test Car C", "5 6 S", "FLFRF")
        car_name = "New Car"

        result = test_field.is_car_name_used(car_name)

        assert result is False


class TestGetCarDetails:
    def test_should_return_all_cars_in_formatted_detail_given_existing_cars(self):
        test_field = Field(10, 10)
        test_field.add_car("Test Car A", "1 2 N", "FLFRF")
        test_field.add_car("Test Car B", "3 4 W", "FLFRF")
        test_field.add_car("Test Car C", "5 6 S", "FLFRF")

        result = test_field.get_car_details()

        assert len(result) is 3
        assert "- Test Car A, (1, 2) N, FLFRF" in result
        assert "- Test Car B, (3, 4) W, FLFRF" in result
        assert "- Test Car C, (5, 6) S, FLFRF" in result

    def test_should_return_empty_list_given_no_existing_cars(self):
        test_field = Field(10, 10)

        result = test_field.get_car_details()

        assert result == []


class TestGetSimulatedResults:
    def test_should_return_simulated_results_for_single_car(self):
        test_field = Field(10, 10)
        test_field.add_car("Test Car A", "1 2 N", "FFRFFFFRRL")

        result = test_field.get_simulated_results()

        assert "- Test Car A, (5, 4) S" in result

    def test_should_return_simulated_results_with_collision_for_single_car(self):
        test_field = Field(10, 10)
        test_field.add_car("Test Car A", "1 2 N", "FFFFFFFFFFF")

        result = test_field.get_simulated_results()

        print(result)
        assert "- Test Car A, hits the wall at (1, 10) at step 8" in result

    def test_should_return_simulated_results_for_multiple_cars(self):
        test_field = Field(10, 10)
        test_field.add_car("A", "1 2 N", "FFRFFFFRRL")
        test_field.add_car("B", "7 8 W", "FFLFFFFFFF")
        test_field.add_car("C", "9 9 N", "")
        test_field.add_car("D", "0 0 S", "F")

        result = test_field.get_simulated_results()

        assert "- A, collides with B at (5, 4) at step 7" in result
        assert "- B, collides with A at (5, 4) at step 7" in result
        assert "- C, (9, 9) N" in result
        assert "- D, hits the wall at (0, 0) at step 1" in result
