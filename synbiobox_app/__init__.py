from flask import Flask

#CREATE DATABASE `test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci

app = Flask(__name__)

from .main import views
