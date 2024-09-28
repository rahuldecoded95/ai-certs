from flask import Flask
import os
#
from utilities.logging_utilities import LoggingUtilities

app = Flask(__name__)

logging_utilities = LoggingUtilities(__name__)
logging_utilities.register_logger(logger=app.logger)

app.config["FILE_UPLOAD"] = os.path.dirname(os.path.realpath(__file__)) + "/uploads"

#
from utilities.llm_utilities import LLMUtilities
llm_utilities = LLMUtilities()
#
from resources import routes