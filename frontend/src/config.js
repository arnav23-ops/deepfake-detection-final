// API Configuration
const config = {
  // Priority:
  // 1. Use environment variable if available
  // 2. Use production URL if in production mode
  // 3. Fall back to localhost for development
  apiUrl: process.env.REACT_APP_API_URL || 
          (process.env.NODE_ENV === 'production' 
            ? 'https://deepfake-detection-final.onrender.com/api' 
            : 'http://localhost:5000/api')
};

export default config; 