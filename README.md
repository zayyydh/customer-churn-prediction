# 🔮 Customer Churn Prediction — Full Stack ML Web App

go check on any web browser:https://customer-churn-prediction-apws.onrender.com/

A full-stack machine learning web app that predicts whether a telecom customer will churn, built with Flask and Scikit-learn.

## 🌐 Pages
- **Home** — Landing page with live stats, how it works, and key insights
- **Predict** — Input customer details and get churn probability with a gauge chart
- **Dashboard** — Model performance metrics, confusion matrix, ROC curve
- **Features** — Interactive feature importance chart
- **History** — All past predictions saved to SQLite database

## 🧠 Model
- Algorithm: Logistic Regression
- Dataset: IBM Telco Customer Churn (7,043 customers)
- ROC-AUC Score: 0.842
- Accuracy: 80.7%
- F1 Score (Churn): 0.609

## 🔑 Key Findings
- Fiber optic internet users churn the most
- Month-to-month contracts have highest churn risk
- Long tenure customers are the most loyal
- Online security & tech support reduce churn significantly

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML | Scikit-learn, XGBoost |
| Database | SQLite + Flask-SQLAlchemy |
| Frontend | HTML, CSS, Plotly.js |
| Features | Dark mode, Mobile responsive, Prediction history |

## ⚙️ Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```
Then open `http://127.0.0.1:5000`

## 📁 Project Structure
