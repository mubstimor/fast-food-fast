from flask.cli import FlaskGroup
from api import app
from api.database import DatabaseConnection

cli = FlaskGroup(app)

db = DatabaseConnection()
db.create_users_table()

# new
@cli.command()
def recreate_db():
    """ recreate database. """    
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    cli()
