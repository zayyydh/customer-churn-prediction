from flask import Flask, render_template, request, jsonify
from models import db, Prediction
import joblib, json, numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///churn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

model  = joblib.load('churn_model.pkl')
scaler = joblib.load('churn_scaler.pkl')

with open('feature_names.json')      as f: feature_names = json.load(f)
with open('model_stats.json')        as f: stats         = json.load(f)
with open('feature_importance.json') as f: feat_imp      = json.load(f)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    total = Prediction.query.count()
    high  = Prediction.query.filter_by(risk_level='High Risk').count()
    low   = Prediction.query.filter_by(risk_level='Low Risk').count()
    return render_template('home.html',
                           total_predictions=total,
                           high_risk=high,
                           low_risk=low,
                           stats=stats)

@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_vec    = [float(data.get(f, 0)) for f in feature_names]
        input_arr    = np.array(input_vec).reshape(1, -1)
        input_scaled = scaler.transform(input_arr)

        prob       = float(model.predict_proba(input_scaled)[0][1])
        prediction = int(prob >= 0.5)
        risk       = ('High Risk'   if prob >= 0.7 else
                      'Medium Risk' if prob >= 0.4 else
                      'Low Risk')

        contract = ('Two year'      if float(data.get('Contract_Two year', 0)) == 1
               else 'One year'      if float(data.get('Contract_One year', 0)) == 1
               else 'Month-to-month')
        internet = ('Fiber optic'   if float(data.get('InternetService_Fiber optic', 0)) == 1
               else 'No'            if float(data.get('InternetService_No', 0)) == 1
               else 'DSL')
        payment  = ('Electronic check' if float(data.get('PaymentMethod_Electronic check', 0)) == 1
               else 'Mailed check'     if float(data.get('PaymentMethod_Mailed check', 0)) == 1
               else 'Credit card'      if float(data.get('PaymentMethod_Credit card (automatic)', 0)) == 1
               else 'Bank transfer')

        record = Prediction(
            tenure          = float(data.get('tenure', 0)),
            monthly_charges = float(data.get('MonthlyCharges', 0)),
            total_charges   = float(data.get('TotalCharges', 0)),
            contract        = contract,
            internet        = internet,
            payment         = payment,
            probability     = round(prob * 100, 1),
            risk_level      = risk,
            prediction      = prediction
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            'probability': round(prob * 100, 1),
            'prediction':  prediction,
            'risk':        risk
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stats=stats)

@app.route('/features')
def features():
    return render_template('features.html', feat_imp=feat_imp)

@app.route('/history')
def history():
    predictions = Prediction.query.order_by(
                  Prediction.timestamp.desc()).limit(50).all()
    return render_template('history.html', predictions=predictions)

@app.route('/api/history')
def api_history():
    predictions = Prediction.query.order_by(
                  Prediction.timestamp.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in predictions])

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    Prediction.query.delete()
    db.session.commit()
    return jsonify({'message': 'History cleared'})

if __name__ == '__main__':
    app.run(debug=True)