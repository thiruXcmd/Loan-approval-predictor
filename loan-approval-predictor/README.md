# Loan Approval Prediction System

A machine learning-powered web application that predicts loan approval decisions based on borrower information.

## Features

- **Machine Learning Model**: Random Forest classifier with 96% accuracy
- **Interactive Web Interface**: Clean, responsive form for loan applications
- **Real-time Predictions**: Instant approval/rejection predictions with confidence scores
- **Professional UI**: Bootstrap-based dark theme design
- **Form Validation**: Client-side and server-side validation
- **Database Storage**: SQLAlchemy for storing prediction history

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: Bootstrap 5, JavaScript, HTML/CSS
- **Database**: SQLite (default) or PostgreSQL

## Installation

1. **Clone or extract the project files**

2. **Install Python dependencies**:
   ```bash
   pip install flask flask-sqlalchemy scikit-learn pandas numpy joblib gunicorn werkzeug email-validator psycopg2-binary sqlalchemy
   ```

3. **Set environment variables** (optional):
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///loan_app.db"  # or PostgreSQL URL
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access the app**: Open http://localhost:5000 in your browser

## Project Structure

```
loan_approval_system/
├── app.py              # Flask app configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and handlers
├── ml_model.py         # Machine learning model class
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   └── prediction.html
├── static/             # CSS and JavaScript
│   ├── style.css
│   └── script.js
└── README.md          # This file
```

## How It Works

1. **Data**: The system uses a sample dataset of 1000 loan records with realistic borrower profiles
2. **Model**: Random Forest classifier trained on features like income, credit history, education, etc.
3. **Prediction**: Users fill out a form with their details and get instant approval predictions
4. **Results**: Shows approval/rejection with confidence percentage and key factors analysis

## Model Features

The ML model considers these factors:
- Applicant and co-applicant income
- Loan amount and term
- Credit history
- Education level
- Employment status
- Property area
- Marital status and dependents

## Usage

1. Fill out the loan application form with your details
2. Click "Predict Loan Approval"
3. View your prediction result with confidence score
4. See analysis of key factors affecting your application

## Development

To modify or extend the system:

- **Model**: Edit `ml_model.py` to change ML algorithms or features
- **Routes**: Modify `routes.py` for new endpoints
- **UI**: Update templates and static files for interface changes
- **Database**: Add new models in `models.py`

## Production Deployment

For production use:
1. Set strong SESSION_SECRET environment variable
2. Use PostgreSQL instead of SQLite
3. Configure proper logging
4. Use gunicorn with multiple workers
5. Set up reverse proxy (nginx)

## License

This project is for educatinal purposes only and done in my free time.