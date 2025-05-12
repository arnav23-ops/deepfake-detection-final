from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from typing import Optional
import uvicorn

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deepfake_detector import DeepfakeDetector

app = FastAPI(
    title="DeepFake Detection API",
    description="API for detecting deepfake images using deep learning",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                     # Local development
        "https://deepfake-detection-final.vercel.app",  # Vercel frontend
        "https://deepfake-detection-final.onrender.com"  # Backend self-reference
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up model path
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'deepfake_model.h5')

# Initialize the detector
detector = DeepfakeDetector(model_path=MODEL_PATH)

# Create temp directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to DeepFake Detection API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Get prediction
        result = detector.predict(file_path)
        
        # Clean up the temporary file
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not remove temporary file: {str(e)}")
        
        if result is None:
            raise HTTPException(status_code=500, detail="Error processing image")
        
        return {
            "is_fake": result['is_fake'],
            "confidence": result['confidence'],
            "raw_score": result['raw_score']
        }
        
    except Exception as e:
        # Clean up in case of error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True) 