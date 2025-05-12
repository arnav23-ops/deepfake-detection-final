import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
} from '@mui/material';
import SecurityIcon from '@mui/icons-material/Security';
import SpeedIcon from '@mui/icons-material/Speed';
import PsychologyIcon from '@mui/icons-material/Psychology';

const About = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          About Our Project
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          A Deep Learning Solution for Deepfake Detection
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <SecurityIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Our Mission
              </Typography>
              <Typography variant="body1" color="text.secondary">
                To provide a reliable and accessible tool for detecting deepfake images,
                helping to combat the spread of misinformation and protect digital media integrity.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <SpeedIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Technology
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Built using state-of-the-art deep learning techniques, our system
                leverages convolutional neural networks to analyze and detect
                manipulated images with high accuracy.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <PsychologyIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Innovation
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Our solution combines advanced AI algorithms with user-friendly
                interfaces to make deepfake detection accessible to everyone.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Project Details
        </Typography>
        <Typography variant="body1" paragraph>
          This project was developed as a final year project, focusing on the growing
          concern of deepfake technology and its potential misuse. Our goal was to
          create a practical solution that could help identify manipulated images
          and contribute to the fight against digital misinformation.
        </Typography>
        <Typography variant="body1" paragraph>
          The system uses a deep learning model trained on a diverse dataset of
          real and fake images, enabling it to detect subtle patterns and
          inconsistencies that indicate image manipulation.
        </Typography>
      </Box>
    </Container>
  );
};

export default About; 