import re

from field import Field
from utils import is_initial_pos_out_of_bound


class ConsoleDialogue:
    def __init__(self):
        self.field = None
        self.current_stage = "WELCOME"
        self.stages = {
            "WELCOME": self._welcome_stage,
            "MAIN": self._main_menu_stage,
            "BUILD_CAR": self._build_car_stage,
            "SIMULATION": self._simulation_stage,
            "EXIT": self._exit_stage
        }

    def run(self):
        while self.current_stage != "EXIT_PROGRAM":
            if self.current_stage in self.stages:
                next_stage = self.stages[self.current_stage]()
                if next_stage:
                    self.current_stage = next_stage
            else:
                print("Error: Unknown stage.")
                break

    def _welcome_stage(self):
        print("Welcome to Auto Driving Car Simulation!\n\n"
              "Please enter the width and height of the simulation field in x y format:")

        while True:
            user_input = input("")
            if re.match(r"^\d+ \d+$", user_input):
                break

            print("\nPlease enter a valid width and height in x y format (i.e. \"10 10\"):")

        dimensions = user_input.split()
        self.field = Field(int(dimensions[0]), int(dimensions[1]))
        print(f"\nYou have created a field of {self.field.width} x {self.field.height}.")

        return "MAIN"

    def _main_menu_stage(self):
        while True:
            print("\nPlease choose from the following options:\n"
                  "[1] Add a car to field\n"
                  "[2] Run simulation")
            option = input("")

            if option == "1":
                return "BUILD_CAR"
            elif option == "2":
                if not self.field.cars:
                    print("Unable to run simulation. There are no cars currently.")
                    continue
                return "SIMULATION"
            elif option == "0":
                return "EXIT"
            else:
                print(f"\"{option}\" is not a valid option")

    def _build_car_stage(self):
        print("\nPlease enter the name of the car:")
        while True:
            car_name = input("")
            if self.field.is_car_name_used(car_name) is False:
                break
            print(f"\"{car_name}\" is already used. Please enter another name for the car:")

        print(f"\nPlease enter initial position of {car_name} in x y Direction format:")
        while True:
            initial_pos = input("")
            if not re.match(r"^\d+ \d+ [nsewNSEW]$", initial_pos):
                print("Please enter a valid position in x y Direction format (i.e \"1 2 N\"):")
                continue
            if is_initial_pos_out_of_bound(initial_pos, self.field.width, self.field.height):
                print("Given position is out of bounds. Please enter a valid position in x y Direction format:")
                continue
            break

        print(f"Please enter the commands for {car_name}:")
        while True:
            commands = input("")
            if re.match(r"^[flrFLR]*$", commands):
                break
            print("Please enter valid commands (valid commands are: F L R)")

        self.field.add_car(car_name, initial_pos, commands)
        self._list_cars()
        return "MAIN"

    def _simulation_stage(self):
        self._list_cars()
        print("\nAfter simulation, the result is:")

        for line in self.field.get_simulated_results():
            print(line)

        print("\nPlease choose from the following options:\n"
              "[1] Start over\n"
              "[2] Exit")
        option = input("")

        if option == "1":
            self._list_cars()
            return "MAIN"
        return "EXIT"

    @staticmethod
    def _exit_stage():
        print("\nThanks for using Auto Driving Car Simulation!\n\nBye!")

        return "EXIT_PROGRAM"

    def _list_cars(self):
        car_details = self.field.get_car_details()

        if not car_details:
            return

        print("\nYour current list of cars are:")
        for car in car_details:
            print(car)
