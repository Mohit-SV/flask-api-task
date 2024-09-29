"""For faster we use sqlite in memory db here"""

import unittest
from utils import setup_flask_app, init_db
from models import WeatherData, WeatherStats
from datetime import date

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = setup_flask_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.db = init_db(self.app)

        # Import and register routes
        with self.app.app_context():
            from app import get_weather, get_weather_stats
            self.app.add_url_rule('/api/weather', 'get_weather', get_weather)
            self.app.add_url_rule('/api/weather/stats', 'get_weather_stats', get_weather_stats)

            self.db.create_all()
            
            # Add some test data
            weather_data = WeatherData(station_id='TEST001', date=date(2021, 1, 1), max_temp=10.0, min_temp=5.0, precipitation=2.0)
            weather_stats = WeatherStats(station_id='TEST001', year=2021, avg_max_temp=15.0, avg_min_temp=8.0, total_precipitation=100.0)
            self.db.session.add(weather_data)
            self.db.session.add(weather_stats)
            self.db.session.commit()

        print("Available routes:")
        for rule in self.app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_get_weather(self):
        response = self.client.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('items', data)
        self.assertGreater(len(data['items']), 0)

    def test_get_weather_stats(self):
        response = self.client.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('items', data)
        self.assertGreater(len(data['items']), 0)

    def test_weather_filter(self):
        response = self.client.get('/api/weather?station_id=TEST001')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['items']), 1)

        response = self.client.get('/api/weather?station_id=NONEXISTENT')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['items']), 0)

    def test_weather_stats_filter(self):
        response = self.client.get('/api/weather/stats?year=2021')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['items']), 1)

        response = self.client.get('/api/weather/stats?year=2022')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['items']), 0)

if __name__ == '__main__':
    unittest.main()