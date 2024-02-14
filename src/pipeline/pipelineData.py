class PipelineData():

    def __init__(self, id):
        self.isalive = True
        self.data = None
        self.lock = id

    def set(self, data):
        self.data = data

    def get(self, key = None):
        if key and isinstance(self.data, dict):
            return self.data[key]

        return self.data

    def reset(self):
        self.data = None

    def id(self):
        return self.lock

    def kill(self):
        self.isalive = False

    def alive(self):
        return self.isalive
