import cv2
import numpy as np
import tensorflow as tf

class SportDietAdvisor:
    def __init__(self, model_path, nutrition_db, inv_label_map):
        self.model = tf.keras.models.load_model(model_path)
        self.nutrition_db = nutrition_db
        self.inv_label_map = inv_label_map
        self.classes = list(inv_label_map.values())

    def analyze_meal(self, image_path, user_goal="perte_poids", calorie_budget=600):
        """
        user_goal: 'perte_poids' ou 'prise_masse'
        calorie_budget: Combien de calories le client peut manger sur ce repas ?
        """
        
        # 1. Préparer l'image
        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, (128, 128))
        img_array = np.expand_dims(img_resized, axis=0) / 255.0
        
        # 2. Prédire le plat
        prediction = self.model.predict(img_array)
        predicted_index = np.argmax(prediction)
        dish_name = self.inv_label_map[predicted_index]
        confidence = np.max(prediction) * 100
        
        # 3. Récupérer les infos nutritionnelles
        # (On gère le cas où les calories seraient manquantes ou mal formatées)
        try:
            calories = float(self.nutrition_db.get(dish_name, 0))
        except:
            calories = 0 # Valeur par défaut si erreur

        # 4. Logique du Coach Sportif
        advice = ""
        status = "NEUTRE"

        if user_goal == "perte_poids":
            if calories > calorie_budget:
                status = "DECONSEILLE"
                advice = f"Attention ! Ce plat ({calories} kcal) dépasse votre budget de {calorie_budget} kcal. Trop riche pour votre sèche."
            elif calories < 200:
                status = "ATTENTION"
                advice = "C'est très léger. Assurez-vous d'avoir assez de protéines à côté."
            else:
                status = "VALIDE"
                advice = "Excellent choix pour votre perte de poids. Rentre dans les macros."
        
        elif user_goal == "prise_masse":
            if calories < 400:
                status = "INSUFFISANT"
                advice = f"Ce plat est trop léger ({calories} kcal). Ajoutez une source de glucides ou un dessert pour la masse."
            else:
                status = "VALIDE"
                advice = "Parfait ! Bon apport calorique pour la construction musculaire."

        return {
            "plat": dish_name,
            "calories": calories,
            "confiance_ia": confidence,
            "statut": status,
            "conseil": advice
        }

# --- Exemple d'utilisation (Simulé) ---
# Pour tester sans avoir entraîné, on simule :
if __name__ == "__main__":
    print("Ceci est le module de conseil. Lancez le main.py pour tout connecter.")