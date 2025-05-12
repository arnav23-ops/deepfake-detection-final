import React from 'react';
import {
  Container,
  Typography,
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Paper,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import VerifiedIcon from '@mui/icons-material/Verified';

const steps = [
  {
    label: 'Upload Image',
    description: 'Start by uploading an image you want to analyze. Our system supports JPG, JPEG, and PNG formats.',
    icon: <UploadFileIcon />,
  },
  {
    label: 'Analysis',
    description: 'Our deep learning model analyzes the image for signs of manipulation, looking for patterns and inconsistencies that indicate deepfake content.',
    icon: <AnalyticsIcon />,
  },
  {
    label: 'Results',
    description: 'Get detailed results showing whether the image is real or fake, along with a confidence score indicating the reliability of the prediction.',
    icon: <VerifiedIcon />,
  },
];

const HowItWorks = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          How It Works
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Understanding Our Deepfake Detection Process
        </Typography>
      </Box>

      <Paper sx={{ p: 4, mb: 6 }}>
        <Stepper orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label} active={true}>
              <StepLabel
                StepIconComponent={() => (
                  <Box sx={{ color: 'primary.main' }}>{step.icon}</Box>
                )}
              >
                <Typography variant="h6">{step.label}</Typography>
              </StepLabel>
              <StepContent>
                <Typography variant="body1" color="text.secondary">
                  {step.description}
                </Typography>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </Paper>

      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Technical Details
        </Typography>
        <Typography variant="body1" paragraph>
          Our deepfake detection system uses a sophisticated deep learning model
          based on MobileNetV2 architecture, which has been fine-tuned specifically
          for detecting manipulated images. The model analyzes various features of
          the image, including:
        </Typography>
        <ul>
          <li>
            <Typography variant="body1">
              Facial inconsistencies and artifacts
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Lighting and shadow patterns
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Texture and color distribution
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Geometric distortions
            </Typography>
          </li>
        </ul>
        <Typography variant="body1" paragraph>
          The model has been trained on a diverse dataset of both real and fake
          images, allowing it to identify subtle patterns that indicate image
          manipulation. When you upload an image, it goes through a preprocessing
          pipeline before being analyzed by the model, which then provides a
          prediction along with a confidence score.
        </Typography>
      </Box>
    </Container>
  );
};

export default HowItWorks; 