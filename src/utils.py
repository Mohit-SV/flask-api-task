import logging
import os
from dotenv import load_dotenv
from flask import Flask

def setup_logger(log_file):
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Use the log_file name directly without timestamp
    log_path = os.path.join(logs_dir, log_file)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Check if logger already has handlers to avoid duplicate logging
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

def setup_flask_app():
    # Load environment variables
    load_dotenv(override=True)

    # Construct the DATABASE_URL
    DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    print(f"Constructed DATABASE_URL: {DATABASE_URL}")

    # Create and configure Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("DATABASE_URL is not set correctly")

    return app

def init_db(app):
    from models import db
    db.init_app(app)
    return db

# Example usage in other files:
# logger = setup_logger("flask_app.log")
