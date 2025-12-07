from tf_keras.models import Sequential
from tf_keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def create_food_cnn(num_classes):
    model = Sequential()

    # Bloc 1 : Détection des formes simples
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(MaxPooling2D(2, 2))

    # Bloc 2 : Détection des textures
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))

    # Bloc 3 : Détection complexe (ingrédients)
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Flatten())
    
    # Couches Denses
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5)) # Évite le sur-apprentissage
    
    # Couche de sortie : Autant de neurones que de plats différents
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model