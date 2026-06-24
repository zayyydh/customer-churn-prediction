from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)

    # Customer inputs
    tenure        = db.Column(db.Float)
    monthly_charges = db.Column(db.Float)
    total_charges = db.Column(db.Float)
    contract      = db.Column(db.String(20))
    internet      = db.Column(db.String(20))
    payment       = db.Column(db.String(30))

    # Result
    probability   = db.Column(db.Float)
    risk_level    = db.Column(db.String(15))
    prediction    = db.Column(db.Integer)  # 0 or 1

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'tenure': self.tenure,
            'monthly_charges': self.monthly_charges,
            'total_charges': self.total_charges,
            'contract': self.contract,
            'internet': self.internet,
            'payment': self.payment,
            'probability': self.probability,
            'risk_level': self.risk_level,
            'prediction': self.prediction
        }