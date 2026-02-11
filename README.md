Excellent 👏
Now we’ll create a **professional, production-ready README.md** for your SkyCast AI project.

You can directly copy-paste this into your GitHub README.md.

---

# 🌤️ SkyCast AI – Predictive Weather Forecasting Platform

SkyCast AI is an end-to-end Machine Learning powered weather forecasting web application that collects live weather data, stores it in a cloud database, trains ML models, and serves intelligent forecasts through a Flask web interface deployed on AWS.

---

## 🚀 Live Deployment

🌍 **Public URL:**

```
http://18.207.118.178:5000
```

<img width="1893" height="866" alt="image" src="https://github.com/user-attachments/assets/dab5bc37-cca1-44fb-809c-1b06ea3487c0" />


Hosted on:

* AWS EC2 (Amazon Linux 2023)
* Gunicorn production server
* Neon Cloud PostgreSQL Database

---

# 📌 Project Overview

SkyCast AI performs:

1. 🌦️ Daily weather data ingestion using external APIs
2. 🗄️ Cloud storage using Neon PostgreSQL
3. 🧠 Machine Learning model training (XGBoost)
4. 📊 Dataset preparation & preprocessing
5. 🌐 Web deployment using Flask
6. 🚀 Production hosting on AWS EC2

---

<img width="1750" height="865" alt="image" src="https://github.com/user-attachments/assets/8965ea57-ce42-4faf-aed3-547aa8bd415c" />


# 🧠 Key Features

✅ Automated Daily Weather Data Collection
✅ PostgreSQL Cloud Database Integration
✅ ML Model Training using XGBoost
✅ City-wise Forecasting
✅ Historical Weather Storage
✅ Clean Interactive Flask UI
✅ Cloud Deployment (AWS EC2)
✅ Environment Variable Security (.env)
✅ Production Server using Gunicorn

---

<img width="1849" height="864" alt="image" src="https://github.com/user-attachments/assets/d2a7a94f-aa42-4270-a519-c592817ffd73" />

# 🏗️ Project Architecture

```
SkyCast AI
│
├── app.py                     # Flask application entry point
│
├── data_collection/
│   └── daily_weather_updater.py   # Collects daily weather data
│
├── database/
│   ├── db.py                      # Database engine setup
│   ├── create_tables.py
│   └── check_data.py
│
├── ml/
│   ├── prepare_dataset.py         # Data preprocessing
│   ├── train_model.py             # ML training
│
├── extensions/                    # Additional app modules
│
├── models/
│   └── weather_model.pkl          # Trained ML model
│
├── static/                        # CSS, JS, assets
├── templates/                     # HTML templates
│
├── requirements.txt
└── README.md
```

---

<img width="1644" height="866" alt="image" src="https://github.com/user-attachments/assets/724b5fa8-b593-4126-9489-1a047e7d9ad3" />

# 🛠️ Tech Stack

### 🖥 Backend

* Python 3.9
* Flask
* Gunicorn

### 🧠 Machine Learning

* Scikit-Learn
* XGBoost
* Joblib
* Pandas
* NumPy

### 🗄 Database

* PostgreSQL
* Neon Cloud Database
* SQLAlchemy
* Psycopg2

### ☁ Cloud & Deployment

* AWS EC2 (Amazon Linux 2023)
* Security Groups
* Public IPv4 Hosting
* Virtual Environment
* Gunicorn Production Server

### 🔐 Security

* Environment variables using `.env`
* python-dotenv

---

# 🔄 End-to-End Workflow

### Step 1 — Data Collection

```
python -m data_collection.daily_weather_updater
```

* Fetches weather data via API
* Stores data in Neon PostgreSQL

---

### Step 2 — Prepare Dataset

```
python -m ml.prepare_dataset
```

* Cleans and preprocesses weather data
* Creates ML-ready dataset

---

### Step 3 — Train Model

```
python -m ml.train_model
```

* Trains XGBoost regression model
* Saves model in `models/weather_model.pkl`

---

### Step 4 — Run Flask App

Development:

```
python app.py
```

Production:

```
sudo gunicorn -b 0.0.0.0:80 app:app
```

---

# 🔑 Environment Variables (.env)

Create a `.env` file:

```
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
VISUAL_CROSSING_API_KEY=your_api_key
LOCATIONIQ_API_KEY=your_api_key
```

Never upload `.env` to GitHub.

---

# 🌍 Deployment Guide (AWS EC2)

1. Launch EC2 (t3.micro recommended for free tier)
2. Open inbound ports:

   * 22 (SSH)
   * 80 (HTTP)
3. Clone repository
4. Create virtual environment
5. Install requirements
6. Configure `.env`
7. Run Gunicorn

---

# 📊 Machine Learning Details

* Model Type: XGBoost Regressor
* Training Data: Historical weather dataset
* Features: Temperature, humidity, wind speed, etc.
* Output: Future temperature prediction

---

# 🧠 Prompt Engineering Usage

Prompt Engineering is used to:

* Design structured AI explanations and codes
* Optimize model interaction workflows
* Enhance forecasting logic clarity
* Improve AI-generated insights

---

# 📦 Requirements

Key dependencies:

```
flask
pandas
sqlalchemy
psycopg2-binary
scikit-learn
xgboost
joblib
python-dotenv
meteostat
gunicorn
```

---

# 🏆 Skills Demonstrated

✔ End-to-End ML Pipeline
✔ Cloud Deployment
✔ Database Engineering
✔ Backend Development
✔ API Integration
✔ DevOps & Linux Commands
✔ AWS Infrastructure Management
✔ Environment Variable Management
✔ Production Server Setup

---

# 📈 Future Improvements

* Add CI/CD using GitHub Actions
* Add scheduled cron jobs
* Add Nginx reverse proxy
* Add HTTPS using SSL
* Deploy using Docker
* Add user authentication

---

# 👩‍💻 Author

Subham
M.Tech Graduate | ML Engineer | Cloud Enthusiast

---

# ⭐ If You Like This Project

Give it a ⭐ on GitHub.



