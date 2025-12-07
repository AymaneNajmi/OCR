# 🍽️ Food-IA Streamlit Web App

A modern, interactive web application for meal analysis and sports nutrition planning using Streamlit, TensorFlow, and Python.

## Features

### 📸 Meal Analysis
- **Image Recognition**: Upload or select meals from the Food Images folder
- **Calorie Detection**: AI-powered calorie estimation from meal images
- **Confidence Scoring**: View prediction confidence percentages
- **Real-time Analysis**: Instant feedback on meal compatibility

### 🎯 Sports Plan Integration
Three sports goals with customizable budgets:
- **Perte de poids (Sèche)**: Calorie deficit, light meals, high protein
- **Prise de masse (Bulk)**: Calorie surplus, substantial meals, balanced macros
- **Maintenance**: Balanced intake matching daily expenditure

### 🍴 Meal Type Support
- **Petit-déjeuner** (Breakfast)
- **Déjeuner** (Lunch)
- **Snack** (Snack/Light meal)
- **Dîner** (Dinner)

### 📊 Dashboard & Analytics
- **Budget Tracking**: Real-time budget consumption visualization
- **Daily Goal Progress**: See your percentage toward daily calorie target
- **Nutritional Guidelines**: Evidence-based recommendations by goal
- **Budget Comparison**: View all meal budgets across different sports goals

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Steps

1. **Install dependencies:**
```powershell
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. **Verify Streamlit installation:**
```powershell
.venv\Scripts\python.exe -m streamlit --version
```

## Running the App

### Method 1: Using the provided launcher script
```powershell
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\python.exe run_app.py
```

### Method 2: Direct Streamlit command
```powershell
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\python.exe -m streamlit run app.py
```

### Method 3: PowerShell activation bypass (no execution policy change)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## Project Structure

```
OCR/
├── app.py                      # Main Streamlit web application
├── run_app.py                  # App launcher script
├── requirements.txt            # Python dependencies
├── README.md                   # Main project documentation
├── .venv/
│   └── src/
│       ├── main.py            # Training script
│       ├── data_loader.py      # Dataset loading utilities
│       ├── food_model.py       # CNN model architecture
│       ├── diet_advisor.py     # Meal analysis logic
│       └── ...
└── data/
    └── Food Images/           # Meal image database
```

## Usage Guide

### 1. Configuration
In the left sidebar, set up your profile:
- Select your meal type
- Choose your sports goal
- Adjust calorie budgets if needed
- Set daily calorie target

### 2. Image Selection
Choose one of two options:
- **📁 From folder**: Select from available images in the Food Images directory
- **📤 Upload**: Upload your own meal image

### 3. Analysis
Click "🔍 Analyser le repas" to:
- Get dish recognition
- See calorie estimation
- Get AI confidence score
- Receive personalized advice

### 4. Interpretation
- ✅ **VALIDE**: Meal fits your goal
- ⚠️ **ATTENTION**: Review recommended, may need adjustment
- ❌ **DÉCONSEILLÉ**: Doesn't fit your current goal

### 5. Tracking
Monitor your daily progress:
- Budget consumption per meal
- Daily goal percentage
- Remaining calorie budget

## Recommended Calorie Budgets

### Perte de poids (Sèche) - Daily: 1500-2000 kcal
- Petit-déjeuner: 400 kcal
- Déjeuner: 600 kcal
- Snack: 200 kcal
- Dîner: 500 kcal

### Prise de masse - Daily: 2500-3500 kcal
- Petit-déjeuner: 700 kcal
- Déjeuner: 900 kcal
- Snack: 400 kcal
- Dîner: 800 kcal

### Maintenance - Daily: 2000-2500 kcal
- Petit-déjeuner: 500 kcal
- Déjeuner: 700 kcal
- Snack: 300 kcal
- Dîner: 600 kcal

## Customization

### Add Your Own Meals to Database
1. Place meal images in `data/Food Images/`
2. Update the meal_types_db dictionary in `app.py` with:
   ```python
   meal_types_db = {
       0: ("Salade Verte", 150),
       1: ("Poulet Grillé", 350),
       # Add your custom meals here
   }
   ```

### Modify Calorie Budgets
Edit `meal_budgets` dictionary in the sidebar section to adjust default values for your specific needs.

### Connect Real Model
Replace the simulated prediction section in `app.py` with:
```python
model = tf.keras.models.load_model('models/food_model.h5')
prediction = model.predict(img_array)
predicted_index = np.argmax(prediction)
confidence = np.max(prediction) * 100
```

## Troubleshooting

### App won't start
```powershell
# Clear Streamlit cache
Remove-Item -Path $env:USERPROFILE\.streamlit\cache -Recurse -Force -ErrorAction SilentlyContinue

# Reinstall dependencies
.venv\Scripts\python.exe -m pip install --upgrade streamlit
```

### Images not loading
- Verify `data/Food Images` folder exists
- Check that image files are `.jpg`, `.jpeg`, or `.png`
- Ensure proper file permissions

### Model not loading
- Verify `models/food_model.h5` exists
- Check TensorFlow installation: `.venv\Scripts\python.exe -m pip install --upgrade tensorflow tf-keras`

## Contributing

To add new features:
1. Create a new branch
2. Modify `app.py` or supporting modules
3. Test locally with `streamlit run app.py`
4. Commit and push changes

## Dependencies

Core dependencies:
- **streamlit**: Web app framework
- **tensorflow/tf-keras**: Deep learning
- **opencv-python**: Image processing
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning utilities
- **matplotlib/seaborn**: Visualization

See `requirements.txt` for complete list.

## License

This project is part of the Food-IA system. All rights reserved.

## Support

For issues or questions:
1. Check the **📚 Guide** tab in the app
2. Review this documentation
3. Contact your development team

---

**Food-IA © 2025** | Developed with ❤️ using Streamlit, TensorFlow, and Python
