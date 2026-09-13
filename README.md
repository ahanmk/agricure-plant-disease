# 🌾 AgriCure AI: Multi-Crop Plant Disease Detection & Advisory Web App

An end-to-end intelligent agricultural diagnosis system powered by Deep Learning (MobileNetV2 Transfer Learning). Detects valid crop foliage, classifies **31 conditions across 8 commercial crops**, and provides actionable agronomical advice including visual symptoms, biological remedies, chemical treatments, fertilizer management, and cultural prevention practices.

---

## 🚀 Architecture Overview

- **Frontend (`frontend/`)**: Streamlit web application with an agricultural theme, frosted-glass cards, and a farming landscape background.
- **Backend (`backend/`)**: FastAPI REST API providing a two-tier leaf gatekeeper, deep-learning crop disease inference, and agronomical advisory lookups from `data/advisory.json`.
- **Model**: MobileNetV2 feature extractor trained on a balanced 31-class PlantVillage dataset, reaching **88.82% test accuracy**.

### Supported Crops & Conditions (31 Classes)
- **🍏 Apple**: *Apple scab*, *Black rot*, *Cedar apple rust*, *Healthy*
- **🫑 Bell Pepper**: *Bacterial spot*, *Healthy*
- **🍒 Cherry**: *Powdery mildew*, *Healthy*
- **🌽 Corn (Maize)**: *Cercospora leaf spot (Gray leaf spot)*, *Common rust*, *Northern Leaf Blight*, *Healthy*
- **🍇 Grape**: *Black rot*, *Esca (Black Measles)*, *Leaf blight (Isariopsis)*, *Healthy*
- **🥔 Potato**: *Early blight*, *Late blight*, *Healthy*
- **🍓 Strawberry**: *Leaf scorch*, *Healthy*
- **🍅 Tomato**: *Bacterial spot*, *Early blight*, *Late blight*, *Leaf Mold*, *Septoria leaf spot*, *Spider mites*, *Target Spot*, *Yellow Leaf Curl Virus*, *Mosaic virus*, *Healthy*

---

## 🛠️ Local Development Quickstart

### 1. Start the FastAPI Backend
```powershell
# In terminal 1 (project root):
cd backend
python -m uvicorn main:app --reload --port 8000
```
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)
- Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Streamlit Frontend
```powershell
# In terminal 2 (project root):
python -m streamlit run frontend/app.py --server.port 8501
```
- Open in your browser: [http://localhost:8501](http://localhost:8501)

---

## 🌐 Hackathon Cloud Deployment Guide

Follow this step-by-step guide to deploy the backend on **Render** (or **Railway**) and the frontend on **Streamlit Community Cloud**.

---

### Step 1: Push Code to GitHub

1. Open your terminal in the project directory:
   ```bash
   git init
   git add .
   git commit -m "feat: complete multi-crop disease detection app"
   ```
2. Create a new repository on [GitHub](https://github.com/new) named `agricure-plant-disease` (Public recommended for Streamlit Community Cloud).
3. Push your code:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/agricure-plant-disease.git
   git push -u origin main
   ```
*(Note: Large raw dataset folders are automatically excluded by `.gitignore`, keeping your repository under 30MB for rapid pushing.)*

---

### Step 2: Deploy Backend on Render

1. Sign up / Log in to [Render](https://render.com).
2. On your dashboard, click **"New +"** and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and select your `agricure-plant-disease` repository.
4. Configure the Web Service settings:
   - **Name**: `agricure-api` (or any unique name)
   - **Region**: Choose the region closest to you (e.g., Oregon, Frankfurt, Singapore)
   - **Branch**: `main`
   - **Root Directory**: `backend` *(⚠️ Critical: set this to `backend`)*
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Click **"Create Web Service"**.
6. Wait 2–3 minutes for the build to complete. Once finished, Render will display your live URL:
   `https://agricure-api.onrender.com`
7. Test it by visiting:
   `https://agricure-api.onrender.com/health` in your browser. You should see `{"status": "ok", ...}`.

---

### Alternative: Deploy Backend on Railway (Instant, No Cold-Starts)

If you prefer **Railway** (which offers $5 free credits and does not spin down like Render's free tier):
1. Go to [railway.app](https://railway.app) and click **"New Project"** -> **"Deploy from GitHub repo"**.
2. Select your repository.
3. Click on the newly created service -> go to **"Settings"**:
   - **Root Directory**: set to `/backend`.
4. Go to **"Networking"** -> click **"Generate Domain"**.
5. Your backend is live at: `https://<generated-domain>.up.railway.app`.

---

### Step 3: Deploy Frontend on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **"Create app"** (or **"New app"**).
3. Fill in the deployment details:
   - **Repository**: `<YOUR_GITHUB_USERNAME>/agricure-plant-disease`
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
4. Click **"Advanced settings..."**:
   - In the **Secrets** section, add your deployed backend API URL:
     ```toml
     API_URL = "https://agricure-api.onrender.com/predict"
     ```
     *(Replace `https://agricure-api.onrender.com` with your actual Render or Railway URL)*
   - Click **Save**.
5. Click **"Deploy!"**.
6. Within ~1 minute, your interactive Streamlit application will be live at:
   `https://<your-app-name>.streamlit.app`

---

## 💡 Hackathon Demo Tips

> [!TIP]
> **Render Free Tier Cold Starts**:
> Render's free instances spin down after 15 minutes of inactivity. The first request after sleeping takes about 30–50 seconds to boot up.
> **Before presenting your hackathon pitch**: Open your backend health URL (`https://your-api.onrender.com/health`) 2 minutes in advance to wake up the server!

> [!NOTE]
> **Live API URL Override**:
> The Streamlit app includes an editable **"Backend API Endpoint"** field directly in the sidebar settings. If your backend URL changes during the demo or you want to switch between local and cloud backends, you can update it on the fly without redeploying.

---

## 📁 Repository Structure

```
├── backend/                  # Standalone FastAPI service for cloud hosting
│   ├── main.py               # REST API endpoints (/health, /predict, CORS)
│   ├── classifier.py         # MobileNetV2 model inference & class mapping
│   ├── leaf_detector.py      # Two-tier foliage gatekeeper (ExG / chromaticity)
│   ├── advisory.py           # Agronomical advisory lookup service
│   ├── schemas.py            # Pydantic request & response models
│   ├── Procfile              # Cloud process declaration for web workers
│   ├── requirements.txt      # Lightweight backend dependencies (tensorflow-cpu)
│   ├── data/
│   │   └── advisory.json     # Curated treatment & fertilizer knowledge base
│   └── saved_model/
│       ├── multicrop_model.keras   # Trained 31-class neural network (13.1 MB)
│       └── multicrop_classes.json  # Class label index
│
├── frontend/                 # Streamlit web application
│   ├── app.py                # UI with hero banner, leaf preview & 5 advisory tabs
│   ├── requirements.txt      # Fast frontend dependencies (streamlit, requests)
│   └── assets/
│       └── farmer_bg.jpg     # High-res agricultural field background image
│
├── tests/
│   └── test_multicrop_api.py # Automated integration tests for all 8 crops & non-leaves
│
├── data/
│   └── advisory.json         # Master advisory dataset
├── .gitignore                # Excludes large raw datasets and cache files
└── README.md                 # Project documentation & deployment guide
```
