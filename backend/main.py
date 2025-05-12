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

# Configure CORS - use "*" to allow all origins during troubleshooting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins while debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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

# Add OPTIONS method for CORS preflight requests
@app.options("/api/predict")
async def options_predict():
    return {}

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    # Print debug information
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"File saved at: {file_path}")
        
        # Get prediction
        result = detector.predict(file_path)
        print(f"Prediction result: {result}")
        
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
        print(f"Error processing request: {str(e)}")
        # Clean up in case of error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True) 