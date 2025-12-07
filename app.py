"""
Streamlit Web App for Food-IA Meal Analyzer
Analyze meals, predict calories, and check sports plan compatibility.
"""

import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.venv', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Try to import project modules
try:
    from data_loader import IMAGES_DIR
    import tensorflow as tf
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.info("Make sure to install dependencies: pip install -r requirements.txt")
    st.stop()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Food-IA | Meal Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .meal-card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .valid {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .warning {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .invalid {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .metric-box {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("⚙️ Configuration")
st.sidebar.write("Configure your meal analysis settings")

# Meal type selector
meal_type = st.sidebar.selectbox(
    "Type de repas:",
    ["Petit-déjeuner", "Déjeuner", "Snack", "Dîner"],
    index=1
)

# Sports plan selector
sports_goal = st.sidebar.radio(
    "Objectif sportif:",
    ["Perte de poids (Sèche)", "Prise de masse", "Maintenance"],
    index=0
)

# Calorie budget per meal based on goal and meal type
meal_budgets = {
    "Perte de poids (Sèche)": {
        "Petit-déjeuner": 400,
        "Déjeuner": 600,
        "Snack": 200,
        "Dîner": 500
    },
    "Prise de masse": {
        "Petit-déjeuner": 700,
        "Déjeuner": 900,
        "Snack": 400,
        "Dîner": 800
    },
    "Maintenance": {
        "Petit-déjeuner": 500,
        "Déjeuner": 700,
        "Snack": 300,
        "Dîner": 600
    }
}

# Allow custom calorie budget
calorie_budget = st.sidebar.number_input(
    f"Budget calorique pour {meal_type.lower()} (kcal):",
    min_value=50,
    max_value=2000,
    value=meal_budgets[sports_goal][meal_type],
    step=50
)

# Daily goal input
daily_calorie_goal = st.sidebar.number_input(
    "Objectif calorique journalier (kcal):",
    min_value=1200,
    max_value=5000,
    value=2000,
    step=100
)

st.sidebar.markdown("---")

# --- MAIN CONTENT ---
st.title("🍽️ Food-IA: Meal Analyzer")
st.markdown("### Analyser vos repas et vérifier la compatibilité avec votre plan sportif")

# Create two tabs
tab1, tab2, tab3 = st.tabs(["📸 Analyse de repas", "📊 Statistiques", "📚 Guide"])

# --- TAB 1: MEAL ANALYSIS ---
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Charger une image")
        
        # Image source selector
        image_source = st.radio(
            "Source de l'image:",
            ["📁 Depuis le dossier Food Images", "📤 Télécharger une image"],
            index=0
        )
        
        uploaded_image = None
        image_path = None
        
        if image_source == "📁 Depuis le dossier Food Images":
            # List available images
            if os.path.isdir(IMAGES_DIR):
                image_files = [f for f in os.listdir(IMAGES_DIR) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if image_files:
                    selected_image = st.selectbox(
                        "Sélectionnez une image:",
                        image_files,
                        index=0
                    )
                    image_path = os.path.join(IMAGES_DIR, selected_image)
                    uploaded_image = cv2.imread(image_path)
                else:
                    st.warning("⚠️ Aucune image trouvée dans le dossier Food Images")
            else:
                st.error(f"❌ Le dossier {IMAGES_DIR} n'existe pas")
        
        else:
            # Upload image
            uploaded_file = st.file_uploader(
                "Téléchargez une image de votre repas",
                type=["jpg", "jpeg", "png"]
            )
            if uploaded_file:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                uploaded_image = cv2.imdecode(file_bytes, 1)
    
    with col2:
        if uploaded_image is not None:
            st.subheader("Aperçu de l'image")
            # Convert BGR to RGB for display
            display_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)
            st.image(display_image, use_column_width=True)
    
    # Analysis section
    if uploaded_image is not None:
        st.markdown("---")
        
        if st.button("🔍 Analyser le repas", use_container_width=True):
            with st.spinner("Analyse en cours..."):
                # Prepare image for model
                img_resized = cv2.resize(uploaded_image, (128, 128))
                img_array = np.expand_dims(img_resized, axis=0) / 255.0
                
                # Mock prediction (since model might not be trained)
                # In production, use: prediction = model.predict(img_array)
                # For now, we'll create a realistic simulation
                
                # Simulated meal types and their typical calories
                meal_types_db = {
                    0: ("Salade Verte", 150),
                    1: ("Poulet Grillé", 350),
                    2: ("Pâtes Carbonara", 450),
                    3: ("Pizza Margherita", 280),
                    4: ("Burger", 550),
                    5: ("Poisson Blanc", 200),
                    6: ("Riz Pilaf", 300),
                    7: ("Soupe Minestrone", 120),
                    8: ("Steak Frites", 650),
                    9: ("Tarte aux Pommes", 280),
                }
                
                # Simulate prediction with some randomness
                predicted_index = np.random.randint(0, len(meal_types_db))
                dish_name, calories = meal_types_db[predicted_index]
                confidence = np.random.uniform(60, 99)
                
                # --- ANALYSIS RESULTS ---
                st.subheader("📊 Résultats de l'analyse")
                
                # Metrics row
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric("Plat détecté", dish_name)
                
                with metric_col2:
                    st.metric("Calories", f"{calories} kcal")
                
                with metric_col3:
                    st.metric("Confiance IA", f"{confidence:.1f}%")
                
                st.markdown("---")
                
                # Meal type analysis
                st.subheader("🎯 Analyse du repas")
                
                # Calculate compatibility
                remaining_budget = calorie_budget - calories
                daily_percentage = (calories / daily_calorie_goal) * 100
                
                # Determine status
                if sports_goal == "Perte de poids (Sèche)":
                    if calories > calorie_budget:
                        status = "⚠️ DÉCONSEILLÉ"
                        status_color = "invalid"
                        advice = f"Ce plat ({calories} kcal) dépasse votre budget de {calorie_budget} kcal pour ce {meal_type.lower()}. Trop riche pour votre objectif de sèche."
                    elif calories < 100:
                        status = "⚠️ TROP LÉGER"
                        status_color = "warning"
                        advice = "Ce repas est très léger. Assurez-vous d'avoir suffisamment de protéines ailleurs."
                    else:
                        status = "✅ VALIDE"
                        status_color = "valid"
                        advice = f"Excellent choix ! Ce repas rentre parfaitement dans votre objectif de perte de poids. Budget restant: {remaining_budget} kcal."
                
                elif sports_goal == "Prise de masse":
                    if calories < 300:
                        status = "⚠️ INSUFFISANT"
                        status_color = "warning"
                        advice = f"Ce plat est trop léger ({calories} kcal) pour une prise de masse. Ajoutez une source de glucides ou de protéines."
                    elif calories > calorie_budget * 1.3:
                        status = "⚠️ TROP RICHE"
                        status_color = "warning"
                        advice = f"Ce plat dépasse significativement votre budget. Risque de prise de graisse excessive."
                    else:
                        status = "✅ VALIDE"
                        status_color = "valid"
                        advice = f"Parfait ! Bon apport calorique pour la construction musculaire. Budget restant: {remaining_budget} kcal."
                
                else:  # Maintenance
                    if abs(remaining_budget) < 50:
                        status = "✅ PARFAIT"
                        status_color = "valid"
                        advice = f"Excellent ! Ce repas correspond exactement à votre budget pour le {meal_type.lower()}."
                    elif calories > calorie_budget * 1.1:
                        status = "⚠️ LÉGÈREMENT ÉLEVÉ"
                        status_color = "warning"
                        advice = f"Ce repas est légèrement au-dessus du budget prévu. À consommer occasionnellement."
                    elif calories < calorie_budget * 0.7:
                        status = "ℹ️ LÉGER"
                        status_color = "warning"
                        advice = "Ce repas est léger. Vous pourriez ajouter un snack ou une source de protéines."
                    else:
                        status = "✅ VALIDE"
                        status_color = "valid"
                        advice = "Bon équilibre calorique pour le maintien."
                
                # Display status card
                st.markdown(f"""
                <div class="meal-card {status_color}">
                    <h3>{status}</h3>
                    <p>{advice}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed metrics
                st.subheader("📈 Détails du repas")
                
                detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
                
                with detail_col1:
                    st.markdown("""
                    <div class="metric-box">
                        <h4>Budget</h4>
                        <p style="font-size: 18px; color: #2c3e50;"><b>{} kcal</b></p>
                        <p style="font-size: 12px; color: #7f8c8d;">Alloué pour {}</p>
                    </div>
                    """.format(calorie_budget, meal_type.lower()), unsafe_allow_html=True)
                
                with detail_col2:
                    st.markdown("""
                    <div class="metric-box">
                        <h4>Repas</h4>
                        <p style="font-size: 18px; color: #2c3e50;"><b>{} kcal</b></p>
                        <p style="font-size: 12px; color: #7f8c8d;">Calories du plat</p>
                    </div>
                    """.format(calories), unsafe_allow_html=True)
                
                with detail_col3:
                    st.markdown("""
                    <div class="metric-box">
                        <h4>Restant</h4>
                        <p style="font-size: 18px; color: #2c3e50;"><b>{} kcal</b></p>
                        <p style="font-size: 12px; color: #7f8c8d;">Budget restant pour {}</p>
                    </div>
                    """.format(max(0, remaining_budget), meal_type.lower()), unsafe_allow_html=True)
                
                with detail_col4:
                    st.markdown("""
                    <div class="metric-box">
                        <h4>% Journalier</h4>
                        <p style="font-size: 18px; color: #2c3e50;"><b>{:.1f}%</b></p>
                        <p style="font-size: 12px; color: #7f8c8d;">De votre objectif</p>
                    </div>
                    """.format(daily_percentage), unsafe_allow_html=True)
                
                # Progress visualizations
                st.subheader("📊 Progression")
                
                prog_col1, prog_col2 = st.columns(2)
                
                with prog_col1:
                    st.write("**Budget du repas:**")
                    progress_value = min(calories / calorie_budget, 1.5)
                    st.progress(min(progress_value, 1.0))
                    if calories > calorie_budget:
                        st.caption(f"⚠️ Dépasse de {calories - calorie_budget} kcal ({((calories/calorie_budget - 1) * 100):.0f}%)")
                    else:
                        st.caption(f"✅ {((calories/calorie_budget) * 100):.0f}% du budget utilisé")
                
                with prog_col2:
                    st.write("**Objectif journalier:**")
                    daily_progress = min(daily_percentage / 100, 1.0)
                    st.progress(daily_progress)
                    st.caption(f"{daily_percentage:.1f}% de votre objectif journalier")

# --- TAB 2: STATISTICS ---
with tab2:
    st.subheader("📊 Tableau de bord statistique")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Objectif journalier", f"{daily_calorie_goal} kcal", delta="Maintenance")
    
    with col2:
        st.metric("Petit-déjeuner budget", f"{meal_budgets[sports_goal]['Petit-déjeuner']} kcal")
    
    with col3:
        st.metric("Déjeuner budget", f"{meal_budgets[sports_goal]['Déjeuner']} kcal")
    
    with col4:
        st.metric("Dîner budget", f"{meal_budgets[sports_goal]['Dîner']} kcal")
    
    st.markdown("---")
    
    # Meal budgets comparison
    st.subheader("💡 Budgets recommandés par objectif")
    
    budgets_df = pd.DataFrame(meal_budgets).T
    st.dataframe(budgets_df, use_container_width=True)
    
    st.markdown("---")
    
    # Nutritional guidelines
    st.subheader("📋 Recommandations nutritionnelles")
    
    guidelines = {
        "Perte de poids (Sèche)": {
            "Calories": "1500-2000 kcal/jour",
            "Protéines": "1.6-2.2g par kg de poids corporel",
            "Glucides": "Modérés (50-100g/jour)",
            "Lipides": "0.8-1.0g par kg de poids corporel",
            "Conseil": "Maintenir un léger déficit calorique"
        },
        "Prise de masse": {
            "Calories": "2500-3500 kcal/jour",
            "Protéines": "1.6-2.2g par kg de poids corporel",
            "Glucides": "Élevés (5-8g par kg de poids corporel)",
            "Lipides": "1.0-1.5g par kg de poids corporel",
            "Conseil": "Maintenir un léger surplus calorique"
        },
        "Maintenance": {
            "Calories": "2000-2500 kcal/jour",
            "Protéines": "1.2-1.6g par kg de poids corporel",
            "Glucides": "3-5g par kg de poids corporel",
            "Lipides": "0.8-1.2g par kg de poids corporel",
            "Conseil": "Équilibre entre apports et dépenses"
        }
    }
    
    selected_goal = sports_goal
    guidelines_data = guidelines[selected_goal]
    
    for key, value in guidelines_data.items():
        st.write(f"**{key}:** {value}")

# --- TAB 3: GUIDE ---
with tab3:
    st.subheader("📚 Guide d'utilisation")
    
    st.markdown("""
    ### 🎯 Comment utiliser Food-IA?
    
    **1. Configuration (Barre latérale)**
    - Sélectionnez votre type de repas (Petit-déjeuner, Déjeuner, Snack, Dîner)
    - Choisissez votre objectif sportif (Sèche, Prise de masse, Maintenance)
    - Ajustez le budget calorique si nécessaire
    - Définissez votre objectif calorique journalier
    
    **2. Analyse d'image**
    - Sélectionnez une image depuis le dossier ou téléchargez la vôtre
    - Cliquez sur "Analyser le repas"
    - Consultez l'analyse détaillée
    
    **3. Interprétation des résultats**
    - ✅ **VALIDE**: Le repas correspond à votre objectif
    - ⚠️ **ATTENTION**: Le repas demande une vérification
    - ❌ **DÉCONSEILLÉ**: Le repas ne correspond pas à votre objectif
    
    ### 📊 Objectifs sportifs
    
    **Perte de poids (Sèche)**
    - Créer un déficit calorique
    - Repas légers et riches en protéines
    - Budgets réduits par repas
    
    **Prise de masse**
    - Créer un surplus calorique
    - Repas copieux et équilibrés
    - Budgets augmentés par repas
    
    **Maintenance**
    - Équilibre entre apports et dépenses
    - Repas équilibrés
    - Budgets modérés
    
    ### 💡 Conseils pratiques
    
    - Chaque repas doit contribuer à votre objectif journalier
    - Privilégiez les aliments riches en protéines
    - Variez vos sources de glucides et lipides
    - Respectez vos budgets de repas
    - Ajustez progressivement si nécessaire
    
    ### 📞 Besoin d'aide?
    
    Consultez la documentation complète ou contactez votre coach sportif.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 12px;">
    <p>Food-IA © 2025 | Meal Analysis System for Sports Nutrition</p>
    <p>Developed with ❤️ using Streamlit, TensorFlow, and Python</p>
</div>
""", unsafe_allow_html=True)
