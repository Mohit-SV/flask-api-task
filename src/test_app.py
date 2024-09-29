import pytest
from src.app import app
from src.models import db, WeatherData, WeatherStats
from datetime import date

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Add some test data
        weather_data = WeatherData(station_id='TEST001', date=date(2021, 1, 1), max_temp=10.0, min_temp=5.0, precipitation=2.0)
        weather_stats = WeatherStats(station_id='TEST001', year=2021, avg_max_temp=15.0, avg_min_temp=8.0, total_precipitation=100.0)
        db.session.add(weather_data)
        db.session.add(weather_stats)
        db.session.commit()
    
    with app.test_client() as client:
        yield client
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_get_weather(client):
    response = client.get('/api/weather')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) == 1

def test_get_weather_stats(client):
    response = client.get('/api/weather/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) == 1

def test_weather_filter(client):
    response = client.get('/api/weather?station_id=TEST001')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

    response = client.get('/api/weather?station_id=NONEXISTENT')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 0

def test_weather_stats_filter(client):
    response = client.get('/api/weather/stats?year=2021')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

    response = client.get('/api/weather/stats?year=2022')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 0