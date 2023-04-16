from flask import Blueprint, jsonify, request
from ..database.database import client
from .scraper import scrape_data

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def home():
    return 'Welcome to the Product Search Engine!'

@bp.route('/search', methods=['POST'])
def search():
    category = request.json['category']
    site = request.json['site']
    query = request.json['query']

    # Scrape data from websites
    data = scrape_data(category, site, query)

    # Store data in database
    # ...

    return jsonify(data)
