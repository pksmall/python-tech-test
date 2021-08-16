import os

from flask_babel import Babel, _
from flask_cors import CORS
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_restx import Api
from hashids import Hashids
from werkzeug.middleware.proxy_fix import ProxyFix

from project.api.shorturl import shorturl_namespace as ns_shorturl
from project.tools import init_db

load_dotenv()

app_dev = os.environ.get('APPDEV')
app = Flask(__name__, subdomain_matching=True)
#app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', "my.site")
app.secret_key = "asdjFsnD-jdkeiwo1gku314hgbfq5atwshwaulfoSDksdke5xqwaEWULGPJHK;HGJctw6yed"
app.config['ERROR_404_HELP'] = False

app.config['hashids'] = Hashids(min_length=8, salt=app.secret_key)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

babel = Babel(app)

blueprint = Blueprint('api', __name__, url_prefix='/')

api = Api(blueprint, version='0.1', title=_('ShortURL API'),
          description=_('ShortURL API.'),
          doc='/doc/')

api.add_namespace(ns_shorturl)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(blueprint)


if __name__ == '__main__':
  if not os.path.isfile('../database.db'):
    init_db()
  app.run(debug=True, port=5002)
