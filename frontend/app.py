import html
import io
import os
import requests
from PIL import Image
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------
MAX_UPLOAD_MB = 10
LOW_CONFIDENCE = 60.0

# ---------------------------------------------------------------------------
# Multilingual Translations (English, Kannada, Hindi)
# ---------------------------------------------------------------------------
I18N = {
    "en": {
        "app_title": "AgriCure | Crop Disease Diagnostic System",
        "tagline": "AI-Powered Leaf Disease Detection & Instant Treatment Advisory",
        "nav_diag": "Leaf Diagnostic",
        "nav_crops": "Supported Crops",
        "nav_tips": "Field Photo Tips",
        "nav_settings": "Connection",
        "step1_title": "1. Select Crop (Optional)",
        "step2_title": "2. Capture or Upload Leaf Photo",
        "upload_tab": "Upload File",
        "camera_tab": "Use Camera",
        "upload_label": "Choose a JPG or PNG leaf photo",
        "camera_label": "Take a photo of the affected leaf",
        "upload_hint": "Supported: JPG, JPEG, PNG (max 10 MB)",
        "tip_text": "Fill the frame with a single leaf under daylight for the most accurate diagnosis.",
        "btn_check": "Diagnose Leaf",
        "btn_checking": "Analyzing leaf with AI...",
        "not_a_leaf_title": "Image Not Recognized as Leaf",
        "not_a_leaf_msg": "The uploaded photo does not appear to be a plant leaf. Please retake a clear leaf photo.",
        "healthy_stamp": "HEALTHY",
        "diseased_stamp": "DISEASED",
        "crop_label": "Crop",
        "severity_label": "Severity",
        "confidence_label": "Confidence",
        "pathogen_prefix": "Pathogen",
        "low_conf_warning": "Low confidence. Please retake photo in bright daylight with a closer view.",
        "tab_symptoms": "Symptoms",
        "tab_treatment": "Treatment",
        "tab_care": "Care Guide",
        "tab_fertilizer": "Fertilizer Advisory",
        "tab_prevention": "Prevention",
        "organic_title": "Organic & Biological Solutions",
        "chemical_title": "Chemical Control Options",
        "no_mgmt_info": "Maintain regular sanitation and inspection.",
        "disclaimer": "Diagnostic result is based on computer vision. Consult your local agriculture extension officer before spraying chemicals for widespread infestations.",
        "server_error": "Backend server could not process the photo",
        "cannot_reach": "Cannot reach inference server",
        "make_sure_uvicorn": "Make sure your FastAPI server is running: uvicorn api.main:app --reload --port 8000",
        "all_crops": "All Supported Crops (Auto-Detect)",
    },
    "kn": {
        "app_title": "ಅಗ್ರಿಕ್ಯೂರ್ | ಬೆಳೆ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಪರಿಹಾರ ವ್ಯವಸ್ಥೆ",
        "tagline": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ಆಧಾರಿತ ಬೆಳೆ ರೋಗ ಪತ್ತೆ ಹಾಗೂ ತ್ವರಿತ ಚಿಕಿತ್ಸಾ ಮಾರ್ಗದರ್ಶಿ",
        "nav_diag": "ರೋಗ ತಪಾಸಣೆ",
        "nav_crops": "ಬೆಳೆಗಳ ಪಟ್ಟಿ",
        "nav_tips": "ಫೋಟೋ ಸಲಹೆಗಳು",
        "nav_settings": "ಸಂಪರ್ಕ ಸಂರಚನೆ",
        "step1_title": "೧. ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಐಚ್ಛಿಕ)",
        "step2_title": "೨. ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ತೆಗೆಯಿರಿ",
        "upload_tab": "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್",
        "camera_tab": "ಕ್ಯಾಮೆರಾ ಬಳಸಿ",
        "upload_label": "JPG ಅಥವಾ PNG ಎಲೆಯ ಫೋಟೋ ಆಯ್ಕೆಮಾಡಿ",
        "camera_label": "ರೋಗಗ್ರಸ್ತ ಎಲೆಯ ಚಿತ್ರ ತೆಗೆಯಿರಿ",
        "upload_hint": "ಬೆಂಬಲಿತ: JPG, JPEG, PNG (ಗರಿಷ್ಠ 10 MB)",
        "tip_text": "ನಿಖರ ಫಲಿತಾಂಶಕ್ಕಾಗಿ ಹಗಲು ಬೆಳಕಿನಲ್ಲಿ ಒಂದೇ ಎಲೆಯು ಪೂರ್ಣವಾಗಿ ಕಾಣುವಂತೆ ಫೋಟೋ ತೆಗೆಯಿರಿ.",
        "btn_check": "ಈ ಎಲೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ",
        "btn_checking": "ಎಲೆಯ ಚಿತ್ರವನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "not_a_leaf_title": "ಚಿತ್ರವು ಎಲೆಯಂತೆ ಕಂಡುಬರುತ್ತಿಲ್ಲ",
        "not_a_leaf_msg": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರವು ಗಿಡದ ಎಲೆಯಾಗಿ ಕಂಡುಬರುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ ಎಲೆಯ ಚಿತ್ರವನ್ನು ನೀಡಿ.",
        "healthy_stamp": "ಆರೋಗ್ಯಕರ",
        "diseased_stamp": "ರೋಗಗ್ರಸ್ತ",
        "crop_label": "ಬೆಳೆ",
        "severity_label": "ತೀವ್ರತೆ",
        "confidence_label": "ನಿಖರತೆ",
        "pathogen_prefix": "ರೋಗಕಾರಕ",
        "low_conf_warning": "ನಿಖರತೆ ಕಡಿಮೆ ಇದೆ. ದಯವಿಟ್ಟು ಹಗಲು ಬೆಳಕಿನಲ್ಲಿ ಎಲೆಯ ಹತ್ತಿರದ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಮತ್ತೊಮ್ಮೆ ತೆಗೆಯಿರಿ.",
        "tab_symptoms": "ಲಕ್ಷಣಗಳು",
        "tab_treatment": "ಚಿಕಿತ್ಸೆ",
        "tab_care": "ಆರೈಕೆ ಮಾರ್ಗ",
        "tab_fertilizer": "ಗೊಬ್ಬರ ಸಲಹೆ",
        "tab_prevention": "ತಡೆಗಟ್ಟುವ ಕ್ರಮಗಳು",
        "organic_title": "ಸಾವಯವ ಹಾಗೂ ಜೈವಿಕ ಪರಿಹಾರಗಳು",
        "chemical_title": "ರಾಸಾಯನಿಕ ನಿಯಂತ್ರಣ ಕ್ರಮಗಳು",
        "no_mgmt_info": "ನಿಯಮಿತ ನೈರ್ಮಲ್ಯ ಮತ್ತು ಬೆಳೆ ತಪಾಸಣೆಯನ್ನು ಮುಂದುವರಿಸಿ.",
        "disclaimer": "ಈ ಫಲಿತಾಂಶವು AI ಕಂಪ್ಯೂಟರ್ ದೃಷ್ಟಿ ಆಧಾರಿತವಾಗಿದೆ. ದೊಡ್ಡ ಪ್ರಮಾಣದಲ್ಲಿ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸುವ ಮುನ್ನ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "server_error": "ಸರ್ವರ್‌ಗೆ ಈ ಚಿತ್ರವನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ",
        "cannot_reach": "ಹಿನ್ನೆಲೆ ಸರ್ವರ್ ಸಂಪರ್ಕ ವಿಫಲವಾಗಿದೆ",
        "make_sure_uvicorn": "ನಿಮ್ಮ FastAPI ಸರ್ವರ್ ಚಾಲನೆಯಲ್ಲಿದೆಯೇ ಪರಿಶೀಲಿಸಿ: uvicorn api.main:app --reload --port 8000",
        "all_crops": "ಎಲ್ಲಾ ಬೆಳೆಗಳು (ಸ್ವಯಂ ಪತ್ತೆ)",
    },
    "hi": {
        "app_title": "एग्रीक्योर | फसल रोग निदान एवं उपचार प्रणाली",
        "tagline": "एआई-आधारित फसल रोग पहचान एवं त्वरित उपचार सलाह",
        "nav_diag": "रोग निदान",
        "nav_crops": "समर्थित फसलें",
        "nav_tips": "फोटो सुझाव",
        "nav_settings": "सर्वर कनेक्शन",
        "step1_title": "१. अपनी फसल चुनें (वैकल्पिक)",
        "step2_title": "२. पत्ते की फोटो अपलोड करें या खींचें",
        "upload_tab": "फ़ाइल अपलोड",
        "camera_tab": "कैमरा खोलें",
        "upload_label": "JPG या PNG पत्ते की फोटो चुनें",
        "camera_label": "प्रभावित पत्ते की फोटो खींचें",
        "upload_hint": "समर्थित प्रारूप: JPG, JPEG, PNG (अधिकतम 10 MB)",
        "tip_text": "सटीक परिणाम के लिए दिन के उजाले में केवल एक पत्ते की साफ़ तस्वीर लें।",
        "btn_check": "इस पत्ते की जाँच करें",
        "btn_checking": "पत्ते का विश्लेषण किया जा रहा है...",
        "not_a_leaf_title": "यह तस्वीर पत्ते की नहीं लगती",
        "not_a_leaf_msg": "अपलोड की गई तस्वीर पौधे के पत्ते जैसी नहीं है। कृपया साफ़ पत्ते की तस्वीर दोबारा लें।",
        "healthy_stamp": "स्वस्थ",
        "diseased_stamp": "रोगग्रस्त",
        "crop_label": "फसल",
        "severity_label": "गंभीरता",
        "confidence_label": "सटीकता",
        "pathogen_prefix": "रोगजनक",
        "low_conf_warning": "सटीकता कम है। बेहतर रोशनी में पत्ते की नज़दीकी तस्वीर पुनः लें।",
        "tab_symptoms": "लक्षण",
        "tab_treatment": "उपचार",
        "tab_care": "देखभाल",
        "tab_fertilizer": "उर्वरक सलाह",
        "tab_prevention": "रोकथाम",
        "organic_title": "जैविक एवं प्राकृतिक उपचार",
        "chemical_title": "रासायनिक नियंत्रण विकल्प",
        "no_mgmt_info": "नियमित खेत निरीक्षण एवं साफ़-सफ़ाई बनाए रखें।",
        "disclaimer": "यह परिणाम AI तकनीक पर आधारित है। बड़े पैमाने पर कीटनाशक छिड़काव से पहले अपने स्थानीय कृषि अधिकारी से सलाह लें।",
        "server_error": "सर्वर इस तस्वीर की जाँच नहीं कर सका",
        "cannot_reach": "सर्वर से कनेक्ट नहीं हो पा रहा है",
        "make_sure_uvicorn": "सुनिश्चित करें कि FastAPI सर्वर चल रहा है: uvicorn api.main:app --reload --port 8000",
        "all_crops": "सभी समर्थित फसलें (स्वतः पहचान)",
    },
}

# ---------------------------------------------------------------------------
# Page configuration & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AgriCure | Crop Health Diagnostics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Kannada:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

    :root {
        --primary: #15803d;
        --primary-dark: #0f5132;
        --primary-light: #dcfce7;
        --border: #cbd5e1;
        --text: #0f172a;
        --clay: #b91c1c;
        --clay-light: #fee2e2;
    }

    /* Greenish Farm Landscape with Soft Ambient Overlay */
    .stApp {
        background:
            linear-gradient(rgba(240, 253, 244, 0.85), rgba(220, 252, 231, 0.88)),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2000&q=80') center / cover no-repeat fixed;
        font-family: 'Plus Jakarta Sans', 'Noto Sans Kannada', 'Noto Sans Devanagari', sans-serif;
        color: var(--text);
    }

    [data-testid="stHeader"] { background: transparent; }
    footer, #MainMenu { visibility: hidden; }

    /* Top Hero Banner */
    .top-header {
        background:
            linear-gradient(135deg, rgba(20, 83, 45, 0.92) 0%, rgba(21, 128, 61, 0.90) 50%, rgba(34, 197, 94, 0.85) 100%),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80') center / cover no-repeat;
        border-radius: 16px;
        padding: 1.75rem 2rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(22, 101, 52, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .top-header h1 {
        color: #ffffff !important;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 800;
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.35);
    }
    .top-header p {
        color: #f0fdf4 !important;
        font-size: 1.05rem;
        margin: 0;
        font-weight: 600;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* Crisp Card Panels over Farm Background */
    .agri-card {
        background: rgba(255, 255, 255, 0.93);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(134, 239, 172, 0.6);
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08);
        margin-bottom: 1.25rem;
    }

    /* Container lifts for widgets */
    div[data-testid="stFileUploader"],
    div[data-testid="stCameraInput"],
    div[data-testid="stSelectbox"] > div {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 10px;
    }

    /* Navigation Radio Bar */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.85);
        padding: 0.4rem 0.8rem;
        border-radius: 12px;
        border: 1px solid rgba(134, 239, 172, 0.5);
        margin-bottom: 1rem;
    }

    /* Primary Buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.05rem;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 4px 14px rgba(21, 128, 61, 0.35);
    }
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(21, 128, 61, 0.45);
    }

    /* Stamps & Badges */
    .stamp-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 800;
        font-size: 0.95rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .stamp-healthy {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        border: 1.5px solid #86efac;
    }
    .stamp-diseased {
        background-color: var(--clay-light);
        color: var(--clay);
        border: 1.5px solid #fca5a5;
    }

    /* Advisory List Items */
    .adv-item {
        padding: 0.75rem 1rem;
        border-left: 4px solid var(--primary);
        background: rgba(255, 255, 255, 0.92);
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.96rem;
        color: #1e293b;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    .adv-chem {
        border-left-color: #ea580c;
        background: rgba(255, 247, 237, 0.95);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# State & Helpers
# ---------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key: str) -> str:
    current = st.session_state.lang
    return I18N.get(current, I18N["en"]).get(key, I18N["en"].get(key, key))

def esc(value: str) -> str:
    return html.escape(str(value))

# Backend URL Resolution
default_api_url = "http://127.0.0.1:8000/predict"
try:
    if "API_URL" in st.secrets:
        default_api_url = str(st.secrets["API_URL"]).strip()
except Exception:
    pass
default_api_url = os.environ.get("API_URL", default_api_url).strip()
if not default_api_url.endswith("/predict"):
    default_api_url = default_api_url.rstrip("/") + "/predict"
if "localhost" in default_api_url:
    default_api_url = default_api_url.replace("localhost", "127.0.0.1")

if "api_url" not in st.session_state:
    st.session_state.api_url = default_api_url

# ---------------------------------------------------------------------------
# Top Bar: Language Selector & App Header
# ---------------------------------------------------------------------------
lang_col1, lang_col2 = st.columns([8, 4])
with lang_col2:
    lang_choice = st.selectbox(
        "🌐 Language / ಭಾಷೆ / भाषा",
        options=["English", "ಕನ್ನಡ (Kannada)", "हिंदी (Hindi)"],
        index=0 if st.session_state.lang == "en" else (1 if st.session_state.lang == "kn" else 2),
        label_visibility="visible",
    )
    if "Kannada" in lang_choice:
        st.session_state.lang = "kn"
    elif "Hindi" in lang_choice:
        st.session_state.lang = "hi"
    else:
        st.session_state.lang = "en"

st.markdown(
    f"""
    <div class="top-header">
        <h1>🌿 {t('app_title').split('|')[0].strip()}</h1>
        <p>{t('tagline')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Top Navigation
# ---------------------------------------------------------------------------
nav_selection = st.radio(
    "Navigation",
    options=[t("nav_diag"), t("nav_crops"), t("nav_tips"), t("nav_settings")],
    horizontal=True,
    label_visibility="collapsed",
)

# ---------------------------------------------------------------------------
# VIEW 1: DIAGNOSTICS (Main Flow)
# ---------------------------------------------------------------------------
if nav_selection == t("nav_diag"):
    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown(f"### {t('step1_title')}")
        crop_options = [
            t("all_crops"),
            "Apple",
            "Bell Pepper",
            "Cherry",
            "Corn (Maize)",
            "Grape",
            "Potato",
            "Strawberry",
            "Tomato",
        ]
        selected_crop = st.selectbox("Crop", options=crop_options, label_visibility="collapsed")

        st.markdown(f"### {t('step2_title')}")
        input_mode = st.radio(
            "Input Mode",
            [f"📁 {t('upload_tab')}", f"📷 {t('camera_tab')}"],
            horizontal=True,
            label_visibility="collapsed",
        )

        chosen_file = None
        if t("upload_tab") in input_mode:
            chosen_file = st.file_uploader(
                t("upload_label"),
                type=["jpg", "jpeg", "png"],
                help=t("upload_hint"),
                label_visibility="collapsed",
            )
        else:
            chosen_file = st.camera_input(t("camera_label"), label_visibility="collapsed")

        image = None
        if chosen_file is not None:
            if chosen_file.size > MAX_UPLOAD_MB * 1024 * 1024:
                st.warning(f"File exceeds {MAX_UPLOAD_MB} MB limit.")
            else:
                try:
                    image = Image.open(io.BytesIO(chosen_file.getvalue()))
                    st.image(image, caption="Uploaded Leaf Specimen", use_container_width=True)
                except Exception as ex:
                    st.error(f"Error loading image: {ex}")
        else:
            st.info(f"💡 {t('tip_text')}")

        check_btn = st.button(t("btn_check"), disabled=(chosen_file is None or image is None), use_container_width=True)

    with right_col:
        st.markdown("### 📋 Diagnostic Report")

        if check_btn and chosen_file is not None:
            with st.spinner(t("btn_checking")):
                try:
                    raw_bytes = chosen_file.getvalue()
                    pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
                    buf = io.BytesIO()
                    pil_img.save(buf, format="JPEG")
                    img_bytes = buf.getvalue()

                    files = {"file": ("leaf.jpg", img_bytes, "image/jpeg")}
                    resp = requests.post(st.session_state.api_url, files=files, timeout=15)

                    if resp.status_code == 200:
                        data = resp.json()
                        is_leaf = data.get("is_leaf", False)

                        if not is_leaf:
                            st.error(f"**{t('not_a_leaf_title')}**")
                            st.write(data.get("message", t("not_a_leaf_msg")))
                        else:
                            crop = data.get("crop", "Unknown")
                            disease = data.get("disease", "Unknown Condition")
                            confidence = float(data.get("confidence", 0.0))
                            raw_label = data.get("raw_label", "")
                            advisory = data.get("advisory") or {}

                            is_healthy = "healthy" in raw_label.lower()
                            stamp_class = "stamp-healthy" if is_healthy else "stamp-diseased"
                            stamp_text = t("healthy_stamp") if is_healthy else t("diseased_stamp")

                            st.markdown(
                                f"""
                                <div class="agri-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                        <span class="stamp-badge {stamp_class}">{stamp_text}</span>
                                        <span style="font-weight: 700; color: #166534; font-size: 1rem;">{t('crop_label')}: {esc(crop)}</span>
                                    </div>
                                    <h2 style="margin: 0 0 0.5rem 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">{esc(disease)}</h2>
                                    <div style="color: #475569; font-size: 0.95rem;">
                                        <span>{t('severity_label')}: <strong>{esc(advisory.get('severity', 'Normal'))}</strong></span>
                                        {f" · <span>{t('pathogen_prefix')}: <strong>{esc(advisory.get('pathogen'))}</strong></span>" if advisory.get('pathogen') and advisory.get('pathogen') != 'N/A' else ""}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            # Confidence Meter
                            st.markdown(f"**{t('confidence_label')}: {confidence:.1f}%**")
                            st.progress(min(max(confidence / 100.0, 0.0), 1.0))
                            if confidence < LOW_CONFIDENCE:
                                st.warning(t("low_conf_warning"))

                            # Advisory Tabs
                            tab_labels = [
                                t("tab_symptoms"),
                                t("tab_care") if is_healthy else t("tab_treatment"),
                                t("tab_fertilizer"),
                                t("tab_prevention"),
                            ]
                            t1, t2, t3, t4 = st.tabs(tab_labels)

                            with t1:
                                syms = advisory.get("symptoms", [])
                                if syms:
                                    for s in syms:
                                        st.markdown(f'<div class="adv-item">{esc(s)}</div>', unsafe_allow_html=True)
                                else:
                                    st.write("No distinct symptoms reported.")

                            with t2:
                                org = advisory.get("organic_solutions", [])
                                chem = advisory.get("chemical_solutions", [])
                                if org:
                                    st.markdown(f"**🌿 {t('organic_title')}**")
                                    for o in org:
                                        st.markdown(f'<div class="adv-item">{esc(o)}</div>', unsafe_allow_html=True)
                                if not is_healthy and chem:
                                    st.markdown(f"**🧪 {t('chemical_title')}**")
                                    for c in chem:
                                        st.markdown(f'<div class="adv-item adv-chem">{esc(c)}</div>', unsafe_allow_html=True)
                                if not org and not chem:
                                    st.write(t("no_mgmt_info"))

                            with t3:
                                ferts = advisory.get("fertilizer_advice", [])
                                if ferts:
                                    for f in ferts:
                                        st.markdown(f'<div class="adv-item">{esc(f)}</div>', unsafe_allow_html=True)
                                else:
                                    st.write("Maintain balanced N-P-K nutrient application.")

                            with t4:
                                prevs = advisory.get("prevention", [])
                                if prevs:
                                    for p in prevs:
                                        st.markdown(f'<div class="adv-item">{esc(p)}</div>', unsafe_allow_html=True)
                                else:
                                    st.write("Follow crop rotation and maintain healthy field airflow.")

                            st.caption(f"⚠️ {t('disclaimer')}")

                    else:
                        st.error(f"{t('server_error')} (Status {resp.status_code})")
                except requests.exceptions.ConnectionError:
                    st.error(t("cannot_reach"))
                    st.info(t("make_sure_uvicorn"))
                except Exception as ex:
                    st.error(f"Error: {ex}")
        else:
            st.info("Upload or photograph a crop leaf on the left, then click **Diagnose Leaf**.")

# ---------------------------------------------------------------------------
# VIEW 2: SUPPORTED CROPS
# ---------------------------------------------------------------------------
elif nav_selection == t("nav_crops"):
    st.markdown("### 🌾 Supported Crop Library")
    crops_grid = [
        {"name": "Tomato (ಟೊಮೆಟೊ / टमाटर)", "conditions": ["Late Blight", "Early Blight", "Leaf Mold", "Healthy"]},
        {"name": "Potato (ಆಲೂಗಡ್ಡೆ / आलू)", "conditions": ["Late Blight", "Early Blight", "Healthy"]},
        {"name": "Corn / Maize (ಮೆಕ್ಕೆಜೋಳ / मक्का)", "conditions": ["Common Rust", "Northern Leaf Blight", "Healthy"]},
        {"name": "Bell Pepper (ದಪ್ಪ ಮೆಣಸಿನಕಾಯಿ / शिमला मिर्च)", "conditions": ["Bacterial Spot", "Healthy"]},
        {"name": "Apple (ಸೇಬು / सेब)", "conditions": ["Apple Scab", "Black Rot", "Cedar Rust", "Healthy"]},
        {"name": "Grape (ದ್ರಾಕ್ಷಿ / अंगूर)", "conditions": ["Black Rot", "Esca", "Leaf Blight", "Healthy"]},
        {"name": "Strawberry (ಸ್ಟ್ರಾಬೆರಿ / स्ट्रॉबेरी)", "conditions": ["Leaf Scorch", "Healthy"]},
        {"name": "Cherry (ಚೆರ್ರಿ / चेरी)", "conditions": ["Powdery Mildew", "Healthy"]},
    ]
    c1, c2 = st.columns(2)
    for idx, c in enumerate(crops_grid):
        target = c1 if idx % 2 == 0 else c2
        with target:
            st.markdown(
                f"""
                <div class="agri-card">
                    <h4 style="margin: 0 0 0.4rem 0; color: #166534; font-weight: 700;">{c['name']}</h4>
                    <div style="font-size: 0.92rem; color: #334155;">
                        <strong>Monitored:</strong> {', '.join(c['conditions'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# VIEW 3: PHOTO TIPS
# ---------------------------------------------------------------------------
elif nav_selection == t("nav_tips"):
    st.markdown(f"### 📸 {t('nav_tips')}")
    st.markdown(
        """
        <div class="agri-card">
            <h4 style="margin: 0 0 0.8rem 0; color: #166534;">How to get 95%+ diagnosis accuracy:</h4>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; color: #1e293b; font-size: 0.98rem;">
                <div>🌿 <strong>Single leaf focus:</strong> Place one leaf against a plain background or your palm.</div>
                <div>☀️ <strong>Natural daylight:</strong> Shoot in morning or afternoon daylight; avoid strong flash glare.</div>
                <div>📐 <strong>Fill the frame:</strong> The leaf and visible disease spots should cover at least 70% of the image.</div>
                <div>🎯 <strong>Steady & sharp:</strong> Ensure the leaf veins and lesion margins are sharply in focus.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# VIEW 4: SYSTEM CONNECTION SETTINGS
# ---------------------------------------------------------------------------
elif nav_selection == t("nav_settings"):
    st.markdown(f"### ⚙️ {t('nav_settings')}")
    with st.form("settings_form"):
        new_url = st.text_input("FastAPI Inference Endpoint", value=st.session_state.api_url)
        submitted = st.form_submit_button("Save Endpoint")
        if submitted:
            st.session_state.api_url = new_url.strip()
            st.success("API Endpoint saved successfully.")

    if st.button("Ping Endpoint"):
        try:
            health_check = st.session_state.api_url.replace("/predict", "/docs")
            r = requests.get(health_check, timeout=3)
            st.success(f"Backend reachable! (Status {r.status_code})")
        except Exception as e:
            st.error(f"Cannot connect to {st.session_state.api_url}: {e}")
