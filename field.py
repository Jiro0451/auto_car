from car import Car
from utils import get_max_steps, synchronise_paths, generate_collisions, generate_incident_reports, \
    get_single_car_collision


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = []

    def add_car(self, car_name, initial_pos, commands):
        self.cars.append(Car(car_name, initial_pos, commands))

    def is_car_name_used(self, name):
        names = []
        for car in self.cars:
            names.append(car.name)
        return name in names

    def get_car_details(self):
        details = []
        for car in self.cars:
            details.append(f"- {car.name}, {car.position} {car.direction}, {''.join(car.commands)}")
        return details

    def get_simulated_results(self):
        if len(self.cars) == 1:
            return self._simulate_single_car()
        return self._simulate_multiple_cars()

    def _simulate_single_car(self):
        car = self.cars[0]
        path, destination = car.get_path_and_destination()

        collision_step = get_single_car_collision(path, self.width, self.height)
        if collision_step != -1:
            return [f"- {car.name}, hits the wall at {path[collision_step]} at step {collision_step}"]

        return [f"- {car.name}, {destination}"]

    def _simulate_multiple_cars(self):
        cars_data = {}
        for car in self.cars:
            path, destination = car.get_path_and_destination()
            cars_data[car.name] = path

        max_steps = get_max_steps(cars_data)
        synced_paths = synchronise_paths(cars_data, max_steps)
        collisions = generate_collisions(synced_paths, max_steps, self.width, self.height)
        reports = generate_incident_reports(collisions)

        results = []
        for car in self.cars:
            _path, destination = car.get_path_and_destination()
            if car.name in reports.keys():
                results.append(reports[car.name])
            else:
                results.append(f"- {car.name}, {destination}")

        return results
