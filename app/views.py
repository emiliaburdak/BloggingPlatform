from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask.flask4.app.template.models import Note, Hashtag
from flask.flask4.app.template import db
import json
from datetime import datetime

views = Blueprint('views', __name__)