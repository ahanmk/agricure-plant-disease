# 🚀 Step-by-Step Production Deployment Guide (Render + Streamlit Cloud)

This guide walks you through deploying your AgriCure Multi-Crop Disease Diagnostic system to the web **for free**.

---

## Part 1: Push Code to GitHub

If you haven't pushed your code to GitHub yet, run the following commands in your project terminal:

```powershell
git add .
git commit -m "Prepare production deployment configuration"
git push origin main
```

---

## Part 2: Deploy Backend API on Render (Free)

1. Sign up or log in to **[Render Dashboard](https://dashboard.render.com)**.
2. Click **New +** (top right) $\rightarrow$ select **Web Service**.
3. Connect your GitHub repository.
4. Fill in the deployment details:
   * **Name**: `agricure-backend-api`
   * **Region**: Select nearest region (e.g. Oregon / Frankfurt / Singapore)
   * **Branch**: `main`
   * **Root Directory**: `backend`
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   * **Instance Type**: `Free`
5. Click **Create Web Service**.
6. Wait 2-3 minutes for the build to finish. Once live, copy your Web Service URL:
   * Example: `https://agricure-backend-api.onrender.com`

> 💡 **Health Verification**: Open `https://agricure-backend-api.onrender.com/health` in your browser. You should see `{"status": "ok", "service": "AgriCure Multi-Crop Production API", ...}`.

---

## Part 3: Deploy Frontend on Streamlit Community Cloud (Free)

1. Sign up or log in to **[Streamlit Community Cloud](https://share.streamlit.io)**.
2. Click **Create app** $\rightarrow$ select **Use existing repo**.
3. Fill in the repository details:
   * **Repository**: `your-username/all-crops`
   * **Branch**: `main`
   * **Main file path**: `frontend/app.py`
4. Click **Advanced settings...** at the bottom of the form.
5. In the **Secrets** text box, paste your Render backend URL:
   ```toml
   API_URL = "https://agricure-backend-api.onrender.com/predict"
   ```
6. Click **Save**, then click **Deploy!**

---

## 🎉 Your Application is Live!

Your website will build and open at a custom URL such as:
`https://agricure-crop-disease.streamlit.app`

Anyone on a smartphone, tablet, or laptop anywhere in the world can now visit your website URL, upload a leaf photograph, and get instant crop disease diagnoses!
