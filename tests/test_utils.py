from collections import defaultdict

import pytest

from utils import get_max_steps, synchronise_paths, generate_collisions, update_path_after_collision, \
    generate_incident_reports, is_initial_pos_out_of_bound, _find_name_in_positions, _is_position_out_of_bounds, \
    get_single_car_collision

mock_car_paths_A = {
    'A': [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)],
    'B': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)],
    'C': [(10, 10), (9, 9), (8, 8), (7, 7), (6, 6), (5, 5), (5, 4)]
}

mock_car_paths_B = {
    'Drumstick': [(3, 2), (3, 2), (4, 2), (5, 2), (5, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 2), (2, 1)],
    'Chicken': [(4, 4), (4, 4), (5, 4), (6, 4), (6, 4), (6, 5), (6, 6), (6, 6), (5, 6), (4, 6), (4, 6)],
}

mock_car_paths_C = {
    'Drumstick': [(9, 9), (9, 10), (9, 11)],
    'Chicken': [(7, 9), (8, 9), (9, 9)],
}

collision_paths = [
    {'name': 'A',
     'path': [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0), (2, 0), (3, 0), (4, 0)]},
    {'name': 'B',
     'path': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)]},
    {'name': 'C',
     'path': [(2, 0)]}
]


class TestIsValidInitialPos:
    @pytest.mark.parametrize(
        "initial_pos, width, height", [
            ("1 2 N", 10, 10),
            ("0 0 N", 10, 10),
            ("9 9 N", 10, 10),
        ])
    def test_should_return_false_given_position_in_bound(
            self, initial_pos, width, height
    ):
        result = is_initial_pos_out_of_bound(initial_pos, width, height)

        assert result is False

    @pytest.mark.parametrize(
        "initial_pos, width, height", [
            ("1 10 N", 10, 10),
            ("10 1 N", 10, 10),
            ("10 10 N", 10, 10),
        ])
    def test_should_return_true_given_position_out_of_bound(
            self, initial_pos, width, height
    ):
        result = is_initial_pos_out_of_bound(initial_pos, width, height)

        assert result is True


class TestGetSingleCarCollision:
    @pytest.mark.parametrize(
        "expected_step, path", [
            (7, [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)]),
            (8, [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 4), (4, 5), (5, 5), (5, 4)]),
            (4, [(3, 4), (2, 4), (1, 4), (0, 4), (-1, 4), (0, 4)]),
            (3, [(4, 2), (4, 1), (4, 0), (4, -1), (4, 0), (4, 1), (4, 2)]),
        ]
    )
    def test_should_return_step_given_collision_exists(self, expected_step, path):
        result = get_single_car_collision(path, 5, 5)
        assert result == expected_step

    def test_should_return_minus_one_given_no_collisions(self):
        path = [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)]
        result = get_single_car_collision(path, 10, 10)
        assert result == -1


class TestGetMaxSteps:
    @pytest.mark.parametrize(
        "car_paths", [
            mock_car_paths_A,
            mock_car_paths_B
        ])
    def test_should_return_max_steps_given_paths_of_varying_lengths(self, car_paths):
        result = get_max_steps(car_paths)
        assert result == 11

    def test_should_return_0_given_no_car_paths(self):
        result = get_max_steps({})
        assert result == 0


class TestSynchronisePaths:
    @pytest.mark.parametrize(
        "car_paths, expected_paths", [
            (mock_car_paths_A,
             {
                 'A': [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)],
                 'B': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 4)],
                 'C': [(10, 10), (9, 9), (8, 8), (7, 7), (6, 6), (5, 5), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4)]
             }),
            (mock_car_paths_B,
             mock_car_paths_B)
        ])
    def test_should_return_synchronised_paths_given_paths_of_varying_lengths(self, car_paths, expected_paths):
        result = synchronise_paths(car_paths, 11)
        assert result == expected_paths

    def test_should_return_empty_dictionary_given_no_paths(self):
        result = synchronise_paths({}, 0)
        assert result == {}


class TestUpdatePathAfterCollision:
    def test_should_update_path_after_collision(self):
        path = [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 4), (5, 4), (5, 4)]

        result = update_path_after_collision(path, 4)

        expected_path = [(1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4)]
        assert result == expected_path


class TestGetCollisionReport:
    def test_should_get_collision_report_given_collision_data(self):
        collisions = defaultdict(list)
        collisions[(1, 1)].append([['A', 'B'], 5])
        collisions[(1, 1)].append([['C', 'D'], 7])
        collisions[(2, 2)].append([['E', 'F'], 9])
        collisions[(2, 2)].append([['G'], 11])

        result = generate_incident_reports(collisions)

        assert "- A, collides with B at (1, 1) at step 5" in result['A']
        assert "- B, collides with A at (1, 1) at step 5" in result['B']
        assert "- C, collides with D, A, B at (1, 1) at step 7" in result['C']
        assert "- D, collides with C, A, B at (1, 1) at step 7" in result['D']
        assert "- E, collides with F at (2, 2) at step 9" in result['E']
        assert "- F, collides with E at (2, 2) at step 9" in result['F']
        assert "- G, collides with E, F at (2, 2) at step 11" in result['G']
        return

    def test_should_get_collision_report_given_collision_data_with_cars_touching_wall(self):
        collisions = defaultdict(list)
        collisions[(9, 9)].append((['Drumstick'], 1))
        collisions[(9, 9)].append((['Chicken'], 2))

        result = generate_incident_reports(collisions)

        assert "- Drumstick, hits the wall at (9, 9) at step 1" in result['Drumstick']
        assert "- Chicken, collides with Drumstick at (9, 9) at step 2" in result['Chicken']

    def test_should_return_empty_dictionary_given_no_collision_data(self):
        result = generate_incident_reports({})
        assert result == {}


class TestGenerateCollision:
    def test_should_generate_collisions_data_given_collisions_exists(self):
        max_steps = get_max_steps(mock_car_paths_A)
        cars_data = synchronise_paths(mock_car_paths_A, max_steps)
        collisions = generate_collisions(cars_data, max_steps, 10, 10)

        assert (5, 4) in collisions.keys()
        assert (['A', 'C'], 7) in collisions[(5, 4)]
        assert (['B'], 9) in collisions[(5, 4)]

    def test_should_generate_collisions_data_given_collisions_to_the_wall_exists(self):
        max_steps = get_max_steps(mock_car_paths_C)
        cars_data = synchronise_paths(mock_car_paths_C, max_steps)
        collisions = generate_collisions(cars_data, max_steps, 10, 10)

        assert (9, 9) in collisions.keys()
        assert (['Drumstick'], 1) in collisions[(9, 9)]
        assert (['Chicken'], 2) in collisions[(9, 9)]

    def test_should_empty_dictionary_given_no_collisions(self):
        max_steps = get_max_steps(mock_car_paths_B)
        cars_data = synchronise_paths(mock_car_paths_B, max_steps)
        collisions = generate_collisions(cars_data, max_steps, 10, 10)

        assert not collisions.keys()


class TestIsCarTouchingWall:
    @pytest.mark.parametrize(
        "position, width, height", [
            ((0, 10), 10, 10),
            ((0, -1), 10, 10),
            ((10, 0), 10, 10),
            ((-1, 0), 10, 10),
        ]
    )
    def test_should_return_true_given_car_out_of_bounds(
            self, position, width, height
    ):
        result = _is_position_out_of_bounds(position, width, height)
        assert result is True

    def test_should_return_false_given_car_within_bounds(self):
        result = _is_position_out_of_bounds((5, 5), 10, 10)
        assert result is False


class TestFindNameInPositions:
    def test_should_return_position_given_name_in_positions(self):
        positions = defaultdict(list)
        positions[(1, 1)].append("Chicken")
        positions[(1, 1)].append("Drumstick")

        result = _find_name_in_positions("Drumstick", positions)
        assert result == (1, 1)

    def test_should_none_given_name_not_found(self):
        positions = defaultdict(list)
        positions[(1, 1)].append("Chicken")
        positions[(1, 1)].append("Drumstick")

        result = _find_name_in_positions("Coconut", positions)
        assert not result
