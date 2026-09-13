# AgriCure AI: Multi-Crop Plant Disease Detection & Advisory Web App

An end-to-end intelligent agricultural diagnosis system powered by Deep Learning (MobileNetV2 Transfer Learning). Detects valid crop foliage, classifies **31 conditions across 8 commercial crops**, and provides actionable agronomical advice including visual symptoms, biological remedies, chemical treatments, fertilizer management, and cultural prevention practices.

---

## Architecture Overview

- **Frontend (`frontend/`)**: Streamlit web application with an agricultural theme, frosted-glass cards, and a farming landscape background.
- **Backend (`backend/`)**: FastAPI REST API providing a two-tier leaf gatekeeper, deep-learning crop disease inference, and agronomical advisory lookups from `data/advisory.json`.
- **Model**: MobileNetV2 feature extractor trained on a balanced 31-class PlantVillage dataset, reaching **88.82% test accuracy**.

### Supported Crops & Conditions (31 Classes)
- ** Apple**: *Apple scab*, *Black rot*, *Cedar apple rust*, *Healthy*
- ** Bell Pepper**: *Bacterial spot*, *Healthy*
- ** Cherry**: *Powdery mildew*, *Healthy*
- ** Corn (Maize)**: *Cercospora leaf spot (Gray leaf spot)*, *Common rust*, *Northern Leaf Blight*, *Healthy*
- ** Grape**: *Black rot*, *Esca (Black Measles)*, *Leaf blight (Isariopsis)*, *Healthy*
- ** Potato**: *Early blight*, *Late blight*, *Healthy*
- ** Strawberry**: *Leaf scorch*, *Healthy*
- ** Tomato**: *Bacterial spot*, *Early blight*, *Late blight*, *Leaf Mold*, *Septoria leaf spot*, *Spider mites*, *Target Spot*, *Yellow Leaf Curl Virus*, *Mosaic virus*, *Healthy*

---



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
