import pandas as pd
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tf_keras.utils import to_categorical

# --- CONFIGURATION ---
IMAGE_SIZE = (128, 128)  # Taille des images (plus grand que l'OCR car besoin de couleurs)

# Base data folder (point this to the folder that contains the CSV and images).
# In this workspace the dataset is commonly placed under `.venv/data` (but
# ideally move your dataset out of `.venv` to `data/` so the venv can be
# recreated without losing data).
DATASET_PATH = r"C:\Users\Administrateur\Documents\OCR\.venv\data"

# Attempt to auto-detect the CSV file and the images folder inside DATASET_PATH.
import glob

csv_candidates = glob.glob(os.path.join(DATASET_PATH, "*.csv"))
if not csv_candidates:
    raise FileNotFoundError(f"No CSV file found in {DATASET_PATH}. Please place the CSV there or update DATASET_PATH.")

# Use the first CSV found (adjust if multiple exist)
CSV_FILE = csv_candidates[0]

# Try common image folder names under DATASET_PATH, otherwise pick any folder that
# contains image files.
possible_image_dirs = [
    os.path.join(DATASET_PATH, "Food Images"),
    os.path.join(DATASET_PATH, "images"),
    os.path.join(DATASET_PATH, "Images"),
    os.path.join(DATASET_PATH, "food_images"),
]

IMAGES_DIR = None
for d in possible_image_dirs:
    if os.path.isdir(d):
        IMAGES_DIR = d
        break

if IMAGES_DIR is None:
    # Fallback: find any subdirectory with jpg or jpeg files
    for sub in glob.glob(os.path.join(DATASET_PATH, "*")):
        if os.path.isdir(sub):
            jpgs = glob.glob(os.path.join(sub, "*.jpg")) + glob.glob(os.path.join(sub, "*.jpeg"))
            if jpgs:
                IMAGES_DIR = sub
                break

if IMAGES_DIR is None:
    # If still None, set to DATASET_PATH (in case images are placed directly there)
    IMAGES_DIR = DATASET_PATH


def load_food_data(limit=500):
    """
    Charge les images et les labels, et crée un dictionnaire de calories.
    limit: On limite à 500 plats pour ne pas faire exploser la mémoire au début.
    """
    print("1. Chargement du CSV...")
    df = pd.read_csv(CSV_FILE)

    # Detect common column names (case-insensitive and variants)
    cols_lower = {c.lower(): c for c in df.columns}

    def find_col(possible_names):
        for name in possible_names:
            if name.lower() in cols_lower:
                return cols_lower[name.lower()]
        # try substring matches
        for name in df.columns:
            for p in possible_names:
                if p.lower() in name.lower():
                    return name
        return None

    title_col = find_col(['title', 'name', 'dish', 'recipe'])
    image_col = find_col(['image_name', 'imagename', 'image', 'image_id', 'file_name', 'filename'])
    calories_col = find_col(['calories', 'calorie', 'energy', 'kcal'])

    if title_col is None or image_col is None:
        raise KeyError(f"Required columns not found in CSV. Detected columns: {list(df.columns)}")

    # Nettoyage : On ne garde que les lignes qui ont une image correspondante
    df = df.dropna(subset=[image_col])
    df = df.head(limit) # On prend un petit échantillon pour commencer

    images = []
    labels = []
    
    # Dictionnaire pour sauvegarder les infos nutritionnelles : { "NomDuPlat": Calories }
    nutrition_db = {}
    
    # Dictionnaire pour convertir les noms de plats en chiffres (0, 1, 2...)
    unique_dishes = df[title_col].unique()
    label_map = {name: i for i, name in enumerate(unique_dishes)}
    inv_label_map = {i: name for i, name in enumerate(unique_dishes)}

    print(f"2. Chargement des {limit} images...")
    
    for index, row in df.iterrows():
        raw_img_name = str(row[image_col])
        # Ajoutez l'extension si elle manque dans le CSV
        img_name = raw_img_name if raw_img_name.lower().endswith(('.jpg', '.jpeg', '.png')) else raw_img_name + ".jpg"
        dish_name = row[title_col]
        # Calories may be missing; fall back to None
        calories = None
        if calories_col is not None:
            try:
                calories = row[calories_col]
            except Exception:
                calories = None
        
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
            else:
                # Image not found; optionally log or continue
                continue
        except Exception:
            # If an image is unreadable, ignore and continue
            continue

    # Conversion en tableaux NumPy
    X = np.array(images, dtype='float32') / 255.0 # Normalisation
    y = np.array(labels)
    y = to_categorical(y, num_classes=len(unique_dishes))

    return X, y, label_map, inv_label_map, nutrition_db