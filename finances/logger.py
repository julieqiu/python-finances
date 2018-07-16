class Logger:

    def __init__(self, name: str):
        self.name = name

    def info(self, log: str):
        print('[{}] {}'.format(self.name, log))
