class ResourceNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message

class UnknownTrendError(Exception):
    def __init__(self, message: str):
        self.message = message

class MissingArgumentException(Exception):
    def __init__(self, message: str):
        self.message = message