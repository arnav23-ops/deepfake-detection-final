from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from deepfake_detector import DeepfakeDetector

main = Blueprint('main', __name__)

# Set up model path
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'deepfake_model.h5')

# Initialize the detector
detector = DeepfakeDetector(model_path=MODEL_PATH)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create a temporary file
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                
            filename = secure_filename(file.filename)
            filepath = os.path.join(temp_dir, filename)
            
            # Save the file
            file.save(filepath)
            
            # Get prediction
            result = detector.predict(filepath)
            
            # Clean up the temporary file
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {str(e)}")
            
            if result is None:
                return jsonify({'error': 'Error processing image'}), 500
            
            return jsonify({
                'is_fake': result['is_fake'],
                'confidence': result['confidence'],
                'raw_score': result['raw_score']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}) 