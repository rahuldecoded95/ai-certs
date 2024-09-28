import os
#
from global_utilities import app


if __name__ == "__main__":

    app.run(
        debug=os.environ.get("DEBUG"),
        host="0.0.0.0",
        port=os.environ.get("PORT")
    )
