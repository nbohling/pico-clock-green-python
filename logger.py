import io

class Logger:
    def __init__(self):
        self.out = open('log.txt', 'a')

    def log(self, message):
        self.out.write(message + "\n")

    def print(self, message):
        self.log(message)
