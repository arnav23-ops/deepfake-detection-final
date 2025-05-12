import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2
from PIL import Image
import os
from sklearn.model_selection import train_test_split
import glob

class DeepfakeDetector:
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
        else:
            self.model = self._build_model()
        self.input_size = (128, 128)  # Input size for the model
        self.data_augmentation = tf.keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.2),
            layers.RandomZoom(0.2),
            layers.RandomContrast(0.2),
        ])
    
    def _build_model(self):
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(128, 128, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False  # Freeze base model

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        return model

    def load_dataset(self, real_dir, fake_dir):
        """Load and preprocess the dataset, recursively including images in all subfolders."""
        real_images = []
        fake_images = []

        # Recursively find all images in real_dir
        for root, _, files in os.walk(real_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    try:
                        img = cv2.imread(img_path)
                        if img is not None:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, self.input_size)
                            real_images.append(img)
                    except Exception as e:
                        print(f"Error loading image {img_path}: {str(e)}")

        # Recursively find all images in fake_dir
        for root, _, files in os.walk(fake_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    try:
                        img = cv2.imread(img_path)
                        if img is not None:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, self.input_size)
                            fake_images.append(img)
                    except Exception as e:
                        print(f"Error loading image {img_path}: {str(e)}")

        # Convert to numpy arrays
        X_real = np.array(real_images)
        X_fake = np.array(fake_images)

        # Create labels
        y_real = np.zeros(len(real_images))
        y_fake = np.ones(len(fake_images))

        # Combine real and fake data
        X = np.concatenate([X_real, X_fake])
        y = np.concatenate([y_real, y_fake])

        # Normalize pixel values
        X = X.astype('float32') / 255.0

        return X, y
    
    def fine_tune(self, train_ds, val_ds, initial_epochs=10, fine_tune_epochs=5):
        # Unfreeze the last 20 layers of the base model for fine-tuning
        base_model = self.model.layers[0]
        base_model.trainable = True
        for layer in base_model.layers[:-20]:
            layer.trainable = False
        # Recompile with a lower learning rate
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                           loss='binary_crossentropy',
                           metrics=['accuracy'])
        history_fine = self.model.fit(
            train_ds,
            epochs=initial_epochs + fine_tune_epochs,
            initial_epoch=initial_epochs,
            validation_data=val_ds,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                )
            ]
        )
        return history_fine

    def train(self, real_dir, fake_dir, epochs=10, batch_size=32, validation_split=0.2, fine_tune_epochs=5):
        print("Loading dataset...")
        X, y = self.load_dataset(real_dir, fake_dir)
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42
        )
        print(f"Training on {len(X_train)} images, validating on {len(X_val)} images")

        def augment(x, y):
            return self.data_augmentation(x), y

        train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_ds = train_ds.shuffle(buffer_size=100).map(augment).batch(batch_size).prefetch(tf.data.AUTOTUNE)
        val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(batch_size).prefetch(tf.data.AUTOTUNE)

        # Initial training (feature extraction)
        history = self.model.fit(
            train_ds,
            epochs=epochs,
            validation_data=val_ds,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                )
            ]
        )
        # Fine-tuning phase
        print("\nStarting fine-tuning phase...")
        self.fine_tune(train_ds, val_ds, initial_epochs=epochs, fine_tune_epochs=fine_tune_epochs)
        return history
    
    def save_model(self, model_path):
        """Save the trained model"""
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
    
    def preprocess_image(self, image_path):
        """Preprocess the input image for model prediction"""
        try:
            # Convert to absolute path if it's not already
            abs_path = os.path.abspath(image_path)
            
            # Check if file exists
            if not os.path.exists(abs_path):
                print(f"Error: File not found at {abs_path}")
                return None
                
            # Read and resize image
            img = cv2.imread(abs_path)
            if img is None:
                print(f"Error: Could not read image at {abs_path}")
                return None
                
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, self.input_size)
            
            # Normalize pixel values
            img = img.astype('float32') / 255.0
            
            # Add batch dimension
            img = np.expand_dims(img, axis=0)
            
            return img
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_path):
        """Predict if the image is real or fake"""
        # Preprocess the image
        processed_img = self.preprocess_image(image_path)
        
        if processed_img is None:
            return None
        
        # Make prediction
        prediction = self.model.predict(processed_img)[0][0]
        
        # Print raw prediction value for debugging
        print(f"Raw prediction value: {prediction}")
        
        # Use a more balanced threshold
        threshold = 0.5
        
        # Return result
        result = {
            'is_fake': bool(prediction > threshold),
            'confidence': float(prediction if prediction > threshold else 1 - prediction),
            'raw_score': float(prediction)  # Add raw score to output
        }
        
        return result

def main():
    # Initialize the detector
    detector = DeepfakeDetector()
    
    # Training mode
    if len(sys.argv) > 1 and sys.argv[1] == '--train':
        if len(sys.argv) != 4:
            print("Usage: python deepfake_detector.py --train <real_images_dir> <fake_images_dir>")
            return
        
        real_dir = sys.argv[2]
        fake_dir = sys.argv[3]
        
        print("Starting training...")
        history = detector.train(real_dir, fake_dir)
        detector.save_model('deepfake_model.h5')
        print("Training completed!")
        return
    
    # Prediction mode
    print("Deepfake Detection System")
    print("------------------------")
    
    while True:
        image_path = input("\nEnter the path to the image (or 'q' to quit): ")
        
        if image_path.lower() == 'q':
            break
            
        if not os.path.exists(image_path):
            print("Error: File not found!")
            continue
            
        result = detector.predict(image_path)
        
        if result is None:
            print("Error processing the image!")
            continue
            
        print("\nResults:")
        print(f"Prediction: {'Fake' if result['is_fake'] else 'Real'}")
        print(f"Confidence: {result['confidence']*100:.2f}%")
        print(f"Raw Score: {result['raw_score']:.4f}")  # Print raw score

if __name__ == "__main__":
    import sys
    main() 