from flask import Blueprint, request
import main

routes = Blueprint('routes', __name__)

@routes.route('/scrape', methods=['POST'])
def scrapeUrl():
    
    data = request.get_json()
    result = main.scrape(data)

    return result