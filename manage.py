from flask_script import Manager

from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from test_app.app import app
from test_app.extensions import db

from test_app.user.models import User
from test_app.post.models import Post

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
