import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { motion } from 'framer-motion';
import { ArrowUpTrayIcon, CameraIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import config from '../config';

const Home = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log(`Sending request to: ${config.apiUrl}/api/predict`);
      const response = await axios.post(`${config.apiUrl}/api/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Response received:', response.data);
      setResult(response.data);
    } catch (err) {
      console.error('API Error:', err);
      if (err.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Response data:', err.response.data);
        console.error('Response status:', err.response.status);
        console.error('Response headers:', err.response.headers);
        setError(err.response.data?.detail || `Error: ${err.response.status}`);
      } else if (err.request) {
        // The request was made but no response was received
        console.error('Request error, no response received:', err.request);
        setError('No response received from server. Please try again later.');
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', err.message);
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.5,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="relative pt-10 pb-20">
      {/* Hero Section */}
      <motion.div 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center"
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        <motion.h1 
          className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight mb-4"
          variants={itemVariants}
        >
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600">
            DeepFake Detection
          </span>
        </motion.h1>
        <motion.p 
          className="max-w-2xl mx-auto text-xl text-gray-500 mb-10"
          variants={itemVariants}
        >
          Upload an image to detect if it's a deepfake or real using our advanced AI technology
        </motion.p>

        {/* Main Content */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div variants={itemVariants} className="w-full">
            <motion.div
              {...getRootProps()}
              className={`group cursor-pointer h-64 border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center transition-all duration-300 ${
                isDragActive 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <input {...getInputProps()} />
              <ArrowUpTrayIcon className={`h-12 w-12 mb-4 transition-colors ${isDragActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-primary-500'}`} />
              <p className="text-lg font-medium text-gray-700">
                {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
              </p>
              <p className="text-sm text-gray-500 mt-1">or click to select a file</p>
              <p className="text-xs text-gray-400 mt-4">Supports JPG, JPEG, PNG</p>
            </motion.div>
          </motion.div>

          {/* Preview Section */}
          <motion.div variants={itemVariants} className="w-full">
            {preview ? (
              <motion.div 
                className="card h-full flex flex-col items-center justify-center p-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <div className="relative w-full flex-1 flex items-center justify-center mb-4 overflow-hidden rounded-lg">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-48 max-w-full object-contain"
                  />
                </div>
                <motion.button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className={`btn-primary w-full py-3 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                  whileHover={{ scale: loading ? 1 : 1.03 }}
                  whileTap={{ scale: loading ? 1 : 0.97 }}
                >
                  {loading ? (
                    <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : (
                    <CameraIcon className="h-5 w-5 mr-2" />
                  )}
                  {loading ? 'Analyzing...' : 'Analyze Image'}
                </motion.button>
              </motion.div>
            ) : (
              <div className="card h-64 flex flex-col items-center justify-center p-6 bg-gray-50">
                <div className="text-center">
                  <CameraIcon className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Image preview will appear here</p>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Result Section */}
        {error && (
          <motion.div 
            className="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <XCircleIcon className="h-5 w-5 text-red-500 mr-2 mt-0.5" />
            <span className="text-red-700">{error}</span>
          </motion.div>
        )}

        {result && (
          <motion.div 
            className="mt-8 card p-6"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Results</h2>
            <div className="flex flex-col md:flex-row justify-between items-center p-4 rounded-lg bg-gray-50">
              <div className="flex-1">
                <div className="flex items-center mb-4">
                  {result.is_fake ? (
                    <XCircleIcon className="h-8 w-8 text-red-500 mr-2" />
                  ) : (
                    <CheckCircleIcon className="h-8 w-8 text-green-500 mr-2" />
                  )}
                  <span className={`text-xl font-semibold ${result.is_fake ? 'text-red-600' : 'text-green-600'}`}>
                    {result.is_fake ? 'Fake Image Detected' : 'Real Image Detected'}
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center">
                    <span className="text-sm text-gray-500 w-24">Confidence:</span>
                    <div className="flex-1 h-4 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${result.is_fake ? 'bg-red-500' : 'bg-green-500'}`}
                        style={{ width: `${(result.confidence * 100).toFixed(2)}%` }}
                      ></div>
                    </div>
                    <span className="ml-2 text-sm font-medium">
                      {(result.confidence * 100).toFixed(2)}%
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Raw score: {result.raw_score.toFixed(4)}
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default Home; 