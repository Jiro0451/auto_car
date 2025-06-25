from console_dialogue import ConsoleDialogue


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height


if __name__ == "__main__":
    try:
        app = ConsoleDialogue()
        app.run()
    except Exception as exception:
        print(f"Failed to process: {exception}")
