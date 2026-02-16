# 🌱 EcoScale – Carbon-Aware Cloud Optimization Platform

EcoScale is an AI-powered, carbon-aware cloud workload optimization platform that helps businesses reduce energy consumption, lower CO₂ emissions, and optimize infrastructure intelligently.

It combines:
-  ML-based workload prediction
-  Carbon emission modeling
-  Explainable AI (SHAP-based insights)
-  Before vs After sustainability comparison
-  Green Score metric

---

##  Problem Statement

Cloud infrastructure is often **over-provisioned**, leading to:
- High energy consumption
- Increased carbon emissions
- Unnecessary cloud costs

Most companies optimize for performance and cost — but not for sustainability.

EcoScale bridges this gap by providing **AI-driven, carbon-aware infrastructure recommendations**.

---

##  Key Features

### 1️⃣ ML-Based Resource Optimization
- Predicts CPU utilization
- Suggests optimal CPU allocation
- Adjusts based on workload type (Web / API / ML)

### 2️⃣ Carbon-Aware Simulation
- Calculates:
  - Energy consumption (kWh)
  - CO₂ emissions (kg)
  - Cost estimation ($)
- Compares before vs optimized configuration

### 3️⃣ Time-Series Workload Prediction
- Predicts traffic for user-selected hours
- Helps identify peak and off-peak periods
- Supports smarter scheduling

### 4️⃣ Explainable AI (XAI)
- Uses SHAP (Shapley Additive Explanations)
- Shows feature impact:
  - Traffic impact
  - CPU impact
  - Memory impact
- Makes recommendations transparent and interpretable

### 5️⃣ Green Score System
- Score between 0–100
- Based on carbon reduction percentage
- Encourages sustainability-focused decisions

---

##  Architecture Overview

### Frontend
- React + TypeScript
- TailwindCSS
- Framer Motion (animations)
- Recharts (visualizations)

### Backend
- FastAPI
- Random Forest models
- SHAP for explainability
- Energy & carbon simulation modules

### ML Components
- Utilization prediction model
- Optimal CPU recommendation model
- Time-series traffic prediction model

---

##  System Flow

1. User inputs workload configuration
2. Backend ML models predict:
   - CPU utilization
   - Optimal CPU allocation
3. Energy & carbon modules compute emissions
4. SHAP explains model decisions
5. Frontend displays:
   - Recommendations
   - Before vs After dashboard
   - Green Score
   - Visual charts

---

##  Tech Stack

### Frontend
- React
- TypeScript
- TailwindCSS
- Recharts
- Framer Motion

### Backend
- FastAPI
- Pydantic
- Joblib
- SHAP
- Scikit-learn (Random Forest)

---

##  Installation & Setup

### 1️) Clone the repository

```bash
git clone https://github.com/your-username/ecoscale.git

```
### 2) Backend Setup

```bash
cd ecoscale-backend
pip install -r requirements.txt
```

```bash
python ml/dataset-generator.py
python ml/timeseries_dataset_generator.py
python ml/train_optimization_model.py
python ml/train_utilisation_model.py
python ml/train_timeseries_model.py
```
### 3) Run Backend

```bash
uvicorn main:app --reload --port 8000
```

### 4) Run Frontend (In separate terminal)

```bash
cd frontend
npm install
npm run dev
```



