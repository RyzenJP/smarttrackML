# Smart Track ML Server

Machine Learning server for predictive vehicle maintenance in the Smart Track system.

## Features

- **Predictive Maintenance**: ML model to predict vehicle maintenance needs based on mileage, usage patterns, and historical data
- **Synthetic Data Generation**: Tools to generate realistic training data
- **REST API**: Flask-based REST API exposing ML predictions via JSON API
- **Heroku Ready**: Pre-configured for easy Heroku deployment

## Files

- `ml_server.py` - Main Flask ML server
- `maintenance_model.pkl` - Trained XGBoost model
- `maintenance_scaler.pkl` - Feature scaler
- `Procfile` - Heroku process file
- `runtime.txt` - Python version for Heroku
- `generate_synthetic_data.py` - Generate synthetic maintenance data
- `seed_synthetic.py` - Seed database with synthetic data
- `update_mileage.py` - Update vehicle mileage in database

## Requirements

```bash
pip install -r requirements.txt
```

## Configuration

The server uses environment variables for database configuration:

```bash
DB_HOST=your_host
DB_USER=your_user
DB_PASS=your_password
DB_NAME=trackingv2
PORT=8080  # Optional, defaults to 8080
```

## Running the Server

### Local Development

```bash
python ml_server.py
```

Server will start on `http://localhost:8080`

### Production with Gunicorn

```bash
gunicorn ml_server:app
```

### Heroku Deployment

1. **Install Heroku CLI** (if not already installed):
   ```bash
   # Visit https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set DB_HOST=your_host
   heroku config:set DB_USER=your_user
   heroku config:set DB_PASS=your_password
   heroku config:set DB_NAME=trackingv2
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **View logs**:
   ```bash
   heroku logs --tail
   ```

The app will be available at `https://your-app-name.herokuapp.com`

**Note**: Heroku provides a free MySQL addon (JawsDB MySQL) or you can use an external MySQL database.

### Other Cloud Platforms

- **PythonAnywhere**: Free tier available
- **AWS EC2/Lambda**: Scalable cloud hosting
- **Google Cloud Run**: Serverless container deployment

Update your frontend `config.prod.php` with your production ML server URL:
```php
define('PYTHON_ML_SERVER_URL', 'https://your-app-name.herokuapp.com');
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /status` - Get server and model status
- `GET /predict_all` - Get predictions for all vehicles
- `GET /predict?vehicle_id=1` - Get maintenance prediction for a single vehicle
- `GET /stats` - Get model training statistics
- `POST /train` - Retrain the ML model

## License

Part of the Smart Track Vehicle Tracking System


