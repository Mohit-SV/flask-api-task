import os
import csv
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from utils import setup_logger, setup_flask_app, init_db
from models import WeatherData
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.dialects.postgresql import insert
import time

# Load environment variables
load_dotenv(override=True)

# Setup logger
logger = setup_logger("weather_ingestion.log")

# Create and configure Flask app
app = setup_flask_app()
db = init_db(app)

def create_db_if_not_exists() -> None:
    """
    Create the database and weather_data table if they don't exist.
    """
    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            logger.info(f"Created database: {db.engine.url}")
        
        WeatherData.__table__.create(db.engine, checkfirst=True)
        logger.info("WeatherData table created (if it didn't exist)")

def ingest_weather_data(data_dir='data/wx_data/') -> None:
    """
    Ingest weather data from CSV files into the database.
    """
    create_db_if_not_exists()
    
    data_dir = os.path.join('data', 'wx_data')
    files: List[str] = os.listdir(data_dir)
    
    start_time = time.time()
    logger.info(f"Starting data ingestion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Found {len(files)} weather files to process")
    
    total_records = 0
    total_new_records = 0
    
    with app.app_context():
        for file in files:
            logger.info(f"Processing file: {file}")
            new_records = 0
            with open(os.path.join(data_dir, file), 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    try:
                        date = datetime.strptime(row[0], '%Y%m%d')
                        max_temp = float(row[1]) / 10 if row[1] != '-9999' else None
                        min_temp = float(row[2]) / 10 if row[2] != '-9999' else None
                        precipitation = float(row[3]) / 10 if row[3] != '-9999' else None
                        
                        stmt = insert(WeatherData).values(
                            station_id=file.split('.')[0],
                            date=date,
                            max_temp=max_temp,
                            min_temp=min_temp,
                            precipitation=precipitation
                        )
                        
                        stmt = stmt.on_conflict_do_nothing(
                            index_elements=['station_id', 'date']
                        )
                        
                        result = db.session.execute(stmt)
                        if result.rowcount > 0:
                            new_records += 1
                        
                        total_records += 1
                    except ValueError as e:
                        logger.error(f"Error converting data in row {row} in file {file}: {e}")
                    except Exception as e:
                        logger.error(f"Unexpected error processing row {row} in file {file}: {e}")
            
            try:
                db.session.commit()
                total_new_records += new_records
                logger.info(f"Successfully ingested file: {file}. New records: {new_records}")
            except IntegrityError:
                db.session.rollback()
                logger.error(f"Failed to commit data for file: {file}")
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Data ingestion completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Total duration: {duration:.2f} seconds")
    logger.info(f"Total records processed: {total_records}")
    logger.info(f"Total new records inserted: {total_new_records}")

if __name__ == "__main__":
    ingest_weather_data()
