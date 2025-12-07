import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Dictionnaire pour traduire le résultat de l'IA (0 -> A, 1 -> B...)
word_dict = {i: chr(65 + i) for i in range(26)}

def load_trained_model():
    return tf.keras.models.load_model('models/mon_modele_ocr.h5')

def sort_contours(cnts):
    # Fonction pour trier les lettres de gauche à droite
    # Sinon l'IA lira les lettres dans le désordre
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][0]))
    return cnts

def predict_image(image_path, model):
    # 1. Lecture de l'image
    img = cv2.imread(image_path)
    if img is None:
        print("Erreur: Image introuvable.")
        return

    # Copie pour l'affichage final
    img_copy = img.copy()

    # 2. Prétraitement OpenCV (Segmentation)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Flou et Seuillage (Binarisation)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. Trouver les contours (les lettres)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Trier les contours de gauche à droite
    if len(contours) > 0:
        contours = sort_contours(contours)

    full_text = ""

    for c in contours:
        # Récupérer le rectangle autour de la lettre
        x, y, w, h = cv2.boundingRect(c)

        # Filtrer les tout petits bruits qui ne sont pas des lettres
        if w > 10 and h > 10:
            # Découper la lettre (Region of Interest - ROI)
            roi = thresh[y:y+h, x:x+w]

            # Ajouter une bordure noire (padding) pour centrer la lettre
            # C'est crucial car l'IA a appris sur des lettres centrées
            roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))

            # Redimensionner en 28x28 (taille standard de l'IA)
            roi = cv2.resize(roi, (28, 28))
            
            # Préparer pour l'IA (ajouter les dimensions manquantes)
            roi_final = np.reshape(roi, (1, 28, 28, 1))
            roi_final = roi_final / 255.0

            # 4. Prédiction
            prediction = model.predict(roi_final)
            index = np.argmax(prediction)
            lettre = word_dict[index]
            
            full_text += lettre

            # Dessiner un rectangle vert et la lettre sur l'image originale
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_copy, lettre, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    print(f"Texte détecté : {full_text}")
    
    # Afficher le résultat
    plt.imshow(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB))
    plt.title(f"Resultat : {full_text}")
    plt.show()

# --- LANCEMENT ---
if __name__ == "__main__":
    # Assurez-vous d'avoir une image nommée 'test_image.png' dans le dossier racine
    # Ou changez le chemin ci-dessous
    mon_modele = load_trained_model()
    predict_image('test_images/mon_test.png', mon_modele)