from flask import Flask, render_template
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
import click

from .models import db, User, Talk, Vote
from .v1_resources import api_bp
from .config import Config
from .admin import AuthModelView
from .commands import (
    load_talks_command, createsuperuser_command)
from . import views


application = Flask(__name__)
application.config.from_object(Config)

# ...# initialize and create the database
db.init_app(application)
migrate = Migrate(application, db)


@application.cli.command()
@click.option(
    '--file', '-f', type=str, default='data/talks_db_dump.csv',
    help='csv file containing talks.')
def load_talks(file):
    click.echo('\n Loading Talks File: {}'.format(file))
    load_talks_command(file)


@application.cli.command()
@click.argument('name', nargs=1)
@click.argument('password', nargs=1)
def createsuperuser(name, password):
    click.echo('\n create superuser: {}'.format(name))
    createsuperuser_command(name, password)


# Register models with the Admin
admin = Admin(application, name='flask4data', template_mode='bootstrap3')
admin.add_view(AuthModelView(User, db.session))
admin.add_view(AuthModelView(Talk, db.session))
admin.add_view(AuthModelView(Vote, db.session))

# Instantiate the Flask Login manager
login = LoginManager(application)
login.login_view = 'login'


# Define function to map id to user for Flask Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Create a custome 404 page
@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# register the auth views
application.add_url_rule(r'/login/', view_func=views.login, methods=['GET', 'POST'])
application.add_url_rule(r'/logout/', view_func=views.logout, methods=['GET', 'POST'])
application.add_url_rule(r'/', view_func=views.index, methods=['GET', 'POST'])

# register the API views
application.register_blueprint(
    api_bp,
    url_prefix="/api/v1")

# set up flask konch (beefed up flask shell)
application.config.update({
    'KONCH_CONTEXT': {
        'db': db,
        'User': User,
        'Talk': Talk,
        'Vote': Vote,
    }
})

# Run the main loop
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
