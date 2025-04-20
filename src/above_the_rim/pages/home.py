"""
Blueprint: home_route. Содержит логику рендера home
"""

from flask import Blueprint, render_template

home_route = Blueprint('home_page', __name__)

@home_route.route('/')
def home_page():
    return render_template('home.html')