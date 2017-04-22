from flask_alembic import alembic_script
from flask_script import Manager
from app import app


manager = Manager(app)

manager.add_command('db', alembic_script)

@manager.command
def hello():
    print("hello")

if __name__ == "__main__":
    manager.run()