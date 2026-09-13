from typing import List, Optional
from pydantic import BaseModel

class AdvisoryDetails(BaseModel):
    crop: str
    condition: str
    pathogen: str
    type: str
    severity: str
    symptoms: List[str]
    organic_solutions: List[str]
    chemical_solutions: List[str]
    fertilizer_advice: List[str]
    prevention: List[str]

class PredictionResponse(BaseModel):
    is_leaf: bool
    message: Optional[str] = None
    crop: Optional[str] = None
    disease: Optional[str] = None
    raw_label: Optional[str] = None
    confidence: Optional[float] = None
    advisory: Optional[AdvisoryDetails] = None
