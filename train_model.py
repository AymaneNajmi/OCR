"""
Food-IA: Training script to train the CNN model on actual food images
This script loads the dataset, trains the model, and saves it for production use.
"""

import os
import sys
import numpy as np
import pandas as pd
import cv2
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import IMAGES_DIR, CSV_FILE

# Configuration
IMAGE_SIZE = (224, 224)  # Larger size for better feature extraction
BATCH_SIZE = 32
EPOCHS = 15
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1
MIN_IMAGES_PER_CLASS = 5  # Minimum images to include a class
RANDOM_STATE = 42

# Paths
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'food_model_trained.h5')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')
CLASSES_PATH = os.path.join(MODEL_DIR, 'classes.pkl')

def create_model_directory():
    """Create models directory if it doesn't exist"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"✅ Models directory ready: {MODEL_DIR}")

def load_and_prepare_data():
    """Load CSV and filter images that exist"""
    print("\n📊 Loading dataset...")
    
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"   Total records in CSV: {len(df)}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None, None, None
    
    # Detect column names
    cols_lower = {c.lower(): c for c in df.columns}
    
    def find_col(possible_names):
        for name in possible_names:
            if name.lower() in cols_lower:
                return cols_lower[name.lower()]
        for name in df.columns:
            for p in possible_names:
                if p.lower() in name.lower():
                    return name
        return None
    
    title_col = find_col(['title', 'name', 'dish', 'recipe'])
    image_col = find_col(['image_name', 'imagename', 'image', 'image_id', 'file_name', 'filename'])
    
    if title_col is None or image_col is None:
        print(f"❌ Required columns not found!")
        print(f"   Available columns: {list(df.columns)}")
        return None, None, None
    
    print(f"   Using columns: title='{title_col}', image='{image_col}'")
    
    # Remove duplicates and null values
    df = df.dropna(subset=[image_col, title_col])
    df = df.drop_duplicates(subset=[image_col])
    
    # Build list of valid image paths and labels
    images_data = []
    valid_count = 0
    missing_count = 0
    
    for _, row in df.iterrows():
        raw_img_name = str(row[image_col])
        img_name = raw_img_name if raw_img_name.lower().endswith(('.jpg', '.jpeg', '.png')) else raw_img_name + ".jpg"
        img_path = os.path.join(IMAGES_DIR, img_name)
        
        # Check if file exists
        if os.path.exists(img_path):
            images_data.append({
                'path': img_path,
                'label': row[title_col],
                'filename': img_name
            })
            valid_count += 1
        else:
            missing_count += 1
    
    print(f"   Found {valid_count} valid images")
    print(f"   Missing {missing_count} images")
    
    # Create DataFrame from valid images
    data_df = pd.DataFrame(images_data)
    
    # Count images per class
    class_counts = data_df['label'].value_counts()
    print(f"\n   Total unique dishes: {len(class_counts)}")
    print(f"   Images per dish:")
    print(f"     Min: {class_counts.min()}")
    print(f"     Max: {class_counts.max()}")
    print(f"     Mean: {class_counts.mean():.1f}")
    print(f"     Median: {class_counts.median():.1f}")
    
    # Filter classes with minimum images
    valid_classes = class_counts[class_counts >= MIN_IMAGES_PER_CLASS].index.tolist()
    data_df = data_df[data_df['label'].isin(valid_classes)]
    
    print(f"\n   After filtering (min {MIN_IMAGES_PER_CLASS} images per class):")
    print(f"     Classes: {len(valid_classes)}")
    print(f"     Total images: {len(data_df)}")
    
    if len(data_df) == 0:
        print("❌ No valid data after filtering!")
        return None, None, None
    
    return data_df, title_col, image_col

def load_image(img_path):
    """Load and preprocess image"""
    try:
        img = cv2.imread(img_path)
        if img is None:
            return None
        # Resize and normalize
        img = cv2.resize(img, IMAGE_SIZE)
        img = img.astype('float32') / 255.0
        return img
    except Exception as e:
        return None

def load_images_batch(data_df, sample_size=None):
    """Load images and labels"""
    print("\n🖼️  Loading images into memory...")
    
    if sample_size:
        data_df = data_df.sample(min(sample_size, len(data_df)), random_state=RANDOM_STATE)
        print(f"   Using sample of {len(data_df)} images")
    
    X = []
    y = []
    failed = 0
    
    for idx, row in data_df.iterrows():
        img = load_image(row['path'])
        if img is not None:
            X.append(img)
            y.append(row['label'])
        else:
            failed += 1
        
        if (idx + 1) % 1000 == 0:
            print(f"   Loaded {len(X)} images... ({failed} failed)")
    
    print(f"   Successfully loaded: {len(X)} images")
    print(f"   Failed to load: {failed} images")
    
    if len(X) == 0:
        print("❌ No images loaded!")
        return None, None
    
    X = np.array(X, dtype='float32')
    return X, np.array(y)

def encode_labels(y_train, y_test=None):
    """Encode labels to integers"""
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    
    if y_test is not None:
        y_test_encoded = le.transform(y_test)
        return y_train_encoded, y_test_encoded, le
    
    return y_train_encoded, le

def build_model(num_classes):
    """Build CNN model using transfer learning"""
    print("\n🏗️  Building model...")
    
    # Use MobileNetV2 as base (faster, lighter than ResNet)
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model weights
    base_model.trainable = False
    
    # Add custom layers
    model = keras.Sequential([
        keras.layers.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"   Model created with {num_classes} output classes")
    print(f"   Total parameters: {model.count_params():,}")
    
    return model

def train_model(model, X_train, y_train, X_val, y_val):
    """Train the model"""
    print("\n🚀 Training model...")
    
    # Convert to categorical
    y_train_cat = keras.utils.to_categorical(y_train)
    y_val_cat = keras.utils.to_categorical(y_val)
    
    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    # Callbacks
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        min_lr=1e-7
    )
    
    # Train
    history = model.fit(
        datagen.flow(X_train, y_train_cat, batch_size=BATCH_SIZE),
        epochs=EPOCHS,
        validation_data=(X_val, y_val_cat),
        callbacks=[early_stop, reduce_lr],
        verbose=1
    )
    
    return history

def evaluate_model(model, X_test, y_test):
    """Evaluate model on test set"""
    print("\n📊 Evaluating model on test set...")
    
    y_test_cat = keras.utils.to_categorical(y_test)
    loss, accuracy = model.evaluate(X_test, y_test_cat, verbose=0)
    
    print(f"   Test Loss: {loss:.4f}")
    print(f"   Test Accuracy: {accuracy*100:.2f}%")
    
    return accuracy

def save_model_and_artifacts(model, le, classes):
    """Save trained model and supporting artifacts"""
    print("\n💾 Saving model...")
    
    # Save model
    model.save(MODEL_PATH)
    print(f"   ✅ Model saved: {MODEL_PATH}")
    
    # Save label encoder
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(le, f)
    print(f"   ✅ Label encoder saved: {ENCODER_PATH}")
    
    # Save class names
    with open(CLASSES_PATH, 'wb') as f:
        pickle.dump(list(classes), f)
    print(f"   ✅ Classes saved: {CLASSES_PATH}")
    
    print(f"\n✨ Model artifacts ready for production use!")

def main():
    """Main training pipeline"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        🍽️  FOOD-IA: Model Training Pipeline                  ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    print(f"\n⚙️  Configuration:")
    print(f"   Image size: {IMAGE_SIZE}")
    print(f"   Batch size: {BATCH_SIZE}")
    print(f"   Epochs: {EPOCHS}")
    print(f"   Min images per class: {MIN_IMAGES_PER_CLASS}")
    
    # Step 1: Load and prepare data
    create_model_directory()
    data_df, title_col, image_col = load_and_prepare_data()
    
    if data_df is None or len(data_df) == 0:
        print("\n❌ Training failed: No valid data")
        return
    
    # Step 2: Load images (use sample for faster training on first run)
    # Set to None to use all images (slower but more accurate)
    SAMPLE_SIZE = 5000  # Use 5000 images for faster initial training
    X, y = load_images_batch(data_df, sample_size=SAMPLE_SIZE)
    
    if X is None or len(X) == 0:
        print("\n❌ Training failed: Could not load images")
        return
    
    # Step 3: Encode labels
    print(f"\n🏷️  Encoding labels...")
    unique_classes = np.unique(y)
    num_classes = len(unique_classes)
    print(f"   Classes: {num_classes}")
    print(f"   Sample classes: {unique_classes[:5]}")
    
    # Step 4: Split data
    print(f"\n✂️  Splitting data...")
    # First split: training+validation vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=TEST_SPLIT, random_state=RANDOM_STATE, stratify=y
    )
    
    # Second split: training vs validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=VALIDATION_SPLIT, random_state=RANDOM_STATE, stratify=y_temp
    )
    
    print(f"   Training set: {len(X_train)} images")
    print(f"   Validation set: {len(X_val)} images")
    print(f"   Test set: {len(X_test)} images")
    
    # Encode labels
    y_train_enc, y_test_enc, le = encode_labels(y_train, y_test)
    y_val_enc = le.transform(y_val)
    
    # Step 5: Build model
    model = build_model(num_classes)
    
    # Step 6: Train model
    try:
        history = train_model(model, X_train, y_train_enc, X_val, y_val_enc)
        
        # Step 7: Evaluate
        accuracy = evaluate_model(model, X_test, y_test_enc)
        
        # Step 8: Save artifacts
        save_model_and_artifacts(model, le, unique_classes)
        
        print(f"\n╔════════════════════════════════════════════════════════════════╗")
        print(f"║                   ✨ TRAINING COMPLETE ✨                     ║")
        print(f"║  Model saved with {accuracy*100:.2f}% accuracy on test set      ║")
        print(f"║  Ready to use in Streamlit app!                             ║")
        print(f"╚════════════════════════════════════════════════════════════════╝")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
