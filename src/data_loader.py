import pandas as pd
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tf_keras.utils import to_categorical

# --- CONFIGURATION ---
IMAGE_SIZE = (128, 128) # Taille des images (plus grand que l'OCR car besoin de couleurs)
DATASET_PATH = r"C:\Users\Administrateur\Documents\OCR\.venv\data\Food Images" # Mettez le chemin affiché par votre commande kagglehub
IMAGES_DIR = os.path.join(DATASET_PATH, "Food Images") # Vérifiez le nom exact du dossier images dans votre dossier téléchargé
CSV_FILE = os.path.join(DATASET_PATH, "Recipes.csv")    # Vérifiez le nom exact du CSV

def load_food_data(limit=500):
    """
    Charge les images et les labels, et crée un dictionnaire de calories.
    limit: On limite à 500 plats pour ne pas faire exploser la mémoire au début.
    """
    print("1. Chargement du CSV...")
    df = pd.read_csv(CSV_FILE)
    
    # On suppose que le CSV a des colonnes 'Title', 'Image_Name', 'Calories'
    # Nettoyage : On ne garde que les lignes qui ont une image correspondante
    df = df.dropna(subset=['Image_Name']) 
    df = df.head(limit) # On prend un petit échantillon pour commencer

    images = []
    labels = []
    
    # Dictionnaire pour sauvegarder les infos nutritionnelles : { "NomDuPlat": Calories }
    nutrition_db = {}
    
    # Dictionnaire pour convertir les noms de plats en chiffres (0, 1, 2...)
    unique_dishes = df['Title'].unique()
    label_map = {name: i for i, name in enumerate(unique_dishes)}
    inv_label_map = {i: name for i, name in enumerate(unique_dishes)}

    print(f"2. Chargement des {limit} images...")
    
    for index, row in df.iterrows():
        img_name = row['Image_Name'] + ".jpg" # Ajoutez l'extension si elle manque dans le CSV
        dish_name = row['Title']
        calories = row['Calories'] # Assurez-vous que la colonne s'appelle bien Calories
        
        # Remplir la base de données nutritionnelle
        nutrition_db[dish_name] = calories

        # Chemin complet de l'image
        img_path = os.path.join(IMAGES_DIR, img_name)
        
        try:
            # Lecture et redimensionnement
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, IMAGE_SIZE)
                images.append(img)
                labels.append(label_map[dish_name])
        except Exception as e:
            pass # Si une image est illisible, on l'ignore

    # Conversion en tableaux NumPy
    X = np.array(images, dtype='float32') / 255.0 # Normalisation
    y = np.array(labels)
    y = to_categorical(y, num_classes=len(unique_dishes))

    return X, y, label_map, inv_label_map, nutrition_db