# AgriCure AI: Multi-Crop Plant Disease Detection & Advisory Web App

An end-to-end intelligent agricultural diagnosis system powered by Deep Learning (MobileNetV2 Transfer Learning). Detects valid crop foliage, classifies **31 conditions across 8 commercial crops**, and provides actionable agronomical advice including visual symptoms, biological remedies, chemical treatments, fertilizer management, and cultural prevention practices.

---

## ⚡ Quick Start: Running Locally

### 1. Start the Active FastAPI Backend
From the project root directory, launch the active FastAPI server:
```powershell
uvicorn api.main:app --reload --port 8000
```
*Health Check*: Access `http://localhost:8000/health` to confirm the model and API are online.

### 2. Start the Active Streamlit Frontend
In a separate terminal window, launch the Streamlit frontend:
```powershell
streamlit run frontend/app.py
```
*Web Application*: Access `http://localhost:8501` in your browser.

---

## 📋 Image Upload Restrictions & Technical Limits

* **Supported File Formats**: `JPG`, `JPEG`, `PNG`
* **Maximum File Size Limit**: `10 MB`
* **Image Mode Compatibility**: Automatic conversion of `RGBA`, `LA`, `P`, `L`, and `CMYK` modes to 3-channel `RGB`.
* **Sanitized Error Handling**: Server logs detailed Python exception tracebacks internally while client interfaces display safe, actionable error guidance without exposing stack traces.

---

## 📱 Mobile (Android Browser) Testing Checklist

To verify mobile usability on Android phone browsers (e.g. Chrome Mobile / Firefox Mobile):

1. **Responsive Viewport Layout**: Open DevTools Mobile Emulator (360px - 412px width) or test directly on an Android device. Ensure no horizontal scrolling or clipped cards occur.
2. **Camera & File Selection**: Tap the file uploader and verify Android native options appear (*Camera* to capture a live photo, or *Files/Gallery* to select a saved photo).
3. **Touch Targets**: Confirm all interactive controls (Crop Selector, File Uploader, and "Analyze Leaf Image" button) have a minimum tap height of 48px.
4. **Result Clarity**: Ensure crop diagnosis banner, confidence percentage bar, and management recommendations stack vertically without overlapping.
5. **Error Notification**: Test uploading an invalid file format or corrupted image and verify the clear error card displays cleanly on mobile screens.

---

## 📁 Repository Structure

```
├── api/                      # Active local FastAPI backend service
│   ├── main.py               # Active REST API endpoints (/health, /predict, CORS) & validation
│   ├── classifier.py         # MobileNetV2 model inference & class mapping
│   ├── leaf_detector.py      # Two-tier foliage gatekeeper (ExG / chromaticity)
│   ├── advisory.py           # Agronomical advisory lookup service
│   └── schemas.py            # Pydantic request & response models
│
├── frontend/                 # Active Streamlit web application
│   ├── app.py                # Mobile-first, emoji-free professional UI
│   ├── requirements.txt      # Frontend dependencies (streamlit, requests)
│   └── assets/               # Assets directory
│
├── backend/                  # Preserved standalone PaaS deployment bundle
├── tests/
│   └── test_multicrop_api.py # Automated integration & input validation tests
├── saved_model/              # Master trained neural network weights & class index
├── data/
│   └── advisory.json         # Master advisory dataset
├── requirements.txt          # Complete local environment requirements
└── README.md                 # Project documentation & setup guide
```
