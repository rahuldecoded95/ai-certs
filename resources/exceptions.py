from http import HTTPStatus

class Exceptions(Exception):
    def __init__(self, status_code: HTTPStatus, message: str):
        self.status_code = status_code
        self.message = message