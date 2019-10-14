from flask import Flask
from .resources import api_bp

application = Flask(__name__)


# register the API views
application.register_blueprint(
    api_bp,
    url_prefix="")


# Run the main loop
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
