import cv2
import numpy as np
from skimage import exposure
import os

def preprocess_image(image):
    """Apply mild initial noise reduction."""
    denoised = cv2.fastNlMeansDenoising(image, None, h=10, searchWindowSize=21, templateWindowSize=7)
    return denoised

def enhance_contrast(image):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(image)
    return enhanced

def adjust_gamma(image, gamma=1.0):
    """Adjust image gamma."""
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def sharpen_image(image):
    """Apply sharpening filter."""
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def enhance_psr_image(image_path, output_path, gamma=1.2, sharpen_strength=0.5):
    """Enhance the image and save the result."""
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Preprocessing
    preprocessed = preprocess_image(image)

    # Contrast enhancement
    contrast_enhanced = enhance_contrast(preprocessed)

    # Gamma correction
    gamma_corrected = adjust_gamma(contrast_enhanced, gamma=gamma)

    # Sharpen the image
    sharpened = sharpen_image(gamma_corrected)

    # Blend sharpened image with gamma corrected image
    final_enhanced = cv2.addWeighted(gamma_corrected, 1 - sharpen_strength, sharpened, sharpen_strength, 0)

    # Final contrast enhancement
    final_enhanced = enhance_contrast(final_enhanced)

    # Save the result
    cv2.imwrite(output_path, final_enhanced)

    return output_path  # Return path of enhanced image
