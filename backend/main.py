import io
import os
import logging
import contextlib
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Flexible imports supporting both root-level and subfolder execution
try:
    from backend.classifier import classifier
    from backend.leaf_detector import leaf_detector
    from backend.advisory import advisory_service
    from backend.schemas import PredictionResponse, AdvisoryDetails
except ImportError:
    from classifier import classifier
    from leaf_detector import leaf_detector
    from advisory import advisory_service
    from schemas import PredictionResponse, AdvisoryDetails

# Configure server-side logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("agricure.backend")

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".jfif", ".mpo"}

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Multi-Crop Plant Disease Cloud API server...")
    if not classifier.is_ready():
        classifier.load_model()
    yield
    logger.info("Multi-Crop Plant Disease Cloud API server shut down.")

app = FastAPI(
    title="Multi-Crop Plant Disease Detection & Advisory API",
    description="Deep Learning API for leaf verification, multi-crop disease classification (8 crops, 31 classes), and crop-care advisory.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/ping")
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "AgriCure Multi-Crop Production API",
        "model_loaded": classifier.is_ready(),
        "supported_classes": len(classifier.classes),
        "crops": ["Apple", "Bell Pepper", "Cherry", "Corn", "Grape", "Potato", "Strawberry", "Tomato"]
    }

@app.get("/predict")
async def predict_get_info():
    return {
        "message": "AgriCure Prediction Endpoint",
        "usage": "Send an HTTP POST request with a multipart/form-data payload containing 'file' (JPG/PNG image).",
        "frontend": "Access the Streamlit Community Cloud frontend application."
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not classifier.is_ready():
        logger.info("Lazy loading production model for prediction...")
        try:
            classifier.load_model()
        except Exception as e:
            logger.error(f"Lazy model load failed: {e}", exc_info=True)
            raise HTTPException(status_code=503, detail="Model is not ready.")

    # 1. Filename / Extension check
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext and ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Rejected file '{filename}': unsupported extension '{ext}'")
        raise HTTPException(
            status_code=400,
            detail="Unsupported file extension. Only JPG, JPEG, and PNG images are allowed."
        )

    # 2. Read content & validate size
    try:
        content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read uploaded file stream: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="Could not read uploaded file.")

    if not content or len(content) == 0:
        logger.warning(f"Rejected file '{filename}': empty file (0 bytes)")
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE_BYTES:
        logger.warning(f"Rejected file '{filename}': size {len(content)} bytes exceeds 10 MB limit")
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of 10 MB (uploaded {len(content) / (1024 * 1024):.1f} MB)."
        )

    # 3. Pillow Image decoding & mode conversion
    try:
        image = Image.open(io.BytesIO(content))
        image.load()  # Force decoding image raster pixels
        if image.mode != "RGB":
            image = image.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as e:
        logger.warning(f"Invalid image format for '{filename}': {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Please upload a valid, uncorrupted JPG or PNG photo."
        )
    except Exception as e:
        logger.error(f"Unexpected error parsing image '{filename}': {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Could not process image file. Please ensure it is a valid JPG or PNG photo."
        )

    # 4. Step 1: Gatekeeper check - Verify leaf vs non-leaf
    try:
        is_leaf, explanation = leaf_detector.verify_leaf(image)
    except Exception as e:
        logger.error(f"Error during leaf verification for '{filename}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during leaf verification."
        )

    if not is_leaf:
        return PredictionResponse(
            is_leaf=False,
            message=explanation,
            confidence=0.0
        )

    # 5. Step 2: Crop disease classification for verified leaves
    try:
        pred_result = classifier.predict(image)
    except Exception as e:
        logger.error(f"Inference error for '{filename}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during disease classification."
        )

    raw_label = pred_result["raw_label"]
    crop = pred_result["crop"]
    disease = pred_result["disease"]
    confidence = pred_result["confidence"]

    # 6. Step 3: Retrieve agronomic advisory & fertilizer care
    try:
        raw_advisory = advisory_service.get_advisory(raw_label)
        advisory_obj = None
        if raw_advisory:
            advisory_obj = AdvisoryDetails(**raw_advisory)
    except Exception as e:
        logger.error(f"Advisory lookup error for '{raw_label}': {e}", exc_info=True)
        advisory_obj = None

    diag_message = "Valid plant leaf diagnosed successfully."
    if confidence < 50.0:
        diag_message = f"Valid plant leaf diagnosed. Note: Confidence is moderate ({confidence:.1f}%); symptoms may be early-stage or ambiguous."

    return PredictionResponse(
        is_leaf=True,
        message=diag_message,
        crop=crop,
        disease=disease,
        raw_label=raw_label,
        confidence=confidence,
        advisory=advisory_obj
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
