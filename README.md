# DeepFake Detection System

A full-stack web application for detecting deepfake images using deep learning. This project was developed as a final year project to help combat the spread of manipulated images.

## Features

- Real-time deepfake detection using deep learning
- Modern, responsive web interface
- Detailed analysis results with confidence scores
- Multiple pages including About, How It Works, and Contact
- RESTful API backend

## Tech Stack

### Frontend
- React.js
- Material-UI
- Axios for API calls
- React Router for navigation

### Backend
- Flask (Python)
- TensorFlow
- OpenCV
- scikit-learn

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd deepfake-detection-system
```

2. Set up the Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
# From the root directory
cd backend
python run.py
```

2. Start the frontend development server:
```bash
# From the frontend directory
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Project Structure

```
deepfake-detection-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/
│   ├── templates/
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   ├── public/
│   └── package.json
├── deepfake_model.h5
├── deepfake_detector.py
└── requirements.txt
```

## API Endpoints

- `POST /api/predict`: Upload and analyze an image
- `GET /api/health`: Check API health status

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DeepFake TIMIT dataset
- TensorFlow and Keras
- Material-UI
- React.js community 