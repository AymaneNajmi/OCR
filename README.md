# 🍽️ Food-IA: Meal Analysis System for Sports Nutrition

A comprehensive AI-powered meal analysis system that uses deep learning to recognize food items, estimate nutritional content, and provide personalized coaching for sports nutrition planning.

## 🎯 Project Overview

Food-IA combines computer vision, machine learning, and sports nutrition expertise to help athletes and fitness enthusiasts make better meal choices aligned with their training goals.

### Key Features
- **AI-Powered Meal Recognition**: CNN-based image classification
- **Calorie Estimation**: Automatic nutritional analysis
- **Interactive Streamlit Dashboard**: Real-time meal analysis and tracking
- **Personalized Coaching**: Advice tailored to sports goals (weight loss, muscle gain, maintenance)
- **Budget Tracking**: Daily and per-meal calorie budgets
- **Multi-Language Support**: French interface with extensible design

## 📦 Quick Start

### Installation

1. **Install dependencies:**
```powershell
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. **Launch the Streamlit app:**
```powershell
.venv\Scripts\python.exe run_app.py
```

Or directly:
```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

### Alternative: PowerShell Activation (no execution policy change)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Or use Command Prompt batch activation:
```cmd
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
OCR/
├── app.py                      # Main Streamlit web application
├── run_app.py                  # App launcher script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── STREAMLIT_GUIDE.md          # Detailed Streamlit documentation
├── .gitignore                  # Git exclusions
├── .venv/                      # Python virtual environment
│   ├── Scripts/                # Executable scripts
│   └── Lib/                    # Installed packages
└── src/                        # Source code (inside .venv)
    ├── main.py                 # Training entry point
    ├── data_loader.py          # Dataset loading & preprocessing
    ├── food_model.py           # CNN architecture
    ├── diet_advisor.py         # Nutrition coaching logic
    ├── ocr_engine.py           # OCR utilities
    ├── preprocessor.py         # Image preprocessing
    └── train.py                # Training utilities
```

## 🚀 Features

### Streamlit Web Dashboard
- **📸 Image Upload & Selection**: Choose meals from your Food Images folder or upload custom images
- **🔍 Real-time Analysis**: Instant meal recognition and calorie estimation
- **🎯 Personalized Goals**: Three sports modes with automatic budget calculations
- **📊 Progress Tracking**: Visual budgets and daily goal monitoring
- **💡 Coaching Advice**: AI-powered recommendations based on your goals
- **📋 Nutritional Guidelines**: Evidence-based macro recommendations

### Machine Learning
- **CNN Architecture**: 3-layer convolutional neural network
- **Image Recognition**: 128x128 optimized input size
- **Transfer Learning Ready**: Extensible model design
- **Real-time Prediction**: Fast inference with confidence scoring

## 📊 Usage Guide

### 1. Launch the App
```powershell
.venv\Scripts\python.exe run_app.py
```

### 2. Configure Your Profile
- Select meal type (Breakfast/Lunch/Snack/Dinner)
- Choose sports goal (Weight Loss/Muscle Gain/Maintenance)
- Set daily calorie target

### 3. Analyze a Meal
- Upload an image or select from Food Images folder
- Click "Analyze the meal"
- Review recommendations

### 4. Track Progress
- Monitor budget consumption
- Check daily goal percentage
- Adjust meals as needed

### 5. View Statistics
- Compare budgets across goals
- Review nutritional guidelines
- Plan your nutrition strategy

## 🎓 Supported Sports Goals

### Perte de poids (Weight Loss/Cutting)
- **Daily Target**: 1500-2000 kcal
- **Focus**: Calorie deficit, high protein
- **Meal Budgets**: 
  - Breakfast: 400 kcal
  - Lunch: 600 kcal
  - Snack: 200 kcal
  - Dinner: 500 kcal

### Prise de masse (Muscle Gain/Bulking)
- **Daily Target**: 2500-3500 kcal
- **Focus**: Calorie surplus, balanced macros
- **Meal Budgets**:
  - Breakfast: 700 kcal
  - Lunch: 900 kcal
  - Snack: 400 kcal
  - Dinner: 800 kcal

### Maintenance
- **Daily Target**: 2000-2500 kcal
- **Focus**: Balanced intake matching expenditure
- **Meal Budgets**:
  - Breakfast: 500 kcal
  - Lunch: 700 kcal
  - Snack: 300 kcal
  - Dinner: 600 kcal

## 🔧 Configuration

### Modify Calorie Budgets
Edit the `meal_budgets` dictionary in `app.py` to customize default values.

### Add Custom Meals
Update the `meal_types_db` dictionary with your own meal-calorie pairs.

### Connect Real Model
Replace the simulated prediction with your trained model:
```python
model = tf.keras.models.load_model('models/food_model.h5')
prediction = model.predict(img_array)
```

## 📚 Detailed Documentation

- **[Streamlit Guide](STREAMLIT_GUIDE.md)**: Complete app documentation
- **[Training Guide](src/main.py)**: Model training instructions
- **[Data Loading](src/data_loader.py)**: Dataset preparation

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Streamlit uses port 8501 by default. To use a different port:
streamlit run app.py --server.port 8502
```

### Images Not Loading
- Verify `data/Food Images/` exists with `.jpg/.jpeg/.png` files
- Check file permissions
- Ensure images are readable by OpenCV

### Model Import Errors
```powershell
# Reinstall TensorFlow
.venv\Scripts\python.exe -m pip install --upgrade tensorflow tf-keras
```

### PowerShell Execution Policy
To permanently allow scripts (use with caution):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

Or bypass temporarily for current session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 📦 Dependencies

Core packages (see `requirements.txt` for complete list):
- **streamlit**: Web framework
- **tensorflow/tf-keras**: Deep learning
- **opencv-python**: Image processing
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: ML utilities

## 🤝 Contributing

To add features:
1. Create a branch
2. Make changes
3. Test locally: `streamlit run app.py`
4. Commit and push to GitHub

## 📝 License

Food-IA Project © 2025. All rights reserved.

## 📞 Support

1. Check the **Guide** tab in the Streamlit app
2. Review this README and STREAMLIT_GUIDE.md
3. Consult the source code comments
4. Contact the development team

## 🔄 Updates

To sync with latest changes:
```powershell
git pull origin main
```

To push your local changes:
```powershell
git add .
git commit -m "Your message"
git push origin main
```

---

**Food-IA © 2025** | Developed with ❤️ for better sports nutrition
