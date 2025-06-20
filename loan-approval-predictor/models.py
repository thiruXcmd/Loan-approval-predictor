from extensions import db  # ✅ Replaces 'from app import db'

class LoanPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_income = db.Column(db.Float, nullable=False)
    coapplicant_income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_amount_term = db.Column(db.Integer, nullable=False)
    credit_history = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    married = db.Column(db.String(10))
    dependents = db.Column(db.String(10))
    education = db.Column(db.String(20))
    self_employed = db.Column(db.String(10))
    property_area = db.Column(db.String(20))
    prediction = db.Column(db.String(20))
    confidence = db.Column(db.Float)
