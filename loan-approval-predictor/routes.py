from flask import request, render_template, redirect, url_for, flash
from ml_model import loan_model
from extensions import db
import logging

from flask import Blueprint
from models import LoanPrediction

from app import app  # Required if you're not using Blueprint setup

@app.route('/')
def index():
    metrics = loan_model.get_model_metrics()
    return render_template('index.html', model_metrics=metrics)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = {
            'Gender': request.form.get('gender'),
            'Married': request.form.get('married'),
            'Dependents': request.form.get('dependents'),
            'Education': request.form.get('education'),
            'Self_Employed': request.form.get('self_employed'),
            'ApplicantIncome': float(request.form.get('applicant_income', 0)),
            'CoapplicantIncome': float(request.form.get('coapplicant_income', 0)),
            'LoanAmount': float(request.form.get('loan_amount', 0)),
            'Loan_Amount_Term': int(request.form.get('loan_term', 360)),
            'Credit_History': int(request.form.get('credit_history', 1)),
            'Property_Area': request.form.get('property_area')
        }

        logging.debug(f"Form data received: {form_data}")

        # Check required dropdown fields
        required_fields = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
        missing_fields = [field for field in required_fields if not form_data[field]]
        if missing_fields:
            flash(f'Missing required fields: {", ".join(missing_fields)}', 'error')
            return redirect(url_for('index'))

        if form_data['ApplicantIncome'] <= 0 or form_data['LoanAmount'] <= 0:
            flash('Income and loan amount must be greater than 0.', 'error')
            return redirect(url_for('index'))

        # Make prediction
        prediction, confidence = loan_model.predict(form_data)
        if prediction is None:
            flash('Prediction failed. Please check input values.', 'error')
            return redirect(url_for('index'))

        # Save to database
        loan = LoanPrediction(
            applicant_income=form_data['ApplicantIncome'],
            coapplicant_income=form_data['CoapplicantIncome'],
            loan_amount=form_data['LoanAmount'],
            loan_amount_term=form_data['Loan_Amount_Term'],
            credit_history=form_data['Credit_History'],
            gender=form_data['Gender'],
            married=form_data['Married'],
            dependents=form_data['Dependents'],
            education=form_data['Education'],
            self_employed=form_data['Self_Employed'],
            property_area=form_data['Property_Area'],
            prediction="Approved" if prediction == 1 else "Not Approved",
            confidence=confidence
        )
        db.session.add(loan)
        db.session.commit()
        
        income_ratio = form_data['LoanAmount'] / max(1, (form_data['ApplicantIncome'] + form_data['CoapplicantIncome']))

        return render_template("prediction.html",
    prediction="Approved" if prediction == 1 else "Not Approved",
    confidence=confidence * 100,
    form_data=form_data,
    income_ratio=income_ratio  # ✅ THIS IS REQUIRED
)


    except Exception as e:
        flash('An error occurred while processing your request. Please try again.', 'error')
        logging.error(f"Error in prediction route: {e}", exc_info=True)
        return redirect(url_for('index'))


@app.route('/retrain', methods=['POST'])
def retrain():
    success = loan_model.train_model()
    if success:
        flash('Model retrained successfully.', 'success')
    else:
        flash('Failed to retrain model.', 'error')
    return redirect(url_for('index'))
