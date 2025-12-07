#!/usr/bin/env python
"""
Quick launcher to train the Food-IA model
Usage: python train_and_launch.py
"""

import subprocess
import sys
import os
import time

def check_model_exists():
    """Check if trained model already exists"""
    model_path = 'models/food_model_trained.h5'
    return os.path.exists(model_path)

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        🍽️  FOOD-IA: Train Model and Launch App               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    # Check if model exists
    if check_model_exists():
        print("\n✅ Trained model found!")
        print("\nStarting Streamlit app...")
        time.sleep(1)
    else:
        print("\n⚠️  No trained model found!")
        print("\nStarting model training...")
        print("(This will take 10-30 minutes depending on your system)\n")
        
        # Run training
        try:
            subprocess.run(
                [sys.executable, 'train_model.py'],
                check=True
            )
            print("\n✅ Training complete!")
        except subprocess.CalledProcessError:
            print("\n❌ Training failed!")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n⚠️  Training cancelled by user")
            sys.exit(1)
    
    # Launch Streamlit
    print("\n" + "="*64)
    print("🚀 Starting Streamlit app...")
    print("="*64 + "\n")
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'streamlit', 'run', 'app.py'],
            check=True
        )
    except KeyboardInterrupt:
        print("\n✅ App stopped")

if __name__ == "__main__":
    main()
