import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tf_keras.utils import to_categorical
from src.food_model import create_model # On importe notre fonction du fichier précédent
import os

# --- CONFIGURATION ---
CSV_PATH = 'data/raw/A_Z Handwritten Data.csv'
MODEL_SAVE_PATH = 'models/mon_modele_ocr.h5'

print("1. Chargement des données (Patientez, fichier volumineux)...")
data = pd.read_csv(CSV_PATH).astype('float32')

# Séparation des pixels (X) et des réponses (y)
X = data.drop('0', axis=1) # Tout sauf la première colonne
y = data['0']              # Juste la première colonne (le label)

print("2. Préparation des images...")
# On découpe en train (80%) et test (20%) pour vérifier si l'IA apprend bien
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Redimensionnement : On passe d'une ligne de 784 chiffres à une image 28x28
X_train = np.reshape(X_train.values, (X_train.shape[0], 28, 28, 1))
X_test = np.reshape(X_test.values, (X_test.shape[0], 28, 28, 1))

# Normalisation (0-255 -> 0-1)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Encodage des réponses (le chiffre 0 devient [1, 0, 0, ...])
y_train = to_categorical(y_train, num_classes=26)
y_test = to_categorical(y_test, num_classes=26)

print("3. Création et Entraînement du modèle...")
model = create_model()

# Lancement de l'apprentissage
# epochs=5 signifie qu'il va lire tout le dataset 5 fois.
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=64)

print("4. Sauvegarde du modèle...")
if not os.path.exists('models'):
    os.makedirs('models')
model.save(MODEL_SAVE_PATH)
print(f"Bravo ! Modèle sauvegardé sous : {MODEL_SAVE_PATH}")