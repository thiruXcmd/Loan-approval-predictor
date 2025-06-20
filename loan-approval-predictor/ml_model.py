import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import logging

class LoanApprovalModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 
            'Loan_Amount_Term', 'Credit_History', 'Property_Area'
        ]
        self.categorical_columns = [
            'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area'
        ]
        self.model_metrics = {}
        
    def create_sample_dataset(self):
        np.random.seed(42)
        n_samples = 1000

        genders = np.random.choice(['Male', 'Female'], n_samples, p=[0.8, 0.2])
        married = np.random.choice(['Yes', 'No'], n_samples, p=[0.7, 0.3])
        dependents = np.random.choice(['0', '1', '2', '3+'], n_samples, p=[0.4, 0.3, 0.2, 0.1])
        education = np.random.choice(['Graduate', 'Not Graduate'], n_samples, p=[0.75, 0.25])
        self_employed = np.random.choice(['Yes', 'No'], n_samples, p=[0.15, 0.85])
        property_area = np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples, p=[0.4, 0.4, 0.2])

        applicant_income = np.random.lognormal(mean=10, sigma=0.8, size=n_samples)
        coapplicant_income = np.random.lognormal(mean=8, sigma=1.2, size=n_samples) * (married == 'Yes').astype(int)
        loan_amount = np.random.lognormal(mean=5, sigma=0.6, size=n_samples)
        loan_amount_term = np.random.choice([6, 12, 24, 48], n_samples, p=[0.25, 0.35, 0.25, 0.15])

        credit_history = np.random.choice([0, 1], n_samples, p=[0.15, 0.85])

        income_ratio = loan_amount / (applicant_income + coapplicant_income)
        approval_prob = (
            0.3 * (credit_history == 1) +
            0.25 * (education == 'Graduate') +
            0.2 * (income_ratio < 0.3) +
            0.15 * (applicant_income > 5000) +
            0.1 * (property_area == 'Urban')
        )
        approval_prob += np.random.normal(0, 0.1, n_samples)
        loan_status = (approval_prob > 0.5).astype(int)

        data = pd.DataFrame({
            'Gender': genders,
            'Married': married,
            'Dependents': dependents,
            'Education': education,
            'Self_Employed': self_employed,
            'ApplicantIncome': applicant_income,
            'CoapplicantIncome': coapplicant_income,
            'LoanAmount': loan_amount,
            'Loan_Amount_Term': loan_amount_term,
            'Credit_History': credit_history,
            'Property_Area': property_area,
            'Loan_Status': loan_status
        })
        return data

    def load_or_create_data(self, data_path='loan_data.csv'):
        try:
            if os.path.exists(data_path):
                logging.info(f"Loading data from {data_path}")
                data = pd.read_csv(data_path)
            else:
                data = self.create_sample_dataset()
                data.to_csv(data_path, index=False)
                logging.info(f"Sample dataset saved to {data_path}")
            return data
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return self.create_sample_dataset()

    def preprocess_data(self, data):
        data = data.copy()
        num_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
        for col in num_cols:
            if col in data.columns:
                data[col] = data[col].fillna(data[col].median())
        for col in self.categorical_columns:
            if col in data.columns:
                data[col] = data[col].fillna(data[col].mode()[0])
        return data

    def encode_features(self, data, is_training=True):
        data_encoded = data.copy()
        for col in self.categorical_columns:
            if col in data_encoded.columns:
                if is_training:
                    self.label_encoders[col] = LabelEncoder()
                    data_encoded[col] = self.label_encoders[col].fit_transform(data_encoded[col])
                else:
                    if col in self.label_encoders:
                        encoder = self.label_encoders[col]
                        if hasattr(encoder, 'classes_'):
                            unique_vals = encoder.classes_
                            data_encoded[col] = data_encoded[col].apply(
                                lambda x: x if x in unique_vals else unique_vals[0]
                            )
                            try:
                                data_encoded[col] = encoder.transform(data_encoded[col])
                            except Exception as e:
                                logging.error(f"Encoding failed for column {col}: {e}")
                                return None
                        else:
                            logging.warning(f"Encoder for {col} has no classes_ attribute.")
                            return None
                    else:
                        logging.warning(f"No encoder for column {col}.")
                        return None
        return data_encoded

    def train_model(self, data_path='loan_data.csv'):
        try:
            data = self.load_or_create_data(data_path)
            data = self.preprocess_data(data)
            X = data[self.feature_columns]
            y = data['Loan_Status']
            X_encoded = self.encode_features(X, is_training=True)

            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42, stratify=y)

            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            models = {
                'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
                'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
            }

            best_score = 0
            best_model_name = None

            for name, model in models.items():
                model.fit(X_train_scaled, y_train)
                score = accuracy_score(y_test, model.predict(X_test_scaled))
                logging.info(f"{name} accuracy: {score:.4f}")
                if score > best_score:
                    best_score = score
                    best_model_name = name
                    self.model = model

            self.model_metrics = {
                'model_name': best_model_name,
                'accuracy': best_score,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }

            self.save_model()
            return True
        except Exception as e:
            logging.error(f"Error training model: {e}")
            return False

    def predict(self, input_data):
        try:
            if self.model is None or not self.label_encoders:
                logging.warning("Model or encoders not loaded. Trying to reload...")
                if not self.load_model():
                    logging.error("Model load failed.")
                    return None, 0.0

            df = pd.DataFrame([input_data])
            df = self.preprocess_data(df)
            df_encoded = self.encode_features(df, is_training=False)
            if df_encoded is None:
                return None, 0.0

            df_scaled = self.scaler.transform(df_encoded)
            prediction = self.model.predict(df_scaled)[0]
            prediction_proba = self.model.predict_proba(df_scaled)[0]
            confidence = prediction_proba[prediction]
            logging.info(f"Prediction: {prediction}, Confidence: {confidence:.2f}")
            return int(prediction), float(confidence)
        except Exception as e:
            logging.error(f"Error making prediction: {e}")
            return None, 0.0

    def save_model(self, model_path='loan_model.pkl'):
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns,
                'categorical_columns': self.categorical_columns,
                'model_metrics': self.model_metrics
            }
            joblib.dump(model_data, model_path)
            logging.info(f"Model saved to {model_path}")
            return True
        except Exception as e:
            logging.error(f"Error saving model: {e}")
            return False

    def load_model(self, model_path='loan_model.pkl'):
        try:
            if os.path.exists(model_path):
                model_data = joblib.load(model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.label_encoders = model_data['label_encoders']
                self.feature_columns = model_data['feature_columns']
                self.categorical_columns = model_data['categorical_columns']
                self.model_metrics = model_data.get('model_metrics', {})
                logging.info(f"Model loaded from {model_path}")
                return True
            else:
                logging.warning(f"Model file {model_path} not found.")
                return False
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return False

    def get_model_metrics(self):
        return self.model_metrics

# Initialize model on import
loan_model = LoanApprovalModel()
if not loan_model.load_model():
    logging.info("No saved model found. Training a new one...")
    loan_model.train_model()
