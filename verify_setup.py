#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify Food-IA installation and show model status
"""

import os
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Directory Structure:")
    dirs = [
        'models',
        '.venv/data/Food Images',
        'src'
    ]
    
    for d in dirs:
        exists = os.path.isdir(d)
        status = "✅" if exists else "❌"
        print(f"   {status} {d}")
    
    return all(os.path.isdir(d) for d in dirs)

def check_files():
    """Check if required files exist"""
    print("\n📄 File Structure:")
    files = [
        ('app.py', 'Streamlit application'),
        ('train_model.py', 'Model training script'),
        ('train_and_launch.py', 'Training + app launcher'),
        ('run_app.py', 'App launcher'),
        ('src/meal_predictor.py', 'Meal prediction module'),
        ('src/data_loader.py', 'Data loading module'),
        ('requirements.txt', 'Dependencies'),
    ]
    
    for f, desc in files:
        exists = os.path.isfile(f)
        status = "✅" if exists else "❌"
        print(f"   {status} {f:30} - {desc}")
    
    return all(os.path.isfile(f) for f, _ in files)

def check_model_artifacts():
    """Check if model is trained"""
    print("\n🤖 Model Status:")
    
    artifacts = [
        ('models/food_model_trained.h5', 'Trained CNN model'),
        ('models/label_encoder.pkl', 'Label encoder'),
        ('models/classes.pkl', 'Class list'),
    ]
    
    trained = True
    for path, desc in artifacts:
        exists = os.path.isfile(path)
        status = "✅" if exists else "⏳"
        trained = trained and exists
        state = "Ready" if exists else "Not trained yet"
        print(f"   {status} {path:35} - {state}")
    
    return trained

def count_images():
    """Count images in Food Images folder"""
    print("\n📸 Dataset:")
    img_dir = '.venv/data/Food Images'
    
    if os.path.isdir(img_dir):
        images = [f for f in os.listdir(img_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"   ✅ Images found: {len(images)}")
        return len(images) > 0
    else:
        print(f"   ❌ Food Images folder not found")
        return False

def check_python_env():
    """Check Python environment"""
    print("\n🐍 Python Environment:")
    print(f"   Python version: {sys.version.split()[0]}")
    print(f"   Executable: {sys.executable}")
    
    try:
        import cv2
        print(f"   ✅ OpenCV: {cv2.__version__}")
    except:
        print(f"   ❌ OpenCV not installed")
    
    try:
        import tensorflow as tf
        print(f"   ✅ TensorFlow: {tf.__version__}")
    except:
        print(f"   ❌ TensorFlow not installed")
    
    try:
        import streamlit
        print(f"   ✅ Streamlit: {streamlit.__version__}")
    except:
        print(f"   ❌ Streamlit not installed")
    
    try:
        import pandas
        print(f"   ✅ Pandas: {pandas.__version__}")
    except:
        print(f"   ❌ Pandas not installed")

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         🍽️  FOOD-IA: System Verification                      ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    dirs_ok = check_directories()
    files_ok = check_files()
    model_trained = check_model_artifacts()
    data_ok = count_images()
    check_python_env()
    
    print("\n" + "="*64)
    print("📊 SUMMARY:")
    print("="*64)
    
    if dirs_ok and files_ok and data_ok:
        print("✅ Project structure: OK")
    else:
        print("❌ Project structure: INCOMPLETE")
    
    if model_trained:
        print("✅ Model status: TRAINED & READY")
        print("\n🚀 You can run: .venv\\Scripts\\python.exe run_app.py")
    else:
        print("⏳ Model status: NOT TRAINED")
        print("\n🚀 First time? Train the model:")
        print("   .venv\\Scripts\\python.exe train_and_launch.py")
        print("\n   Or train separately:")
        print("   .venv\\Scripts\\python.exe train_model.py")
        print("   Then launch:")
        print("   .venv\\Scripts\\python.exe run_app.py")
    
    print("\n" + "="*64)
    print("📚 For help, see:")
    print("   - README.md (project overview)")
    print("   - TRAINING_GUIDE.md (model training)")
    print("   - STREAMLIT_GUIDE.md (app usage)")
    print("="*64 + "\n")

if __name__ == "__main__":
    main()
