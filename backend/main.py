import io
import os
import contextlib
from PIL import Image
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

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Multi-Crop Plant Disease API server...")
    classifier.load_model()
    yield
    print("Multi-Crop Plant Disease API server shut down.")

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
        "service": "AgriCure Multi-Crop API",
        "model_loaded": classifier.is_ready(),
        "supported_classes": len(classifier.classes),
        "crops": ["Apple", "Bell Pepper", "Cherry", "Corn", "Grape", "Potato", "Strawberry", "Tomato"]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not classifier.is_ready():
        raise HTTPException(status_code=503, detail="Model is not ready.")

    # Validate and load image
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    # Step 1: Gatekeeper check - Verify leaf vs non-leaf first
    is_leaf, explanation = leaf_detector.verify_leaf(image)
    if not is_leaf:
        return PredictionResponse(
            is_leaf=False,
            message=explanation,
            confidence=0.0
        )

    # Step 2: Crop disease classification for verified leaves
    try:
        pred_result = classifier.predict(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

    raw_label = pred_result["raw_label"]
    crop = pred_result["crop"]
    disease = pred_result["disease"]
    confidence = pred_result["confidence"]

    # Step 3: Retrieve agronomic advisory & fertilizer care
    raw_advisory = advisory_service.get_advisory(raw_label)
    advisory_obj = None
    if raw_advisory:
        advisory_obj = AdvisoryDetails(**raw_advisory)

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
