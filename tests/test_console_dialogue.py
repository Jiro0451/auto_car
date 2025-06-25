import io
import sys
import pytest

from car import Car
from console_dialogue import ConsoleDialogue
from field import Field


class TestWelcomeStage:
    @pytest.fixture
    def dialogue_instance(self):
        return ConsoleDialogue()

    @pytest.fixture
    def mock_input(self, monkeypatch):
        input_value = "10 5"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        return input_value.split()

    def test_should_print_welcome_and_prompt(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance._welcome_stage()
        output = capsys.readouterr().out

        assert "Welcome to Auto Driving Car Simulation!" in output
        assert "Please enter the width and height of the simulation field in x y format:" in output

    def test_should_create_field_given_valid_inputs(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance._welcome_stage()
        output = capsys.readouterr().out

        assert isinstance(dialogue_instance.field, Field)
        assert f"You have created a field of {mock_input[0]} x {mock_input[1]}." in output

    def test_should_print_error_given_invalid_inputs(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "invalid"
        monkeypatch.setattr(sys, 'stdin', io.StringIO(input_value))

        with pytest.raises(EOFError):
            dialogue_instance._welcome_stage()

        output = capsys.readouterr().out

        assert "Please enter a valid width and height in x y format (i.e. \"10 10\"):" in output

    def test_should_be_main_menu_stage_after_welcome_stage(
            self, dialogue_instance, mock_input, capsys
    ):
        next_stage = dialogue_instance._welcome_stage()

        assert next_stage == "MAIN"


class TestMainMenuStage:
    @pytest.fixture
    def dialogue_instance(self):
        return ConsoleDialogue()

    def test_should_print_options_prompt(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "1"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        dialogue_instance._main_menu_stage()
        output = capsys.readouterr().out

        assert "Please choose from the following options:" in output
        assert "[1] Add a car to field" in output
        assert "[2] Run simulation" in output

    def test_should_be_build_car_stage_given_option_is_1(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "1"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        next_stage = dialogue_instance._main_menu_stage()

        assert next_stage is "BUILD_CAR"

    def test_should_show_no_cars_error_given_option_is_2_with_no_cars(
            self, dialogue_instance, monkeypatch, capsys
    ):
        dialogue_instance.field = Field(10, 10)
        input_value = "2"
        monkeypatch.setattr(sys, 'stdin', io.StringIO(input_value))

        with pytest.raises(EOFError):
            dialogue_instance._main_menu_stage()

        output = capsys.readouterr().out

        assert "Unable to run simulation. There are no cars currently." in output

    def test_should_be_simulation_stage_given_option_is_2_with_cars(
            self, dialogue_instance, monkeypatch, capsys
    ):
        dialogue_instance.field = Field(10, 10)
        dialogue_instance.field.cars = [
            Car("A", "1 2 N", "")
        ]

        input_value = "2"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        next_stage = dialogue_instance._main_menu_stage()

        assert next_stage is "SIMULATION"

    def test_should_exit_given_option_is_0(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "0"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        next_stage = dialogue_instance._main_menu_stage()

        assert next_stage is "EXIT"

    def test_should_show_error_message_given_invalid_option(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "invalid"
        monkeypatch.setattr(sys, 'stdin', io.StringIO(input_value))

        with pytest.raises(EOFError):
            dialogue_instance._main_menu_stage()

        output = capsys.readouterr().out

        assert f"\"{input_value}\" is not a valid option" in output


class TestBuildCarStage:
    @pytest.fixture
    def dialogue_instance(self):
        console_dialogue = ConsoleDialogue()
        console_dialogue.field = Field(10, 10)
        console_dialogue.field.cars = [
            Car("Used Car", "1 2 N", "")
        ]

        return console_dialogue

    @pytest.fixture
    def mock_input(self, monkeypatch):
        inputs = ["Test Car", "1 2 N", "FFRFFFFRRL"]
        inputs_iter = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs_iter))

        return inputs

    def test_should_show_input_prompts(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "Please enter the name of the car:" in captured
        assert "Please enter initial position of Test Car in x y Direction format:" in captured
        assert "Please enter the commands for Test Car:" in captured

    def test_should_add_car_given_valid_inputs(
            self, dialogue_instance, mock_input
    ):
        dialogue_instance._build_car_stage()

        assert len(dialogue_instance.field.cars) is 2

    def test_should_show_duplicate_name_error_given_car_name_already_exists(
            self, dialogue_instance, monkeypatch, capsys
    ):
        inputs = ["Used Car"]
        inputs_iter = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs_iter))

        with pytest.raises(StopIteration):
            dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "\"Used Car\" is already used. Please enter another name for the car:" in captured

    def test_should_show_invalid_position_error_given_input_does_not_match_format(
            self, dialogue_instance, monkeypatch, capsys
    ):
        inputs = ["Test Car", "invalid"]
        inputs_iter = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs_iter))

        with pytest.raises(StopIteration):
            dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "Please enter a valid position in x y Direction format (i.e \"1 2 N\"):" in captured

    def test_should_show_out_of_bounds_error_given_intiial_position_is_out_of_bounds(
            self, dialogue_instance, monkeypatch, capsys
    ):
        inputs = ["Test Car", "99 99 N"]
        inputs_iter = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs_iter))

        with pytest.raises(StopIteration):
            dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "Given position is out of bounds. Please enter a valid position in x y Direction format:" in captured

    def test_should_invalid_commands_error_given_commands_do_not_match_pattern(
            self, dialogue_instance, monkeypatch, capsys
    ):
        inputs = ["Test Car", "1 2 N", "invalid"]
        inputs_iter = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs_iter))

        with pytest.raises(StopIteration):
            dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "Please enter valid commands (valid commands are: F L R)" in captured

    def test_should_list_all_cars_added(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance.field.cars = [
            Car("Test Car 1", "1 2 N", "FLFRF"),
            Car("Test Car 2", "1 2 N", "FLFRF")
        ]

        dialogue_instance._build_car_stage()
        captured = capsys.readouterr().out

        assert "Your current list of cars are:" in captured
        assert f"- Test Car 1, (1, 2) N, FLFRF" in captured
        assert f"- Test Car 2, (1, 2) N, FLFRF" in captured
        assert f"- Test Car, (1, 2) N, FFRFFFFRRL" in captured

    def test_should_be_main_menu_stage_after_building_car(
            self, dialogue_instance, mock_input
    ):
        next_stage = dialogue_instance._build_car_stage()

        assert next_stage == "MAIN"


class TestSimulationStage:
    @pytest.fixture
    def dialogue_instance(self):
        console_dialogue = ConsoleDialogue()
        console_dialogue.field = Field(10, 10)
        console_dialogue.field.cars = [
            Car("A", "1 2 N", "FFRFFFFRRL"),
        ]

        return console_dialogue

    @pytest.fixture
    def mock_input(self, monkeypatch):
        input_value = "2"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        return input_value.split()

    def test_should_list_all_cars_added(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance._simulation_stage()
        captured = capsys.readouterr().out

        assert "Your current list of cars are:" in captured
        assert f"- A, (1, 2) N, FFRFFFFRRL" in captured

    def test_should_simulation_results_for_single_valid_car(
            self, dialogue_instance, mock_input, capsys
    ):

        dialogue_instance._simulation_stage()
        output = capsys.readouterr().out

        assert "After simulation, the result is:" in output
        assert "- A, (5, 4) S" in output

    def test_should_simulation_results_for_2_valid_cars_colliding(
            self, dialogue_instance, mock_input, capsys
    ):
        dialogue_instance.field.cars = [
            Car("A", "1 2 N", "FFRFFFFRRL"),
            Car("B", "7 8 W", "FFLFFFFFFF"),
        ]

        dialogue_instance._simulation_stage()
        output = capsys.readouterr().out

        assert "After simulation, the result is:" in output
        assert "- A, collides with B at (5, 4) at step 7" in output
        assert "- B, collides with A at (5, 4) at step 7" in output

    def test_should_be_main_stage_given_option_is_1(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "1"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        next_stage = dialogue_instance._simulation_stage()

        assert next_stage == "MAIN"

    def test_should_exit_given_option_is_not_1(
            self, dialogue_instance, monkeypatch, capsys
    ):
        input_value = "0"
        monkeypatch.setattr('builtins.input', lambda prompt: input_value)

        next_stage = dialogue_instance._simulation_stage()

        assert next_stage == "EXIT"


class TestListCars:
    @pytest.fixture
    def dialogue_instance(self):
        console_dialogue = ConsoleDialogue()
        console_dialogue.field = Field(10, 10)

        return console_dialogue

    def test_should_list_all_cars_added(
            self, dialogue_instance, capsys
    ):
        dialogue_instance.field.cars = [
            Car("A", "1 2 N", "FFRFFFFRRL"),
            Car("B", "7 8 W", "FFLFFFFFFF"),
        ]

        dialogue_instance._list_cars()
        captured = capsys.readouterr().out

        assert "Your current list of cars are:" in captured
        assert "- A, (1, 2) N, FFRFFFFRRL" in captured
        assert "- B, (7, 8) W, FFLFFFFFFF" in captured

    def test_should_print_nothing_if_no_cars_added(
            self, dialogue_instance, capsys
    ):
        dialogue_instance._list_cars()
        captured = capsys.readouterr().out

        assert captured == ""
