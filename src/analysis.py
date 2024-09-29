from dotenv import load_dotenv
from utils import setup_logger, setup_flask_app, init_db
from models import WeatherData, WeatherStats
from sqlalchemy import func, extract, case
from sqlalchemy_utils import database_exists, create_database
from typing import List, Tuple

# Load environment variables
load_dotenv(override=True)

# Setup logger
logger = setup_logger("weather_analysis.log")

# Create and configure Flask app
app = setup_flask_app()
db = init_db(app)


def create_weather_stats_table() -> None:
    """
    Create the weather_stats table if it doesn't exist.
    This function ensures that the necessary table for storing weather
    statistics is available.
    """
    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            logger.info(f"Created database: {db.engine.url}")

        WeatherStats.__table__.create(db.engine, checkfirst=True)
        logger.info("WeatherStats table created (if it didn't exist)")


def calculate_annual_stats() -> None:
    """
    Calculate annual weather statistics for each station and year.

    This function computes the average maximum temperature, average
    minimum temperature, and total precipitation for each weather
    station and year. The results are stored in the WeatherStats table.
    If a statistic cannot be calculated, NULL is used.

    The function uses SQLAlchemy's functionality to perform efficient
    database operations.
    """
    create_weather_stats_table()

    with app.app_context():
        logger.info("Starting annual statistics calculation")

        stats: List[Tuple] = (
            db.session.query(
                WeatherData.station_id,
                extract("year", WeatherData.date).label("year"),
                func.avg(
                    case(
                        (
                            WeatherData.max_temp.isnot(None),
                            WeatherData.max_temp,
                        )
                    )
                ).label("avg_max_temp"),
                func.avg(
                    case(
                        (
                            WeatherData.min_temp.isnot(None),
                            WeatherData.min_temp,
                        )
                    )
                ).label("avg_min_temp"),
                func.sum(
                    case(
                        (
                            WeatherData.precipitation.isnot(None),
                            WeatherData.precipitation,
                        )
                    )
                ).label("total_precipitation"),
            )
            .group_by(
                WeatherData.station_id, extract("year", WeatherData.date)
            )
            .all()
        )

        logger.info(
            f"Calculated statistics for {len(stats)} station-year combinations"
        )

        for stat in stats:
            weather_stat = WeatherStats(
                station_id=stat.station_id,
                year=int(stat.year),
                avg_max_temp=stat.avg_max_temp,
                avg_min_temp=stat.avg_min_temp,
                total_precipitation=stat.total_precipitation,
            )
            db.session.merge(weather_stat)

        db.session.commit()
        logger.info(
            "Annual statistics calculation completed and stored "
            "in database"
        )


if __name__ == "__main__":
    calculate_annual_stats()
