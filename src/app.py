from flask import jsonify, request, Response
from flasgger import Swagger
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any

from utils import setup_logger, setup_flask_app, init_db
from models import WeatherData, WeatherStats

# Load environment variables from .env file
load_dotenv(override=True)

# Setup logger for the Flask application
logger = setup_logger("flask_app.log")

# Initialize Flask app and database
app = setup_flask_app()
db = init_db(app)
swagger = Swagger(app)


def create_tables():
    """
    Create database and tables if they don't exist.
    This function is called when the app starts to ensure the database
    is set up.
    """
    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            logger.info(f"Created database: {db.engine.url}")
        db.create_all()
        logger.info("Database tables created (if they didn't exist)")


create_tables()


@app.after_request
def after_request(response: Response) -> Response:
    """
    Log details of each request after it's processed.
    This helps in monitoring and debugging the application.
    """
    timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    logger.info(
        f'{request.remote_addr} - - [{timestamp}]'
        f'"{request.method} {request.full_path} HTTP/1.1" '
        f"{response.status_code} -"
    )
    return response


def paginate(query, page: int, per_page: int) -> Dict[str, Any]:
    """
    Paginate the query results.

    Args:
        query: SQLAlchemy query object
        page: Current page number
        per_page: Number of items per page

    Returns:
        Dict containing paginated results and metadata
    """
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": [item.as_dict() for item in paginated.items],
        "total": paginated.total,
        "page": page,
        "per_page": per_page,
        "pages": paginated.pages,
    }


@app.route("/api/weather", methods=["GET"])
def get_weather():
    """
    Endpoint returning the weather data
    ---
    parameters:
      - name: station_id
        in: query
        type: string
        required: false
      - name: date
        in: query
        type: string
        required: false
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 20
    responses:
      200:
        description: Weather data retrieved successfully
      500:
        description: Internal server error
    """
    try:
        logger.info("Fetching weather data")

        station_id = request.args.get("station_id")
        date = request.args.get("date")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = WeatherData.query

        if station_id:
            query = query.filter_by(station_id=station_id)
        if date:
            query = query.filter_by(date=date)

        return jsonify(paginate(query, page, per_page))
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/weather/stats", methods=["GET"])
def get_weather_stats():
    """
    Endpoint returning the weather statistics
    ---
    parameters:
      - name: year
        in: query
        type: integer
        required: false
      - name: station_id
        in: query
        type: string
        required: false
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 20
    responses:
      200:
        description: Weather stats retrieved successfully
      500:
        description: Internal server error
    """
    try:
        logger.info("Fetching weather statistics")

        year = request.args.get("year", type=int)
        station_id = request.args.get("station_id")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = WeatherStats.query

        if year:
            query = query.filter_by(year=year)
        if station_id:
            query = query.filter_by(station_id=station_id)

        return jsonify(paginate(query, page, per_page))
    except Exception as e:
        logger.error(f"Error fetching weather stats: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)
