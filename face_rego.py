import cv2
import cx_Oracle
from datetime import datetime

# Charger le classifieur de visage pré-entraîné
face_cascade = cv2.CascadeClassifier('xml version.xml')

# Charger les images des personnes connues et leurs noms
known_faces = [
    {'image_path': 'WIN_20230515_11_03_11_Pro.jpg', 'name': 'nidhal'},
    {'image_path': 'WIN_20230515_12_35_20_Pro.jpg', 'name': 'feriel'},
    {'image_path': 'WIN_20230516_12_12_59_Pro.jpg', 'name': 'hatem'},
    {'image_path': 'WIN_20230516_12_14_27_Pro.jpg', 'name': 'badis'},
    # Ajoutez autant d'images et de noms que vous le souhaitez
]

# Connexion à la base de données Oracle
conn = cx_Oracle.connect('system/123@localhost:1521/xe')
cursor = conn.cursor()

# Charger les visages connus et les noms correspondants
known_encodings = []
known_names = []
for known_face in known_faces:
    image = cv2.imread(known_face['image_path'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in face:
        face_encoding = gray[y:y + h, x:x + w]
        hist = cv2.calcHist([face_encoding], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        known_encodings.append(hist)
        known_names.append(known_face['name'])

# Capturer les images de la caméra en temps réel
cap = cv2.VideoCapture(0)

while True:
    # Lire le flux vidéo image par image
    ret, frame = cap.read()

    # Vérifier si la lecture de l'image a réussi
    if not ret:
        print("Échec de la lecture de l'image depuis la caméra.")
        break

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Parcourir les visages détectés
    for (x, y, w, h) in faces:
        face_encoding = gray[y:y + h, x:x + w]
        hist = cv2.calcHist([face_encoding], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        # Comparer avec les visages connus
        matches = []
        for known_encoding in known_encodings:
            # Vérifier que les histogrammes sont de même profondeur et type
            if hist.dtype != known_encoding.dtype:
                 known_encoding = known_encoding.astype(hist.dtype)
            if hist.shape != known_encoding.shape:
                 hist = cv2.resize(hist, known_encoding.shape)

            # Calculer la similarité entre le visage détecté et les visages connus
            similarity = cv2.compareHist(hist, known_encoding, cv2.HISTCMP_CORREL)
            matches.append(similarity)

                # Trouver l'indice de la correspondance la plus élevée
        best_match_index = matches.index(max(matches))
        name = known_names[best_match_index]

            # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Afficher le nom correspondant à côté du visage détecté
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Enregistrer le visage détecté avec l'heure et le nom associé dans la base de données
        timestamp = datetime.now().strftime("%d-%b-%Y ")
        image_data = cv2.imencode('.jpg', frame[y:y + h, x:x + w])[1].tostring()

        cursor.execute("""INSERT INTO faces (name, timestamp, image) VALUES (:name, :timestamp, :image)""", (name, timestamp, image_data))


        conn.commit()

        print("Visage enregistré dans la base de données.")

            # Afficher l'image résultante
    cv2.imshow('Reconnaissance faciale', frame)

        # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break

        # Fermer la connexion à la base de données Oracle
cursor.close()
conn.close()

    # Libérer la capture de la caméra et détruire toutes les fenêtres
cap.release()
cv2.destroyAllWindows()
