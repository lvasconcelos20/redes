class Logger:
    def __init__(self, title: str, log_file=None):
        self.title = title.upper()
        self.green = "\033[92m"
        self.blue = "\033[93m"
        self.reset = "\033[0m"
        self.log_file = log_file

    def log(self, message):
        formatter_message = f"{self.blue}[LOG]{self.reset} {self.title}- {message}"
        print(formatter_message)
        if self.log_file:
            with open(self.log_file, "a") as file:
                file.write(formatter_message + "\n")

    def info(self, message):
        print(f"{self.green}[INFO]{self.reset} {self.title} - {message}")
