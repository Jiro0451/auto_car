from console_dialogue import ConsoleDialogue


if __name__ == "__main__":
    try:
        app = ConsoleDialogue()
        app.run()
    except Exception as exception:
        print(f"Failed to process: {exception}")
