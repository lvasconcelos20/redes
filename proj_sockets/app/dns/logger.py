class Logger:
    def __init__(self, title: str):
        self.title = title.upper()
        self.green = "\033[92m"
        self.blue = "\033[93m"
        self.reset = "\033[0m"

    def log(self, message):
        formatted_message = f"{self.title} [LOG] {message}"
        print(formatted_message)

    def info(self, message):
        formatted_message = f"{self.title} [INFO] {message}"
        print(formatted_message)
