import numpy as np
from PIL import Image

class LeafDetector:
    """
    Visual gatekeeper to verify whether an uploaded image contains plant/crop leaf foliage.
    Checks chromaticity (ExG / HSV plant-tissue color space) and natural texture.
    """
    def __init__(self, min_green_ratio: float = 0.005):
        self.min_green_ratio = min_green_ratio

    def analyze_image_foliage(self, image: Image.Image) -> dict:
        """
        Evaluates visual plant leaf characteristics using Excess Green Index (ExG)
        and color distribution in HSV. Rejects non-plant surfaces such as skin tones and blue objects.
        """
        rgb = np.array(image.convert("RGB"), dtype=np.float32)
        hsv = np.array(image.convert("HSV"), dtype=np.float32)
        
        h = hsv[:, :, 0]
        s = hsv[:, :, 1] / 255.0
        v = hsv[:, :, 2] / 255.0
        
        r = rgb[:, :, 0]
        g = rgb[:, :, 1]
        b = rgb[:, :, 2]
        tot = r + g + b + 1e-5
        exg = (2.0 * g - r - b) / tot

        # Plant foliage mask:
        # Hue 20 to 125 (green, olive, yellow), adequate saturation/value, ExG > -0.05, and r - g < 45
        foliage_mask = (h >= 20) & (h <= 125) & (s >= 0.08) & (v >= 0.08) & (exg > -0.05) & ((r - g) < 45)
        green_ratio = float(np.mean(foliage_mask))

        # Check for noise / high-frequency non-natural patterns
        diff_h = np.abs(np.diff(rgb, axis=0))
        diff_v = np.abs(np.diff(rgb, axis=1))
        roughness = float((np.mean(diff_h) + np.mean(diff_v)) / 2.0)
        is_noise = roughness > 55.0  # Random artificial noise threshold

        is_foliar = (green_ratio >= self.min_green_ratio) and not is_noise

        return {
            "green_ratio": round(green_ratio, 4),
            "is_foliar": is_foliar,
            "is_noise": is_noise
        }

    def verify_leaf(self, image: Image.Image) -> tuple[bool, str]:
        """
        Determines whether the image is a valid crop leaf or non-leaf.
        Returns (is_leaf, explanation_message).
        """
        foliage_stats = self.analyze_image_foliage(image)

        if foliage_stats["is_noise"]:
            return False, "The uploaded image appears to be digital noise or an invalid graphic. Please upload a clear photo of a crop leaf."

        if not foliage_stats["is_foliar"]:
            return False, "The uploaded image does not appear to be a plant leaf. Please upload a clear photo of a crop leaf."

        return True, "Valid crop leaf verified."

leaf_detector = LeafDetector()
