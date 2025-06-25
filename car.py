class Car:
    _DIRECTIONS_ORDER = ['N', 'E', 'S', 'W']
    _MOVE_OFFSETS = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }

    def __init__(self, car_name, initial_pos, commands):
        self.name = car_name
        self.initial_position = initial_pos
        [x, y, direction] = initial_pos.split(" ")
        self.position = (int(x), int(y))
        self.direction = direction.upper()
        self.commands = list(commands.upper())
        self._INSTRUCTIONS = {
            'F': self._move_forward,
            'L': self._turn_left,
            'R': self._turn_right
        }

    def get_path_and_destination(self):
        path = [self.position]
        for command in self.commands:
            self._INSTRUCTIONS[command]()
            path.append(self.position)

        destination = f"{self.position} {self.direction}"
        self._reset_position()
        return path, destination

    def _move_forward(self):
        current_x, current_y = self.position
        delta_x, delta_y = self._MOVE_OFFSETS[self.direction]

        new_x = current_x + delta_x
        new_y = current_y + delta_y

        self.position = (new_x, new_y)

    def _turn_left(self):
        current_index = self._DIRECTIONS_ORDER.index(self.direction)
        new_index = (current_index - 1) % len(self._DIRECTIONS_ORDER)
        self.direction = self._DIRECTIONS_ORDER[new_index]

    def _turn_right(self):
        current_index = self._DIRECTIONS_ORDER.index(self.direction)
        new_index = (current_index + 1) % len(self._DIRECTIONS_ORDER)
        self.direction = self._DIRECTIONS_ORDER[new_index]

    def _reset_position(self):
        [x, y, direction] = self.initial_position.split(" ")
        self.position = (int(x), int(y))
        self.direction = direction.upper()
