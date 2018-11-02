from flask import Flask
# Instantiate the app and set the default app path to this folder.
app = Flask(__name__, instance_relative_config=True) 
# Import all the views(routes) in the app.
from app import views
