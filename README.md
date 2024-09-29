# flask-api-task

This repository contains a Flask-based REST API for ingesting, processing, and serving weather data. The project is designed to complete a data engineering task that involves handling weather data records, performing data analysis, and exposing the results through a REST API.

## Project Overview

The main objectives of this project are:

1. Data Modeling: Design a database schema for weather data records.
2. Data Ingestion: Ingest weather data from raw text files into the database.
3. Data Analysis: Calculate yearly statistics for each weather station.
4. REST API: Create endpoints to serve the ingested and analyzed data.

## Project Components

### 1. Data Modeling

The `app/models.py` file contains the SQLAlchemy ORM models for:
- Weather records
- Weather statistics

### 2. Data Ingestion

The `app/utils.py` file includes functions for:
- Reading weather data from text files
- Inserting data into the database
- Handling duplicates
- Logging ingestion process

### 3. Data Analysis

The `app/utils.py` file also contains functions for:
- Calculating yearly statistics for each weather station
- Storing results in the database

### 4. REST API

The `app/routes.py` file defines the following endpoints:
- `/api/weather`: Get weather data records
- `/api/weather/stats`: Get calculated weather statistics

Both endpoints support filtering by date and station ID, and implement pagination.

## Setup and Running the Project

1. Clone the repository:
   ```
   git clone https://github.com/Mohit-SV/flask-api-task.git
   cd flask-api-task
   ```

2. Ensure you have Python 3.9+ installed. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
   Alternatively, you can use conda to create a new environment:
   ```
   conda create -n flask-api-task python=3.9
   conda activate flask-api-task
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the postgresql database and add the credentials:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     POSTGRES_USER=<user>
     POSTGRES_PASSWORD=<password>
     POSTGRES_DB=weather_db
     POSTGRES_HOST=<host> # "localhost" or "127.0.0.1" is default if running locally
     POSTGRES_PORT=<port> # "5432" is default if running locally
     ```

5. Load data from https://github.com/corteva/code-challenge-template into data/wx_data folder.
6. Run the data ingestion and analysis:
   ```
   python -m src/ingest.py
   python -m src/analysis.py
   ```

7. Start the Flask application server:
   ```
   python -m src/app.py
   ```

## Testing

Run the unit tests using:
```
python -m src/test_app.py
```

## API Documentation

The API documentation is available through a Swagger/OpenAPI endpoint at `/api/docs` when the server is running.

## Technologies Used

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- pytest
- Swagger/OpenAPI (flask-swagger-ui)

## File Structure

```bash
flask-api-task/
├── app/ # Main application package
│ ├── init.py # Initializes the Flask application
│ ├── models.py # Defines SQLAlchemy ORM models
│ ├── routes.py # Contains API route definitions
│ ├── schemas.py # Marshmallow schemas for serialization/deserialization
│ └── utils.py # Utility functions for data processing and analysis
├── data/ # Directory for storing data files
│ └── wx_data/ # Weather data files
│ ├── USC00110072.txt # Example weather station data file
│ ├── USC00110187.txt # Another example weather station data file
│ └── ... # Other weather station data files
├── tests/ # Directory for test files
│ ├── init.py # Initializes the test package
│ ├── test_ingestion.py # Tests for data ingestion functionality
│ ├── test_analysis.py # Tests for data analysis functionality
│ └── test_api.py # Tests for API endpoints
├── .gitignore # Specifies intentionally untracked files to ignore
├── config.py # Configuration settings for the application
├── requirements.txt # List of Python package dependencies
├── run.py # Script to run the Flask application
└── README.md # Project documentation and instructions
```

## Extra Credit - Deployment

For the extra credit deployment approach using AWS services, please refer to the [extra_credit_answer.md](extra_credit_answer.md) file in the root directory of this project. This file contains a detailed explanation of:

- AWS services and tools to be used
- A step-by-step deployment approach
- Security considerations
- Scaling and optimization strategies

If needed, since I don't have access to AWS, I can replicate the similar setup using:
- **Airflow**: For scheduling weather data ingestion tasks.
- **Docker** & **Docker Compose**: For containerizing the application and managing services locally.
- **Minikube**: For local Kubernetes deployment.
- **GitHub Actions**: For automating the CI/CD pipeline.
- **DockerHub**: For storing and sharing Docker images.