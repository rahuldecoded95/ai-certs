import logging
import os

class LoggingUtilities:
    def __init__(self, name):
        self.logger = None
        self.logger = logging.getLogger(name)

        debug = eval(os.environ.get("DEBUG", "False"))

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(levelname)s: [%(asctime)s] [%(pathname)s:%(lineno)d] [%(module)s] %(message)s')

        # Create StreamHandler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        if not debug:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dir_path, "../logs/app.log")

            # Create File Handler
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)

    def register_logger(self, logger):
        self.logger = logger