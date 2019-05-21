from flask_script import Manager
from gevent import spawn
from core import data
import settings

def command_manager(app):
    manager = Manager(app, with_default_commands=None)

    @manager.command
    def start():
        try:
            app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, threaded=False, processes=settings.NUM_WORKERS)
        except KeyboardInterrupt:
            pass
    return manager