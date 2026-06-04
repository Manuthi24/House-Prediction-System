# 🏠 House Price Prediction System

A full-stack machine learning web application that predicts house prices in the King County, Seattle Metro area. The system uses a **Gradient Boosting Regression** model, a **FastAPI backend**, and a **React + Vite frontend**.

---

## ✨ Features

- 🏡 Predict house prices using property details
- 🤖 Machine learning model trained with King County house sales data
- ⚡ FastAPI backend with REST API endpoints
- 🎨 Responsive React frontend
- 📊 Displays predicted price with confidence range
- 🔁 Option to retrain the model when needed

---

## 🛠️ Tech Stack

**Frontend**
- React
- Vite
- CSS

**Backend**
- Python
- FastAPI
- scikit-learn
- pandas
- numpy
- joblib
- Pydantic

**Machine Learning**
- Gradient Boosting Regressor
- StandardScaler
- King County House Sales Dataset

---

## 📁 Project Structure

```txt
house-price-predictor/
│
├── backend/
│   ├── data/
│   │   └── kc_house_data.csv
│   ├── model/
│   │   ├── train.py
│   │   └── model.pkl
│   ├── main.py
│   ├── schemas.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── predict.js
    │   ├── components/
    │   │   ├── PredictionForm.jsx
    │   │   └── ResultCard.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    └── vite.config.js

🚀 How to Run the Project

1️⃣ Run the Backend
cd house-price-predictor/backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000

Backend runs at:

http://localhost:8000

API documentation:

http://localhost:8000/docs

2️⃣ Run the Frontend

Open a new terminal:

cd house-price-predictor/frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173

🤖 Train the ML Model

If model.pkl is missing, train the model again:

cd house-price-predictor/backend
venv\Scripts\activate
python model/train.py --data data/kc_house_data.csv --output model/model.pkl

🔗 API Endpoints
Method	Endpoint	Description
GET	/	Check backend status
GET	/health	Check backend and model health
POST	/predict	Predict house price
GET	/features	Get input feature details

📌 Important Notes
Backend must be running before using the frontend.
venv, node_modules, and model.pkl should not be uploaded to GitHub.
If model.pkl is not available after cloning, retrain the model using the training command.
The frontend sends prediction requests to the backend API at http://localhost:8000.
