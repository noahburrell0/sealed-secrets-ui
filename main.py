import logging 
import os

from flask import Flask, Blueprint, request, send_from_directory

from modules.kubeseal import Kubeseal
from modules.ui import UI
from modules.api import API

class application:
    def __init__ (self):
        # Set envs
        self.DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
        KUBECONF_DIR = os.getenv('KUBECONF_DIR')
        DEFAULT_SCOPE = os.getenv('DEFAULT_SCOPE')
        SCOPE_TOOLTIP = os.getenv('SCOPE_TOOLTIP', None)
        BASE_PATH = os.getenv('BASE_PATH')

        # Set logging
        logLevel = logging.INFO if not self.DEBUG else logging.DEBUG
        logging.basicConfig(level=logLevel, format='[%(levelname)s] %(name)s:%(module)s %(asctime)s -- %(message)s')
        self.logger = logging.getLogger(__name__) 

        # Initialize kubeseal object
        self.ks = Kubeseal(config_dir=KUBECONF_DIR)

        # Create UI and API objects
        self.apiObj = API(self.ks)
        self.uiObj = UI(
            self.ks,
            default_scope=DEFAULT_SCOPE,
            scope_tooltip=SCOPE_TOOLTIP
        )

        # Setup Flask
        self.app = Flask(__name__)    
        self.api = Blueprint("api", __name__, url_prefix=BASE_PATH+"/api")
        self.ui = Blueprint("ui", __name__, url_prefix=BASE_PATH)


        # Define static documents route
        @self.ui.route("/static/<path:path>")
        def staticFiles(path):
            return send_from_directory('static', path)


        # Define UI Routes
        @self.ui.route("/")
        def uiIndex():
            return self.uiObj.index()


        # Define API routes
        @self.api.route("/seal/raw", methods=['POST'])
        def apiSealRaw():
            return self.apiObj.sealRaw(request)


        @self.api.route("/seal/file", methods=['POST'])
        def apiSealFile():
            return self.apiObj.sealFile(request)
        
        # Register Flask Blueprints
        self.app.register_blueprint(self.api)
        self.app.register_blueprint(self.ui)
    
    # Run Flask
    def run(self):
        self.app.run(debug=self.DEBUG, host="0.0.0.0")

# Setup for Gunicorn
app = application().app

# Run using development server
if __name__ == "__main__":
    application().run()