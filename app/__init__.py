from flask import Flask
import os
import sys
import logging

# Instantiate the app and set the default app path to this folder.
app = Flask(__name__, instance_relative_config=True) 

from app import views
