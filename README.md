
# 🌬️ HVAC AI Platform

A full-stack web platform for simulating HVAC system performance, monitoring energy usage, and predicting faults using AI. Built to empower technicians, facility managers, and researchers to make data-driven decisions and reduce energy waste.

Read more about my energy efficiency blog here 

alfiyay.com/blog/energy-derivatives
---

## 🚀 Features

- 🏢 **HVAC Simulation:** Simulate HVAC energy usage using EnergyPlus and other standard models.
- 📊 **Real-Time Monitoring:** Display live and historical sensor data with anomaly visualization.
- 🤖 **AI-Powered Fault Prediction:** Detect faults early using ML models trained on time-series sensor data.
- 🧠 **Continuous Learning:** Improve predictions with feedback and new sensor inputs.
- ☁️ **Cloud Native:** Fully containerized and deployed to AWS via Terraform and Docker.
- 🧑‍🤝‍🧑 **Inclusive Design:** Accessibility-first frontend with intuitive insights for end-users.

---

## 🧱 Tech Stack

| Layer         | Tech                                                    |
|---------------|----------------------------------------------------------|
| Frontend      | React, TypeScript, Tailwind, WebSockets                  |
| Backend       | Django, Django REST Framework, Celery                    |
| ML/AI         | Python, Pandas, Scikit-learn, PyTorch (optional)         |
| Database      | PostgreSQL, TimescaleDB or InfluxDB for time-series     |
| DevOps        | Docker, Terraform, AWS (EC2, RDS, ECS, CloudWatch)       |
| Simulation    | EnergyPlus (wrapped with Python)                         |

---

## 🛠️ Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Terraform & AWS CLI

### Backend Setup

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Containerized (Dev Mode)

```bash
cd infrastructure/docker
docker-compose up --build
```

### 🤖 Machine Learning
Train and deploy your ML models:

```bash
cd backend/ml_models
python trainer.py   # Train model
python predictor.py # Test prediction
```

Use predictor.py to serve predictions via Django API.

### ☁️ Cloud Deployment (AWS)

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

---

## 📑 API Endpoints

### Simulation
**POST** `/api/simulate/`
```json
{
	"building_id": "B1",
	"start_time": "2025-10-03T10:00",
	"end_time": "2025-10-03T12:00",
	"parameters": {"temp": 22}
}
```
**Response:** `{ "result": "Simulation run complete" }`

### Prediction
**POST** `/api/predict/`
```json
{
	"sensor_data": [[22.1, 48, 420], [22.3, 47, 425]],
	"timestamp": "2025-10-03T10:00"
}
```
**Response:** `{ "prediction": [0, 1] }`

### Monitoring (Sensor Data)
**GET** `/api/ingest/`
Returns latest sensor data (JSON array)

**POST** `/api/ingest/`
Ingest new time-series data (to be implemented)

---

## 🧠 ML Model Usage

- Train: `python backend/ml_models/trainer.py`
- Predict: `python backend/ml_models/predictor.py`
- Model and scaler are saved in `backend/ml_models/`
- API uses these for predictions

---

## 📈 Example Use Cases

- Smart buildings with real-time fault detection
- Facilities aiming to reduce carbon emissions
- Engineers testing retrofits or new HVAC designs

---

## ❤️ Contributing
We welcome contributors from all backgrounds! Please read CONTRIBUTING.md for how to get started.

## 🌍 License
MIT License © 2025 Alfiya Valitova


STEPS FOR ME: 
Start your Django backend (python manage.py runserver).
In the frontend, run npm run dev.
Visit http://localhost:3000 to use your React app, which will connect to the backend at /api.

To see your API endpoints, visit:
http://localhost:8000/api/simulate/
http://localhost:8000/api/predict/
http://localhost:8000/api/ingest/