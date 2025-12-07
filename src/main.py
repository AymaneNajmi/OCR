from src.data_loader import load_food_data
from src.food_model import create_food_cnn
from src.diet_advisor import SportDietAdvisor
import os

# 1. Chargement et Entraînement
print("--- Démarrage du système Food-IA ---")
X, y, label_map, inv_label_map, nutrition_db = load_food_data(limit=500)

# Séparation train/test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Création du modèle
num_classes = len(label_map)
model = create_food_cnn(num_classes)

print(f"Entraînement sur {len(X_train)} images pour reconnaître {num_classes} plats...")
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
model.save('models/food_model.h5')

# 2. Simulation d'un Client
print("\n--- Simulation Coach Sportif ---")
advisor = SportDietAdvisor('models/food_model.h5', nutrition_db, inv_label_map)

# Imaginons que l'utilisateur prend une photo d'un plat (utilisez une image de test réelle)
# Pour le test, on prend une image du dataset de test
import cv2
test_img_path = "test_plat.jpg" 
# Sauvegardons une image du test pour simuler la "photo"
cv2.imwrite(test_img_path, cv2.cvtColor(X_test[0] * 255, cv2.COLOR_RGB2BGR))

# Cas 1 : Client en sèche
resultat = advisor.analyze_meal(test_img_path, user_goal="perte_poids", calorie_budget=500)

print(f"\nPlat détecté : {resultat['plat']}")
print(f"Calories : {resultat['calories']} kcal")
print(f"Avis du Coach : {resultat['statut']}")
print(f"Détail : {resultat['conseil']}")