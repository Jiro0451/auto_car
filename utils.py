import copy
from collections import defaultdict


def is_initial_pos_out_of_bound(initial_pos, width, height):
    [x, y, _] = initial_pos.split(" ")
    return _is_position_out_of_bounds((int(x), int(y)), width, height)


def get_single_car_collision(path, width, height):
    for index, position in enumerate(path):
        if _is_position_out_of_bounds(position, width, height):
            return index
    return -1


def get_max_steps(cars_data):
    max_steps = 0
    for path in cars_data.values():
        max_steps = max(max_steps, len(path))
    return max_steps


def synchronise_paths(cars_data, max_steps):
    synchronized_paths = {}

    for car, path in cars_data.items():
        path = list(path)
        if len(path) < max_steps:
            last_pos = path[-1]
            while len(path) < max_steps:
                path.append(last_pos)
        synchronized_paths[car] = path

    return synchronized_paths


def update_path_after_collision(path, collision_step):
    path_before_collision = path[:collision_step]
    collided_path = [path[collision_step]] * (len(path) - collision_step)
    return path_before_collision + collided_path


def generate_incident_reports(collisions):
    reports = {}
    for position, incidents in collisions.items():
        wrecks = []

        for cars, step in incidents:
            cars_and_wrecks = cars + wrecks[:]

            for index, car in enumerate(cars):
                cars_before = cars_and_wrecks[:index]
                cars_after = cars_and_wrecks[index + 1:]
                other_cars = cars_before + cars_after

                if not other_cars:
                    reports[car] = f"- {car}, hits the wall at {position} at step {step}"
                else:
                    reports[car] = f"- {car}, collides with {', '.join(other_cars)} at {position} at step {step}"
                wrecks.append(car)

    return reports


def generate_collisions(cars_data, max_steps, field_width, field_height):
    mutable_cars_data = copy.deepcopy(cars_data)
    collisions = defaultdict(list)

    positions_at_previous_step = defaultdict(list)
    for step_number in range(max_steps):
        positions_at_this_step = defaultdict(list)
        for car_name, path in mutable_cars_data.items():
            current_pos = path[step_number]
            positions_at_this_step[current_pos].append(car_name)

        if not positions_at_previous_step:
            positions_at_previous_step = copy.copy(positions_at_this_step)
            continue

        for position, car_names_at_pos in positions_at_this_step.items():
            if _is_position_out_of_bounds(position, field_width, field_height):
                previous_position = _find_name_in_positions(car_names_at_pos[0], positions_at_previous_step)
                collisions[previous_position].append((car_names_at_pos, step_number))
                mutable_cars_data = {
                    key: value for key, value in mutable_cars_data.items() if key not in car_names_at_pos
                }

            if position in collisions.keys() or len(car_names_at_pos) > 1:
                collisions[position].append((car_names_at_pos, step_number))
                mutable_cars_data = {
                    key: value for key, value in mutable_cars_data.items() if key not in car_names_at_pos
                }
        positions_at_previous_step = copy.copy(positions_at_this_step)

    return collisions


def _is_position_out_of_bounds(position, width, height):
    x, y = position
    return not (0 <= x < width and 0 <= y < height)


def _find_name_in_positions(name, positions):
    keys_of_position = [
        key for key, value_list in positions.items()
        if name in value_list
    ]

    if keys_of_position:
        return keys_of_position[0]

    return
