from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine
from config import settings

DB = SQLiteEngine(path='my_db.sqlite')

APP_REGISTRY = AppRegistry(
    apps=["piccolo_admin.piccolo_app", "api.votecatcher.piccolo_app"]
)
