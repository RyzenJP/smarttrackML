# Smart Track ML Server

Machine Learning server for predictive vehicle maintenance in the Smart Track system.

## Features

- **Predictive Maintenance**: ML model to predict vehicle maintenance needs based on mileage, usage patterns, and historical data
- **Synthetic Data Generation**: Tools to generate realistic training data
- **REST API**: HTTP server exposing ML predictions via JSON API

## Files

- `ml_server.py` / `python_ml_server.py` - Main ML server (runs on port 8080)
- `maintenance_model.pkl` - Trained Random Forest model
- `maintenance_scaler.pkl` / `scaler.pkl` - Feature scaler
- `generate_synthetic_data.py` - Generate synthetic maintenance data
- `seed_synthetic.py` - Seed database with synthetic data
- `update_mileage.py` - Update vehicle mileage in database

## Requirements

```bash
pip install flask flask-cors scikit-learn pandas numpy mysql-connector-python
```

## Configuration

Update database credentials in the Python files to match your environment:

```python
DB_CONFIG = {
    'host': 'your_host',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database'
}
```

## Running the Server

### Local Development
```bash
python ml_server.py
# or
python python_ml_server.py
```

Server will start on `http://localhost:8080`

### Production Deployment

For production, deploy this server to a cloud platform:
- **PythonAnywhere**: Free tier available
- **Heroku**: Easy Python deployment
- **AWS EC2/Lambda**: Scalable cloud hosting
- **Google Cloud Run**: Serverless container deployment

Update `config.prod.php` with your production ML server URL:
```php
define('PYTHON_ML_SERVER_URL', 'https://your-ml-server.com');
```

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Get maintenance prediction for a single vehicle
- `POST /predict_all` - Get predictions for all vehicles
- `GET /stats` - Get model training statistics

## License

Part of the Smart Track Vehicle Tracking System

