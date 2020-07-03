"""# Application factory and settings"""

from .settings import settings

import eventlet
import pandas as pd
from flask import Flask, Blueprint
# from flask_apscheduler import APScheduler
from flask_download_btn import DownloadBtnManager
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_worker import Manager
from werkzeug.security import generate_password_hash

import os

bp = Blueprint(
    'hemlock', 
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/hemlock/static'
)
db = SQLAlchemy()
download_btn_manager = DownloadBtnManager(db=db)
bucket = os.environ.get('BUCKET')
if bucket is not None:
    from google.cloud import storage
    gcp_client = storage.Client()
    gcp_bucket = gcp_client.get_bucket(bucket)
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
login_manager.login_message = None
# scheduler = APScheduler()
eventlet.monkey_patch(socket=True)
socketio = SocketIO(async_mode='eventlet')
manager = Manager(db=db, socketio=socketio)

def push_app_context():
    """
    Push an app context for debugging in shell or notebook.

    Returns
    -------
    app : flask.app.Flask
    """
    from ..models.private import DataStore
    app = create_app()
    app.app_context().push()
    app.test_request_context().push()
    db.create_all()
    if not DataStore.query.first():
        DataStore()
    return app

def create_app(settings=settings):
    """
    Create a Hemlock application.

    Parameters
    ----------
    settings : dict
        Default settings for the application, extensions, and models.

    Returns
    -------
    app : flask.app.Flask

    Examples
    --------
    ```python
    from hemlock.app import create_app, settings

    # MODIFY SETTINGS AS NEEDED

    app = create_app(settings)
    app.settings
    ```

    Out:

    ```
    {
    \    'clean_data': None, 
    \    'restart_option': True, 
    \    'restart_text': 'Click << to return to your in progress survey...',
    \    'screenout_csv': 'screenout.csv',
    \    'screenout_keys': [], 
    \    'screenout_text': '...you have already participated...', 
    \    'socket_js_src': 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js', 
    \    'time_expired_text': 'You have exceeded your time limit for this survey', 
    \    'time_limit': None, 
    \    'validate': True, 
    \    'DownloadBtnManager': {}, 
    \    'Manager': {
    \        'loading_img_blueprint': 'hemlock', 
    \        'loading_img_filename': 'img/worker_loading.gif'
    \    }, 
    \    'password_hash': '...'
    }
    ```
    """
    app = _create_app(settings)
    _set_bucket(app)
    _set_redis(app)
    _init_extensions(app, settings)    
    return app

def _create_app(settings):
    app = Flask(
        __name__, 
        static_folder=settings.get('static_folder'), 
        template_folder=settings.get('template_folder'),
    )
    # set password hash
    password = settings.get('password')
    settings['password_hash'] = generate_password_hash(password)
    # get screenouts
    screenout_csv = settings.get('screenout_csv')
    if os.path.exists(screenout_csv):
        df = pd.read_csv(screenout_csv)
        screenout_keys = settings.get('screenout_keys')
        df = df[screenout_keys] if screenout_keys else df
        app.screenouts = df.to_dict(orient='list')
    else:
        app.screenouts = {}
    # store configuration, settings, and blueprint
    app.config.update(settings.get('Config'))
    app.settings = settings
    app.register_blueprint(bp)
    return app

def _set_bucket(app):
    """Set up google bucket"""
    if bucket is not None:
        app.gcp_client, app.gcp_bucket = gcp_client, gcp_bucket
    else:
        app.gcp_client = app.gcp_bucket = None

def _set_redis(app):
    """Set up Redis Queue"""
    redis_url = app.config.get('REDIS_URL')
    if redis_url is not None:
        from redis import Redis
        from rq import Queue
        app.redis = Redis.from_url(redis_url)
        app.task_queue = Queue('hemlock-task-queue', connection=app.redis)
    else:
        app.redis = app.task_queue = None

def _init_extensions(app, settings):
    """Initialize application extensions"""
    db.init_app(app)
    download_btn_manager.init_app(app, **settings.get('DownloadBtnManager'))
    login_manager.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()
    socketio.init_app(app, message_queue=app.config.get('REDIS_URL'))
    manager.init_app(app, **settings.get('Manager'))