# Bank Customer Term Deposit Subscription Prediction (Django + scikit-learn)

## Setup
    pip install -r requirements.txt
    python ml_model/train_model.py              # demo model on synthetic data
    # OR with the real UCI "Bank Marketing" file:
    # python ml_model/train_model.py bank-full.csv
    python manage.py makemigrations predictor
    python manage.py migrate
    python manage.py runserver
Open http://127.0.0.1:8000/

## Flow
Customer form -> Random Forest pipeline (ml_model) -> probability >= 0.5 -> Subscribe / Don't subscribe.
Each prediction is saved in SQLite and visible in /admin (create a user with `createsuperuser`).

## Structure
- config/      Django settings and URLs
- predictor/   forms, views, model (Prediction), ml.py (loads the model), template
- ml_model/    train_model.py and the saved .joblib
