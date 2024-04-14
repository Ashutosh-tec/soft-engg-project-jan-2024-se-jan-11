from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from application.config import LocalDevelopmentConfig
from application.models import db
# from application.models import User, Role
from application import workers
# from flask_caching import Cache
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv
import os

app = None
api = None
celery = None
# cache = None

def create_app(conf=LocalDevelopmentConfig, discourse_api_username=None, discourse_api_key=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(conf)
    app.config['DISCOURSE_API_USERNAME'] = discourse_api_username
    app.config['DISCOURSE_API_KEY'] = discourse_api_key

    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    db.create_all()  
    app.app_context().push() 
    api = Api(app)
    app.app_context().push() 
    CORS(app, resources={r'/*':{'origins':'*'}}) 
    app.app_context().push()    
    # Create celery
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config['CELERY_BROKER_URL'],
        result_backend = app.config['CELERY_RESULT_BACKEND']
    )
    celery.Task = workers.ContextTask
    app.app_context().push() 

    # cache = Cache(app)
    # cache.clear()
    # app.app_context().push() 

    return app,api,celery

app,api,celery = create_app(discourse_api_username='22f1000948', discourse_api_key=os.getenv("DISCOURSE_API_KEY"))

# Initialize Algolia search client, Replace with your own Algolia credentials instead of LocalDevelopmentConfig.SEARCH_API_KEY
client = SearchClient.create("C37H2BH94X", "7ba7215d84745d2397e19ebbefb9c49a")
index = client.init_index('sociogrammers_app')
