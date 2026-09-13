import base64
import os
import io
import requests
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AgriCure | Multi-Crop Disease Diagnostic & Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and encode background image
BG_IMAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "assets", "farmer_bg.jpg")
)

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

bg_base64 = get_base64_of_bin_file(BG_IMAGE_PATH)
bg_style = ""
if bg_base64:
    bg_style = f"""
    .stApp {{
        background-image: linear-gradient(rgba(240, 246, 240, 0.88), rgba(230, 242, 230, 0.88)), url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

# Custom CSS for Agriculture-themed UI
st.markdown(f"""
<style>
    {bg_style}
    
    /* Main container styling */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }}

    .hero-header {{
        background: linear-gradient(135deg, #1B5E20, #2E7D32, #388E3C);
        padding: 1.6rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(27, 94, 32, 0.25);
        text-align: center;
    }}
    .hero-title {{
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
    }}
    .hero-subtitle {{
        font-size: 1.05rem;
        margin-top: 0.5rem;
        color: #E8F5E9;
        font-weight: 400;
    }}

    .crop-pills {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-top: 1rem;
    }}
    .crop-pill {{
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85rem;
        color: #FFFFFF;
        font-weight: 500;
    }}

    /* Card styling */
    .glass-card {{
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(8px);
        border: 1px solid #C8E6C9;
        border-radius: 14px;
        padding: 1.4rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.2rem;
    }}

    .diag-banner {{
        padding: 1.4rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
        border-left: 8px solid;
    }}
    .diag-healthy {{
        background: #E8F5E9;
        border-color: #2E7D32;
        color: #1B5E20;
    }}
    .diag-warning {{
        background: #FFF8E1;
        border-color: #F57F17;
        color: #BF360C;
    }}
    .diag-danger {{
        background: #FFEBEE;
        border-color: #C62828;
        color: #B71C1C;
    }}
    .diag-nonleaf {{
        background: #FFF3E0;
        border-color: #E65100;
        color: #BF360C;
    }}

    .badge {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 6px;
    }}
    .badge-crop {{
        background: #E8F5E9;
        color: #1B5E20;
        border: 1px solid #A5D6A7;
    }}
    .badge-severity-high {{
        background: #FFCDD2;
        color: #B71C1C;
    }}
    .badge-severity-mod {{
        background: #FFE082;
        color: #E65100;
    }}
    .badge-severity-none {{
        background: #C8E6C9;
        color: #2E7D32;
    }}

    /* Advisory section styling */
    .advisory-item {{
        background: #F1F8E9;
        border-left: 4px solid #4CAF50;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }}
</style>
""", unsafe_allow_html=True)

# Hero Header Banner
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">🌾 AgriCure AI: Multi-Crop Disease & Advisory</h1>
    <p class="hero-subtitle">Instant Deep-Learning Diagnosis & Practical Agronomic Solutions for 8 Major Crops</p>
    <div class="crop-pills">
        <span class="crop-pill">🍏 Apple</span>
        <span class="crop-pill">🫑 Bell Pepper</span>
        <span class="crop-pill">🍒 Cherry</span>
        <span class="crop-pill">🌽 Corn</span>
        <span class="crop-pill">🍇 Grape</span>
        <span class="crop-pill">🥔 Potato</span>
        <span class="crop-pill">🍓 Strawberry</span>
        <span class="crop-pill">🍅 Tomato</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Resolve default backend API URL: 1) Streamlit secrets, 2) Environment variable, 3) Localhost default
default_api_url = "http://localhost:8000/predict"
try:
    if "API_URL" in st.secrets:
        default_api_url = str(st.secrets["API_URL"]).strip()
except Exception:
    pass

if default_api_url == "http://localhost:8000/predict":
    default_api_url = os.environ.get("API_URL", default_api_url).strip()

if not default_api_url.endswith("/predict"):
    default_api_url = default_api_url.rstrip("/") + "/predict"

# Sidebar
with st.sidebar:
    if os.path.exists(BG_IMAGE_PATH):
        st.image(BG_IMAGE_PATH, use_container_width=True, caption="AgriCure Agricultural Network")
    st.markdown("### ⚙️ System Settings")
    api_url = st.text_input(
        "Backend API Endpoint",
        value=default_api_url,
        help="FastAPI prediction endpoint URL. Can be set via Streamlit Secrets (API_URL)."
    )
    
    st.markdown("---")
    st.markdown("### 🌿 Diagnostic Protocol")
    st.markdown("""
    1. **Leaf Verification**: Verifies image contains valid crop foliage.
    2. **Disease Diagnosis**: Evaluates 31 conditions across 8 crops.
    3. **Treatment Advisory**: Provides organic remedies, chemical options, and fertilizer adjustments.
    """)
    st.markdown("---")
    st.caption("AgriCure AI Engine • Powered by MobileNetV2 Transfer Learning")

# Main Content Layout (2 Columns)
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📸 Upload Crop Leaf Photo")
    st.write("Take or upload a clear photo of the suspected plant leaf.")

    uploaded_file = st.file_uploader(
        "Choose leaf image file...",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    image = None
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Selected: {uploaded_file.name}", use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load image: {str(e)}")

    diagnose_clicked = st.button(
        "🔍 Analyze & Diagnose Leaf",
        type="primary",
        use_container_width=True,
        disabled=(image is None)
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if not diagnose_clicked and image is None:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2.5rem 1.5rem;">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🌱</div>
            <h3 style="color: #1B5E20; margin-bottom: 0.5rem;">Ready for Crop Leaf Analysis</h3>
            <p style="color: #555555; max-width: 450px; margin: 0 auto; line-height: 1.6;">
                Upload a photo of an Apple, Bell Pepper, Cherry, Corn, Grape, Potato, Strawberry, or Tomato leaf. 
                Our AI will check for disease symptoms and provide actionable fertilizer & care guidance.
            </p>
            <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 15px; font-size: 0.85rem; color: #666;">
                <span>✅ Leaf Detection</span>
                <span>✅ 31 Diseases</span>
                <span>✅ Fertilizer Advice</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif image is not None and not diagnose_clicked:
        st.info("👆 Click **'🔍 Analyze & Diagnose Leaf'** on the left to start the diagnostic scan.")

    elif diagnose_clicked and image is not None:
        with st.spinner("🔬 Examining leaf tissue and calculating agronomic parameters..."):
            try:
                # Prepare payload
                img_byte_arr = io.BytesIO()
                image.convert("RGB").save(img_byte_arr, format="JPEG")
                img_bytes = img_byte_arr.getvalue()

                files = {"file": (uploaded_file.name, img_bytes, "image/jpeg")}
                response = requests.post(api_url, files=files, timeout=12)

                if response.status_code == 200:
                    data = response.json()
                    is_leaf = data.get("is_leaf", False)
                    message = data.get("message", "")

                    # 1. Non-leaf rejection case
                    if not is_leaf:
                        st.markdown(f"""
                        <div class="diag-banner diag-nonleaf">
                            <h3 style="margin: 0 0 0.5rem 0;">⚠️ Non-Leaf Image Detected</h3>
                            <p style="margin: 0; font-size: 1.05rem;">{message}</p>
                            <p style="margin-top: 0.8rem; font-size: 0.88rem; color: #795548;">
                                💡 <strong>Tip</strong>: Place the affected crop leaf on a neutral surface or take a close-up photo in bright daylight. Avoid uploading pictures of people, objects, or indoor furniture.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    # 2. Valid Leaf Diagnosis case
                    else:
                        crop = data.get("crop", "Unknown Crop")
                        disease = data.get("disease", "Unknown Condition")
                        confidence = data.get("confidence", 0.0)
                        raw_label = data.get("raw_label", "")
                        advisory = data.get("advisory", {})

                        # Determine alert color
                        is_healthy = "healthy" in raw_label.lower()
                        banner_class = "diag-healthy" if is_healthy else ("diag-danger" if confidence > 85 else "diag-warning")
                        icon = "✅" if is_healthy else "🚨"

                        severity = advisory.get("severity", "Normal") if advisory else "Normal"
                        severity_badge = "badge-severity-none" if is_healthy else ("badge-severity-high" if "high" in severity.lower() or "critical" in severity.lower() else "badge-severity-mod")

                        st.markdown(f"""
                        <div class="diag-banner {banner_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <div>
                                    <span class="badge badge-crop">🌾 {crop}</span>
                                    <span class="badge {severity_badge}">Severity: {severity}</span>
                                </div>
                                <span style="font-size: 0.9rem; font-weight: 700;">Confidence: {confidence:.2f}%</span>
                            </div>
                            <h2 style="margin: 0.2rem 0; font-size: 1.8rem;">{icon} {disease}</h2>
                            <p style="margin: 0; font-size: 0.92rem; opacity: 0.9;"><strong>Pathogen:</strong> {advisory.get('pathogen', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.progress(min(max(confidence / 100.0, 0.0), 1.0))

                        # Advisory Tabs
                        if advisory:
                            tab_symptoms, tab_organic, tab_chemical, tab_fertilizer, tab_prev = st.tabs([
                                "🔍 Symptoms",
                                "🌿 Organic Care",
                                "🧪 Chemical Controls",
                                "🌾 Fertilizer Advice",
                                "🛡️ Prevention"
                            ])

                            with tab_symptoms:
                                st.markdown("#### Visual Diagnostic Signs")
                                for s in advisory.get("symptoms", []):
                                    st.markdown(f"<div class='advisory-item'>• {s}</div>", unsafe_allow_html=True)

                            with tab_organic:
                                st.markdown("#### Organic & Biological Treatments")
                                for o in advisory.get("organic_solutions", []):
                                    st.markdown(f"<div class='advisory-item'>🌱 {o}</div>", unsafe_allow_html=True)

                            with tab_chemical:
                                st.markdown("#### Conventional Chemical Controls")
                                if is_healthy:
                                    st.info("No chemical fungicides or bactericides required for healthy plants.")
                                else:
                                    for c in advisory.get("chemical_solutions", []):
                                        st.markdown(f"<div class='advisory-item'>⚠️ {c}</div>", unsafe_allow_html=True)

                            with tab_fertilizer:
                                st.markdown("#### Fertilizer & Soil Nutrient Management")
                                for f in advisory.get("fertilizer_advice", []):
                                    st.markdown(f"<div class='advisory-item'>🧪 {f}</div>", unsafe_allow_html=True)

                            with tab_prev:
                                st.markdown("#### Cultural Practices & Crop Rotation")
                                for p in advisory.get("prevention", []):
                                    st.markdown(f"<div class='advisory-item'>🛡️ {p}</div>", unsafe_allow_html=True)

                else:
                    st.error(f"API Server Error ({response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    f"❌ **Backend Disconnected**\n\n"
                    f"Could not connect to `{api_url}`.\n\n"
                    f"Please launch the FastAPI backend server:\n"
                    f"```powershell\npython -m uvicorn api.main:app --reload --port 8000\n```"
                )
            except Exception as e:
                st.error(f"An error occurred during diagnosis: {str(e)}")
