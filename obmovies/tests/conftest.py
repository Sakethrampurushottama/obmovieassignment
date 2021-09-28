import pytest
from obmovies.factory import create_app

import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))


@pytest.fixture
def app():
    app = create_app()
    app.config['SECRET_KEY'] = config['TEST']['SECRET_KEY']
    app.config['MOVIES_NS'] = config['PROD']['MOVIES_NS']
    app.config['MOVIES_DB_URI'] = config['TEST']['MOVIES_DB_URI']
    return app
