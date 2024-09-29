from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from typing import Dict, Any

db = SQLAlchemy()

class WeatherData(db.Model):
    """
    Represents weather data for a specific station and date.
    """
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    
    __table_args__ = (
        UniqueConstraint('station_id', 'date', name='uix_station_date'),
    )
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Convert the WeatherData object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the WeatherData object.
        """
        return {
            'id': self.id,
            'station_id': self.station_id,
            'date': self.date,
            'max_temp': self.max_temp,
            'min_temp': self.min_temp,
            'precipitation': self.precipitation
        }

class WeatherStats(db.Model):
    """
    Represents aggregated weather statistics for a specific station and year.
    """
    __tablename__ = 'weather_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float)
    avg_min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Convert the WeatherStats object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the WeatherStats object.
        """
        return {
            'id': self.id,
            'station_id': self.station_id,
            'year': self.year,
            'avg_max_temp': self.avg_max_temp,
            'avg_min_temp': self.avg_min_temp,
            'total_precipitation': self.total_precipitation
        }
