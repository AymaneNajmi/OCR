#!/usr/bin/env python
"""
🍽️ Food-IA Quick Start Guide
This script provides an interactive overview of the project.
"""

def print_header():
    print("\n" + "=" * 70)
    print("🍽️  FOOD-IA: MEAL ANALYSIS SYSTEM FOR SPORTS NUTRITION")
    print("=" * 70 + "\n")

def print_quick_start():
    print("⚡ QUICK START\n")
    print("1. Install dependencies:")
    print("   .venv\\Scripts\\python.exe -m pip install -r requirements.txt\n")
    print("2. Launch the Streamlit app:")
    print("   .venv\\Scripts\\python.exe run_app.py\n")
    print("   OR:")
    print("   .venv\\Scripts\\python.exe -m streamlit run app.py\n")
    print("3. App opens at: http://localhost:8501\n")

def print_features():
    print("\n✨ KEY FEATURES\n")
    features = [
        ("📸 Image Analysis", "Upload or select meals from Food Images folder"),
        ("🤖 AI Recognition", "CNN-based meal identification with confidence scoring"),
        ("🎯 Sports Planning", "3 goals: Weight Loss, Muscle Gain, Maintenance"),
        ("🍴 Meal Types", "Breakfast, Lunch, Snack, Dinner with custom budgets"),
        ("📊 Dashboard", "Real-time tracking, progress visualization, analytics"),
        ("💡 Coaching", "Personalized advice based on your sports goals"),
        ("📱 Web Interface", "Interactive Streamlit app with responsive design"),
    ]
    
    for title, desc in features:
        print(f"  {title}")
        print(f"    → {desc}\n")

def print_sports_goals():
    print("\n🎯 SPORTS GOALS\n")
    
    goals = {
        "Perte de poids (Weight Loss)": {
            "Daily": "1500-2000 kcal",
            "Breakfast": "400 kcal",
            "Lunch": "600 kcal",
            "Snack": "200 kcal",
            "Dinner": "500 kcal",
            "Focus": "Calorie deficit, high protein, light meals"
        },
        "Prise de masse (Muscle Gain)": {
            "Daily": "2500-3500 kcal",
            "Breakfast": "700 kcal",
            "Lunch": "900 kcal",
            "Snack": "400 kcal",
            "Dinner": "800 kcal",
            "Focus": "Calorie surplus, balanced macros, substantial meals"
        },
        "Maintenance": {
            "Daily": "2000-2500 kcal",
            "Breakfast": "500 kcal",
            "Lunch": "700 kcal",
            "Snack": "300 kcal",
            "Dinner": "600 kcal",
            "Focus": "Balanced intake matching expenditure"
        }
    }
    
    for goal, details in goals.items():
        print(f"  📌 {goal}")
        print(f"     Daily: {details['Daily']}")
        print(f"     Breakfast: {details['Breakfast']} | Lunch: {details['Lunch']}")
        print(f"     Snack: {details['Snack']} | Dinner: {details['Dinner']}")
        print(f"     Focus: {details['Focus']}\n")

def print_project_structure():
    print("\n📁 PROJECT STRUCTURE\n")
    print("""
    OCR/
    ├── 📱 app.py                  ← Main Streamlit app
    ├── 🚀 run_app.py              ← App launcher
    ├── 📋 requirements.txt         ← Dependencies
    ├── 📖 README.md               ← Main documentation
    ├── 📖 STREAMLIT_GUIDE.md      ← Detailed Streamlit docs
    ├── 🔧 QUICK_START.py          ← This file
    ├── .venv/                     ← Virtual environment
    │   └── src/                   ← ML source code
    │       ├── main.py            ← Training entry point
    │       ├── data_loader.py     ← Dataset loading
    │       ├── food_model.py      ← CNN architecture
    │       ├── diet_advisor.py    ← Coaching logic
    │       └── ...
    └── data/
        └── Food Images/           ← Meal image database
    """)

def print_file_guide():
    print("\n📚 KEY FILES EXPLAINED\n")
    
    files = {
        "app.py": "Main Streamlit web application with UI, analysis logic, and dashboard",
        "run_app.py": "Simple launcher script to start the app without terminal commands",
        "STREAMLIT_GUIDE.md": "Complete Streamlit documentation with usage examples",
        "README.md": "Full project documentation with setup and feature details",
        "requirements.txt": "All Python dependencies for the project",
        "src/data_loader.py": "Handles CSV/image loading with auto-detection",
        "src/food_model.py": "CNN model architecture (128x128 input)",
        "src/diet_advisor.py": "Coaching logic for meal analysis",
    }
    
    for filename, description in files.items():
        print(f"  📄 {filename}")
        print(f"     {description}\n")

def print_troubleshooting():
    print("\n🐛 TROUBLESHOOTING\n")
    
    issues = {
        "Port already in use": "streamlit run app.py --server.port 8502",
        "Streamlit not found": ".venv\\Scripts\\python.exe -m pip install streamlit",
        "TensorFlow import error": ".venv\\Scripts\\python.exe -m pip install --upgrade tensorflow tf-keras",
        "Images not loading": "Check data/Food Images/ folder exists and has jpg/jpeg/png files",
        "PowerShell policy issue": "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass",
    }
    
    for issue, solution in issues.items():
        print(f"  ❌ {issue}")
        print(f"     → {solution}\n")

def print_next_steps():
    print("\n➡️  NEXT STEPS\n")
    
    steps = [
        "1. Install dependencies: pip install -r requirements.txt",
        "2. Launch the app: python run_app.py",
        "3. Configure your profile (goal, meal type, calories)",
        "4. Upload or select a meal image",
        "5. Click 'Analyze the meal' to get results",
        "6. Review recommendations and budget consumption",
        "7. Track your daily progress in the Dashboard",
    ]
    
    for step in steps:
        print(f"  {step}")

def print_footer():
    print("\n" + "=" * 70)
    print("For more details, see README.md or STREAMLIT_GUIDE.md")
    print("Food-IA © 2025 | Developed with ❤️ for better sports nutrition")
    print("=" * 70 + "\n")

def main():
    print_header()
    print_quick_start()
    print_features()
    print_sports_goals()
    print_project_structure()
    print_file_guide()
    print_troubleshooting()
    print_next_steps()
    print_footer()

if __name__ == "__main__":
    main()
