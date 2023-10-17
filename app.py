from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import configparser
import os
import dash

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME, suppress_callback_exceptions=True)

app.scripts.config.serve_locally = True
server = app.server