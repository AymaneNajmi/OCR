"""
Food-IA: Meal predictor using trained model
This module handles predictions on food images
"""

import os
import pickle
import numpy as np
import cv2
import tensorflow as tf
from pathlib import Path

# Paths to model artifacts
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'food_model_trained.h5')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')
CLASSES_PATH = os.path.join(MODEL_DIR, 'classes.pkl')

# Image configuration
IMAGE_SIZE = (224, 224)

class FoodRecognizer:
    """Predict meal type from food image using trained CNN"""
    
    def __init__(self, model_path=MODEL_PATH, encoder_path=ENCODER_PATH, classes_path=CLASSES_PATH):
        """Initialize the recognizer with trained model"""
        self.model = None
        self.label_encoder = None
        self.classes = None
        self.model_loaded = False
        
        self.load_model(model_path, encoder_path, classes_path)
    
    def load_model(self, model_path, encoder_path, classes_path):
        """Load trained model and artifacts"""
        try:
            # Check if files exist
            if not os.path.exists(model_path):
                print(f"⚠️  Model not found at {model_path}")
                print(f"   Please run: python train_model.py")
                return False
            
            # Load model
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded: {model_path}")
            
            # Load label encoder
            if os.path.exists(encoder_path):
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print(f"✅ Label encoder loaded")
            
            # Load classes
            if os.path.exists(classes_path):
                with open(classes_path, 'rb') as f:
                    self.classes = pickle.load(f)
                print(f"✅ Classes loaded: {len(self.classes)} dishes")
            
            self.model_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def preprocess_image(self, img):
        """Preprocess image for model input"""
        try:
            if isinstance(img, str):
                # Load from file path
                img = cv2.imread(img)
                if img is None:
                    return None
            
            # Resize to model input size
            img_resized = cv2.resize(img, IMAGE_SIZE)
            
            # Normalize
            img_normalized = img_resized.astype('float32') / 255.0
            
            # Add batch dimension
            img_batch = np.expand_dims(img_normalized, axis=0)
            
            return img_batch
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_input, top_k=3):
        """
        Predict meal type from image
        
        Args:
            image_input: File path (str) or numpy array (image)
            top_k: Return top K predictions
        
        Returns:
            dict with keys:
                - 'meal': Most likely meal name
                - 'confidence': Confidence (0-100%)
                - 'top_predictions': List of (meal, confidence) tuples
                - 'success': Whether prediction was successful
        """
        
        result = {
            'meal': None,
            'confidence': 0,
            'top_predictions': [],
            'success': False
        }
        
        # Check if model is loaded
        if not self.model_loaded:
            print("❌ Model not loaded. Train model first: python train_model.py")
            return result
        
        # Preprocess image
        img_batch = self.preprocess_image(image_input)
        if img_batch is None:
            print("❌ Failed to preprocess image")
            return result
        
        try:
            # Make prediction
            predictions = self.model.predict(img_batch, verbose=0)
            pred_probs = predictions[0]
            
            # Get top K predictions
            top_indices = np.argsort(pred_probs)[::-1][:top_k]
            
            for rank, idx in enumerate(top_indices):
                confidence = float(pred_probs[idx]) * 100
                meal_name = self.classes[idx] if self.classes else f"Class {idx}"
                
                if rank == 0:
                    result['meal'] = meal_name
                    result['confidence'] = confidence
                
                result['top_predictions'].append((meal_name, confidence))
            
            result['success'] = True
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
        
        return result
    
    def get_meal_calories(self, meal_name, nutrition_db=None):
        """
        Get calories for a meal (placeholder for nutrition database)
        In production, integrate with actual nutrition DB
        """
        if nutrition_db is None:
            nutrition_db = {}
        
        # Return calorie value if available, else estimate based on meal type
        if meal_name in nutrition_db:
            return nutrition_db[meal_name]
        
        # Simple heuristic: estimate based on keywords in meal name
        name_lower = meal_name.lower()
        
        if any(x in name_lower for x in ['salad', 'salade', 'soup', 'soupe']):
            return 200
        elif any(x in name_lower for x in ['pasta', 'pâte', 'rice', 'riz']):
            return 350
        elif any(x in name_lower for x in ['steak', 'meat', 'viande', 'fish', 'poisson']):
            return 400
        elif any(x in name_lower for x in ['pizza', 'burger']):
            return 500
        elif any(x in name_lower for x in ['cake', 'dessert', 'gâteau']):
            return 300
        else:
            return 250  # Default estimate


# Global recognizer instance (lazy loaded)
_recognizer = None

def get_recognizer():
    """Get or create global recognizer instance"""
    global _recognizer
    if _recognizer is None:
        _recognizer = FoodRecognizer()
    return _recognizer

def predict_meal(image_input):
    """Quick prediction function"""
    recognizer = get_recognizer()
    return recognizer.predict(image_input)
