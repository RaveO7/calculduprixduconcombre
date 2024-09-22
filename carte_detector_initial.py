import cv2
import pytesseract
import difflib
import numpy as np
import shutil
import time
import os

# Définir le chemin de tesseract si nécessaire (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def setup_directory(directory):
    # Supprime l'ancien dossier s'il existe
    if os.path.exists(directory):
        shutil.rmtree(directory)

    # Crée un nouveau dossier
    os.makedirs(directory)


def detect_dominant_color(roi):
    # Convertir l'image en espace de couleur HSV
    hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Calculer l'histogramme pour la composante H (teinte)
    hist_hue = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])

    # Trouver la valeur de teinte dominante
    dominant_hue = np.argmax(hist_hue)

    # Définir les seuils pour les couleurs dominantes
    if 0 <= dominant_hue < 10 or 160 <= dominant_hue < 180:
        return 'h'  # hearts
    elif 35 <= dominant_hue < 85:
        return 'c'  # clubs
    elif 85 <= dominant_hue < 130:
        return 'd'  # diamonds
    elif 130 <= dominant_hue < 160:
        return 's'  # spades
    else:
        return 'unknown'

last_detected_cards = []
def detect_flop_card(image_path, dir):
    global last_detected_cards  # Utilisation de la variable globale pour mémoriser le dernier tableau

    # Charger l'image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Impossible de charger l'image : {image_path}")
        return []

    # Coordonnées des régions d'intérêt (x, y, w, h)
    rois = [
        (320, 256, 20, 40),
        (387, 256, 20, 40),
        (454, 256, 20, 40),
        (521, 256, 20, 40),
        (588, 256, 20, 40),
    ]

    # Utiliser Tesseract pour extraire le texte des cartes
    custom_config = r'--oem 3 --psm 6'
    
    # Définir les valeurs de cartes à rechercher
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    
    detected_cards = []

    for i, (x, y, w, h) in enumerate(rois):
        roi = image[y:y+h, x:x+w]

        if roi.size == 0:
            print(f"ROI {i+1} est vide ou invalide.")
            continue

        # Convertir l'image en niveaux de gris pour améliorer la précision de l'OCR
        gray_image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un seuil pour améliorer la reconnaissance
        _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Extraire le texte de l'image
        text = pytesseract.image_to_string(thresh_image, config=custom_config).strip()
        
        # Convertir le texte extrait en une liste de mots
        detected_values = text.split()
        
        # Sauvegarder l'image de la région d'intérêt pour vérification
        # cv2.imwrite(f'card_{i+1}.png', roi)
        cv2.imwrite(os.path.join(dir, f'card_board_{i+1}.png'), roi)

        # Vérifier les valeurs détectées contre les valeurs de cartes et trouver les correspondances les plus proches
        card_value = None
        for value in detected_values:
            if value in card_values:
                card_value = value
                break
            else:
                closest_value = get_closest_value(value, card_values)
                if closest_value:
                    card_value = closest_value
                    break

        # Détection de la couleur dominante
        dominant_color = detect_dominant_color(roi)
        
        # Si une valeur de carte a été détectée, l'ajouter avec sa couleur
        if card_value:
            if dominant_color != "unknown":
                detected_cards.append(f"{card_value}{dominant_color}")

    # Comparaison avec le dernier tableau détecté
    if len(last_detected_cards) > len(detected_cards) and len(detected_cards) != 0:
        detected_cards = last_detected_cards
    else:
        last_detected_cards = detected_cards

    

    return detected_cards
   
def get_closest_value(detected_value, card_values):
    closest_match = difflib.get_close_matches(detected_value, card_values, n=1, cutoff=0.0)
    return closest_match[0] if closest_match else None

def detect_card_values(image_path, dir):
    # Charger l'image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Impossible de charger l'image : {image_path}")
        return []

    # Coordonnées des régions d'intérêt (x, y, w, h)
    rois = [
        (419, 450, 20, 45),
        (481, 450, 20, 45),
    ]

    # Utiliser Tesseract pour extraire le texte des cartes
    custom_config = r'--oem 3 --psm 6'
    
    # Définir les valeurs de cartes à rechercher
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    
    detected_cards = []

    for i, (x, y, w, h) in enumerate(rois):
        roi = image[y:y+h, x:x+w]

        if roi.size == 0:
            print(f"ROI {i+1} est vide ou invalide.")
            continue

        # Convertir l'image en niveaux de gris pour améliorer la précision de l'OCR
        gray_image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un seuil pour améliorer la reconnaissance
        _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Extraire le texte de l'image
        text = pytesseract.image_to_string(thresh_image, config=custom_config).strip()
        
        # Convertir le texte extrait en une liste de mots
        detected_values = text.split()
        
        # Sauvegarder l'image de la région d'intérêt pour vérification
        # cv2.imwrite(f'card_{i+1}.png', roi)
        cv2.imwrite(os.path.join(dir, f'card_{i+1}.png'), roi)

        # Vérifier les valeurs détectées contre les valeurs de cartes et trouver les correspondances les plus proches
        card_value = None
        for value in detected_values:
            if value in card_values:
                card_value = value
                break
            else:
                closest_value = get_closest_value(value, card_values)
                if closest_value:
                    card_value = closest_value
                    break

        # Détection de la couleur dominante
        dominant_color = detect_dominant_color(roi)
        
        # Si une valeur de carte a été détectée, l'ajouter avec sa couleur
        if card_value:
            if dominant_color != "unknown":
                detected_cards.append(f"{card_value}{dominant_color}")

    return detected_cards
  
def detect_button_player(image_path, dir):
    # Charger l'image
    image = cv2.imread(image_path)

    # Utiliser Tesseract pour extraire le texte des cartes
    custom_config = r'--oem 3 --psm 6'

    # Coordonnées des boutons (x, y, w, h)
    buttons_coords = [
        (763, 248, 30, 30),  # Button player_right
        (165, 248, 30, 30),   # Button player_left
    ]

    # Liste pour stocker les informations des boutons
    button_info = []

    # Boucle à travers les coordonnées des boutons
    for i, (x, y, w, h) in enumerate(buttons_coords):
        roi_button = image[y:y+h, x:x+w]

        # Convertir en niveaux de gris et appliquer un seuil pour améliorer l'OCR
        gray_button = cv2.cvtColor(roi_button, cv2.COLOR_BGR2GRAY)

        # Appliquer un seuil pour ne garder que le noir et enlever les autres couleurs
        _, thresh_button = cv2.threshold(gray_button, 150, 255, cv2.THRESH_BINARY_INV)

        # Inverser les couleurs pour que le texte soit noir sur fond blanc
        thresh_button = cv2.bitwise_not(thresh_button)

        # Utiliser Tesseract pour extraire le texte des informations du bouton
        text_button = pytesseract.image_to_string(thresh_button, config=custom_config)

        # Nettoyer et vérifier la présence du symbole "D"
        button_info.append(text_button.strip())

        # Sauvegarder l'image de la région d'intérêt
        # cv2.imwrite(f'button_{i+1}.png', roi_button)
        cv2.imwrite(os.path.join(dir, f'button_{i+1}.png'), roi_button)

    # Vérifier la présence du symbole "D" dans les informations des boutons
    if "©" in button_info or "D)" in button_info or "D" in button_info or "d" in button_info:
        if "©" in button_info[0] or "D)" in button_info[0] or "D" in button_info[0] or "d" in button_info[0]:
            return ["sb", "bb", "btn"]
        else:
            return ["bb", "btn", "sb"]
    else:
        return ["btn", "sb", "bb"]   
   
def size_of_pot(image_path, dir):
    # Charger l'image
    image = cv2.imread(image_path)

    # Coordonnées du pot total (x, y, w, h)
    x, y, w, h = 400, 225, 150, 27

    roi_pot = image[y:y+h, x:x+w]
    
    # Convertir en niveaux de gris et appliquer un seuil pour améliorer l'OCR
    gray_pot = cv2.cvtColor(roi_pot, cv2.COLOR_BGR2GRAY)
    _, thresh_pot = cv2.threshold(gray_pot, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Utiliser Tesseract pour extraire le texte du pot total
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text_pot = pytesseract.image_to_string(thresh_pot, config=custom_config)
    
    # Nettoyer les informations du pot total
    pot_info = text_pot.replace("Pot:", "").replace(",", ".").strip()
    
    # Sauvegarder l'image de la région d'intérêt
    cv2.imwrite(os.path.join(dir, f'pot_total.png'), roi_pot)

    return int(pot_info)

last_blind = 20
previous_pot_value = None
round = 1
def monitor_pot(total_pot):
    global previous_pot_value
    global last_blind
    global round

    # Obtenir la valeur actuelle du pot
    current_pot_value = total_pot

    # Vérifier si la valeur précédente du pot est définie
    if previous_pot_value is not None:
        # Comparer la valeur actuelle avec la valeur précédente
        if current_pot_value < previous_pot_value:
            # Appeler la fonction bb
            bb(total_pot)
            if total_pot == last_blind + last_blind/2:
                round += 1
    # Mettre à jour la valeur précédente du pot
    previous_pot_value = current_pot_value

    return last_blind

def bb(new_blind):
    global last_blind

    # Calculer le nouveau blind
    new_blind_value = int(new_blind / 3 * 2)

    # Comparer le nouveau blind avec l'ancien
    if last_blind is None or new_blind_value > last_blind and new_blind_value-20 < last_blind and new_blind_value == 30 or new_blind_value == 40 or new_blind_value == 60 or new_blind_value == 80 or new_blind_value == 100 or new_blind_value == 120:        
        if last_blind == 20 and new_blind_value == 30:
            last_blind = new_blind_value
        elif last_blind == 30 and new_blind_value == 40:
            last_blind = new_blind_value
        elif last_blind + 20 == new_blind_value:
            last_blind = new_blind_value
        elif last_blind == 120 and new_blind_value == 160:
            last_blind = new_blind_value
        elif last_blind == 160 and new_blind_value == 200:
            last_blind = new_blind_value
         
    return last_blind

def size_stacks(image_path, dir):
    image = cv2.imread(image_path)

    # Liste pour stocker les informations de chaque joueur
    player_values = []
    result_player = []

    # Coordonnées des joueurs (x, y, w, h)
    players_coords = [
        [
            (457, 555, 11, 17),  # BB player
            (464, 555, 11, 17),  # BB player
            (474, 555, 11, 17),  # BB player
            (484, 555, 11, 17),  # BB player            
            (450, 555, 60, 17),  # BB player
        ],
        [
            (99, 224, 10, 17),
            (106, 224, 11, 17),   # BB player_left
            (117, 224, 11, 17),   # BB player_left
            (127, 224, 11, 17),   # BB player_left     
            (75, 224, 95, 18),   # BB player_left
        ],
        [
            (815, 224, 10, 17),
            (822, 224, 11, 17),   # BB player_right
            (832, 224, 11, 17),   # BB player_right
            (843, 224, 11, 17),   # BB player_right
            (800, 224, 95, 17)   # BB player_right
        ]   
    ]

    all_results = [] # Liste pour stocker les résultats de chaque tableau

    for coords_set in players_coords:
        result_player = [] # Réinitialiser result_player pour chaque set de coordonnées
        for i, (x, y, w, h) in enumerate(coords_set):
            # Extraire la région d'intérêt
            roi_pot = image[y:y+h, x:x+w]
            img_gray = cv2.cvtColor(roi_pot, cv2.COLOR_BGR2GRAY)

            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789-)|'
            result = pytesseract.image_to_string(img_gray, config=custom_config).strip()

            if result == "|":
                result = "1"

            if result == ")":
                result = "9"

            # print(f"Resultat coordonnée {i+1}: {result}")
                            
            result_player.append(result)

            # Sauvegarder l'image de la région d'intérêt
            # cv2.imwrite(f'stack_{i+1}.png', roi_pot)
            cv2.imwrite(os.path.join(dir, f'stack_{i+1+x}.png'), roi_pot)

        # Vérification des résultats pour le set de coordonnées actuel
        if result_player[0] == "1":
            # Utiliser uniquement la capture de la dernière coordonnée
            last_result = result_player[-1]
            # print(f"Utilisation de la dernière coordonnée : {last_result}")
            # print(last_result)
            all_results.append(last_result) 
        else:
            # Utiliser les coordonnées 2, 3, 4
            additional_results = result_player[1:4] 
            concatenated_result = ''.join(map(str, additional_results))
            # print(f"Résultats concaténés : {concatenated_result}")
            # print(concatenated_result)
            if concatenated_result == "":
                all_results.append("-1")
            elif concatenated_result == "11":
                all_results.append("0")
            else:
                all_results.append(concatenated_result)
    # print(all_results)
    return all_results








last_round = 0
last_street = None
def merge_info(size_of_stacks, btn_info, blind_value, total_pot, detected_cards, detected_board):
    merged_info = []
    global round
    global last_street
    global last_round
    
    merged_info.append(detected_cards)
    # Fusionner les informations des BB et des boutons
    for i, btn in enumerate(btn_info):
        if i < len(size_of_stacks):
            merged_info.append([btn, int(size_of_stacks[i])])
        else:
            merged_info.append([btn, None])

    # Ajouter le total_pot converti en float
    merged_info.append([total_pot])
    merged_info.append(detected_board)
    
    if last_round != round:
        print("Round: ", round)
        print(detected_cards)
        print("Blind: ", blind_value/2,"/",blind_value)
    print("Pot: ", total_pot)
        
        # for i in range(len(btn_info)):
        #     print(f"{btn_info[i]} / stack: {size_of_stacks[i]}")
        # last_round = round

    for i in range(len(btn_info)):
        print(f"{btn_info[i]} / stack: {size_of_stacks[i]}")
    last_round = round
            
    if last_street != detected_board:
        if len(detected_board) == 3:
            print("Flop: ", detected_board)
    
        elif len(detected_board) == 4:
            print("Turn: ", detected_board)

        elif len(detected_board) == 5:
            print("River: ", detected_board)
        else:
            print("Prelop: ", detected_board)
        last_street = detected_board

    # if total_pot+ sum(size_of_stacks) != 1500:    
    #     print("ERREUR: ", total_pot+ sum(size_of_stacks))
    # else:
    #     print(total_pot+ sum(size_of_stacks))
    







previous_stacks = []

def main(x):
    global previous_stacks
    image_path = 'screen.png'  # Chemin de votre image
    dir = "partie"
    
    image_dir = "screenshot"  # Assurez-vous que ce dossier est le bon
    image_path = os.path.join(image_dir, f'screenshot_{x}.png')  # Utilisation de f-string pour insérer la variable x
    max_attempts = 10
    attempts = 0

    # Attendre que l'image "screenshot_1.png" soit créée dans le dossier "screenshot"
    while not os.path.exists(image_path):
        time.sleep(1)  # Attendre 1 seconde avant de vérifier à nouveau

        if attempts >= max_attempts:
            print("Aucune nouvelle image n'a été trouvée après plusieurs tentatives.")
            return
        print(f"Attente de la création de l'image '{image_path}'...")
        attempts += 1
    print(x)

    # Configurer le dossier pour les images
    setup_directory(dir)


    
    size_of_stacks = size_stacks(image_path, dir)
    btn_info = detect_button_player(image_path, dir)
    total_pot = size_of_pot(image_path, dir)
    blind_value = monitor_pot(total_pot)
    detected_cards = detect_card_values(image_path, dir)
    detected_board = detect_flop_card(image_path, dir)

    # Fusionner les informations
    merged_info = merge_info(size_of_stacks, btn_info, blind_value, total_pot, detected_cards, detected_board)
    

    
    x += 1
    # return
    main(x)
    
if __name__ == "__main__":
    x = 1
    main(x)
    
    # 110 - 126 nouvelle table se lance
    # 274 se remmetre en jeux
    # 370 fin de partie
    
    # 103 enlever les animations dans les parametres
    # 187 - 202 nouvelle table se lance
    # 281 282 se remmetre en jeux
    # 390 fin
    
    #22-24
    
    # ajouter une fonction qui définit si c'est mon tour/ ajouter une fonction qui définit si il y a 3 ou 2 joueur
    
    # petit erreur au moment ou les carte se retourne mais probleme résolut si on eneleve les animations dans les parametres
    # ne pas mettre en bb met en nombre de jeton pour eviter les erreurs de stack
    
    
    #  si un player = -1 alors à perdu/ si un joeur 0 alors shove