from global_utilities import logging_utilities

class BaseResource:
    def __init__(self):
        self.logger = logging_utilities.logger