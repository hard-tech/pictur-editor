from PIL import Image, ImageFilter
import cv2
import logger
import numpy as np
import os
import sys
from datetime import datetime

arguments = sys.argv

# Fonction pour afficher & enregistrer les messages d'erreur
def print_and_log_msg(err_message):
    maintenant = datetime.now()
    time = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    logger.log(time)
    print(f"\n{err_message}")
    logger.log(err_message)

# Fonction pour renvoyer toutes les lignes contenues dans un fichier sous la forme d'un tableau.
def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'existe pas.")
        return []

# Fonction de transformation d'image
def image_transformation(filters, input_folder: str, output_picture: str):

    # Fonction pour retourner les éléments contenus dans un dossier
    def cat_folder_element(folder):
        folder_elements = os.listdir(folder)
        return folder_elements

    # Attribution des valeurs aux variables requises pour le fonctionnement des filtres
    original_picture = input_folder
    modify_picture = output_picture
    image_names = cat_folder_element(input_folder)
    operation = filters.split('&')

    # Fonction pour sauvegarder les images (dans un dossier en paramètre --> path).
    def save_picture(object, path, name):
        try:
            object.save(f'{path}{name}')
        except:
            print_and_log_msg(f"Impossible de sauvegarder l'image.\n")

    # Fonction pour ouvrir une image et la retourner
    def load_picture(picture_name):
        try:
            image = Image.open(f'{original_picture}{picture_name}')
        except:
            print_and_log_msg(f"Impossible de charger l'image '{picture_name}'.\n")
        return image

    # Pour chaque image du tableau contenant les noms des images faire ...
    for image_name in image_names:
        # initialisation de 'i' pour vérifier si l'image a déjà été modifiée une 1ère fois
        # (dans le cas où il y a plusieurs filtres seul le dernier est conservé.)
        i = 0

        # Vérifier si le format de l'image est un 'jpeg' car ce format s'adapte mal à certaines modifications
        if image_name.split('.')[1] == 'jpeg':
            print_and_log_msg("---- ### Erreur format fichier ### ----")
            print_and_log_msg(f"La modification de l'image '{image_name}' n'est pas supportée avec le format JPEG.\n")
        else:
            # Pour chaque paramètre appliqué à l'image ...
            for param_filter in operation:

                # Si le filtre appliqué est supérieur à 1 prendre l'image dans modify_picture
                if i >= 1:
                    original_picture = modify_picture
                else:
                    # Vérifie si une image existe déjà dans modify_picture (path),
                    # pour appliquer à nouveau le filtre sur l'image déjà modifiée
                    if os.path.exists(f"{modify_picture}{image_name}"):
                        original_picture = modify_picture
                    else:
                        original_picture = input_folder

                try:
                    # -- Story 1 : Appliquer un filtre noir et blanc sur l'image -- #
                    if param_filter == "convert_black_and_white":
                        print_and_log_msg("---- ### Noir & Blanc ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)

                        try:
                            # Convertir l'image en noir et blanc
                            image_noir_et_blanc = image.convert('L')

                            # Sauvegarde de l'image transformée
                            save_picture(image_noir_et_blanc, modify_picture, image_name)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été transformée en noir et blanc.\n")
                        except:
                            # Retourner une erreur
                            print_and_log_msg(f"Impossible de transformer l'image '{image_name}' en noir et blanc. Veuillez vérifier les paramètres (--help).\n")

                    # -- Story 2 : Appliquer un filtre de flou sur l'image -- #
                    elif param_filter == "convert_blur":
                        print_and_log_msg("---- ### Floutage ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)

                        try:
                            # Appliquer un flou à l'image
                            image_blur = image.filter(ImageFilter.BLUR)

                            # Sauvegarde de l'image transformée
                            save_picture(image_blur, modify_picture, image_name)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été floutée.\n")
                        except:
                            # Retourner une erreur
                            print_and_log_msg(f"Impossible de flouter l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")

                    # -- Story 3 : Appliquer un filtre de dilatation sur l'image -- #
                    elif param_filter == "dilate_image":
                        print_and_log_msg("---- ### Dilatation ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)

                        try:
                            # Charge l'image
                            image = cv2.imread(f'{original_picture}{image_name}')

                            # Dilater l'image
                            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            kernel = np.ones((5, 5), np.uint8)
                            image_dilated = cv2.dilate(image_gray, kernel, iterations=1)

                            # Sauvegarde de l'image transformée
                            cv2.imwrite(f'{modify_picture}{image_name}', image_dilated)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été dilatée\n")
                        except:
                            # Retourner une erreur
                            print_and_log_msg(f"Impossible de dilater l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")

                    # -- Story 4 : Appliquer une rotation sur d'un angle donné sur l'image -- #
                    elif param_filter == f"convert_rotate:{param_filter.split(':')[1]}":

                        print_and_log_msg("---- ### Rotation ### ----\n")
                        # Faire pivoter l'image
                        value_rotate = param_filter.split(':')[1]
                        # Charge l'image
                        image = load_picture(image_name)

                        try:
                            # Faire pivoter l'image
                            image_rotate = image.rotate(int(value_rotate))

                            # Sauvegarde de l'image transformée
                            save_picture(image_rotate, modify_picture, image_name)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été tournée de {value_rotate}°.\n")
                        except:
                            # Retourner une erreur
                            print_and_log_msg(f"Impossible d'effectuer une rotation de {value_rotate}° sur l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")

                    # -- Story 5 : Appliquer un redimensionnement de l'image avec une valeur donnée -- #
                    elif param_filter == f"convert_resize:{param_filter.split(':')[1]}":

                        print_and_log_msg("---- ### Redimensionnement ### ----\n")
                        # Demander la nouvelle taille de l'image
                        scaling = param_filter.split(':')[1]
                        scaling = float(scaling)

                        # Chargement l'image
                        image = cv2.imread(f'{original_picture}/{image_name}')
                        height, width = image.shape[:2]

                        try:
                            # Changer la taille de l'image
                            image_resize = cv2.resize(image, ((int(scaling * width), int(scaling * height))), interpolation=cv2.INTER_AREA)

                            # Sauvegarde de l'image transformée
                            cv2.imwrite(f'{modify_picture}/{image_name}', image_resize)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"La taille de l'image '{image_name}' a bien été modifiée.\n")
                        except:
                            print_and_log_msg(f"Impossible de redimensionner l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")

                    # -- Story 6 : Appliquer l'ajout du texte donné en paramètre sur l'image -- #
                    elif param_filter == f"add_text:{param_filter.split(':')[1]}":

                        print_and_log_msg("---- ### Ajout de texte ### ----\n")
                        # Demander ce que l'utilisateur écrit sur l'image
                        text_param = param_filter.split(':')[1]
                        text_to_add = text_param

                        # Charge l'image
                        image = cv2.imread(f'{original_picture}{image_name}')

                        try:
                            # Obtenir les dimensions de l'image
                            image_height, image_width = image.shape[:2]

                            # Définir les paramètres du texte à ajouter
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 5
                            color = (255, 255, 255)  # Couleur du texte en BGR (blanc dans notre cas)
                            thickness = 8

                            # Mesurer la taille du texte pour le centrer
                            text_size = cv2.getTextSize(text_to_add, font, font_scale, thickness)[0]
                            text_width, text_height = text_size[0], text_size[1]

                            # Calculer la position pour centrer le texte
                            text_x = (image_width - text_width) // 2
                            text_y = (image_height + text_height) // 2

                            # Ajouter le texte sur l'image
                            image_with_text = cv2.putText(image, text_to_add, (text_x, text_y), font, font_scale, color, thickness)

                            # Sauvegarde de l'image transformée
                            cv2.imwrite(f'{modify_picture}{image_name}', image_with_text)

                            # Retourner l'état final à l'utilisateur
                            print_and_log_msg(f"Le texte a bien été ajouté sur l'image '{image_name}'.\n")
                        except:
                            # Retourner une erreur
                            print_and_log_msg(f"Impossible d'ajouter du texte sur l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")

                    else:
                        # Retourner une erreur de commande
                        print_and_log_msg("---- ### Erreur opération non reconnue ### ----\n")
                        print_and_log_msg(f"Opération non reconnue : ({param_filter}) taper --help pour plus d'informations\n")

                except:
                    print_and_log_msg(f"Une erreur s'est produite lors de l'exécution du filtre sur l'image '{image_name}'. Veuillez vérifier les paramètres (--help).\n")
                i += 1


# Initialisation des variables
x = 0
input_folder = ''
filters = ''
output_folder = ''
help_needed = False
err_commande = False
configs = False

# Récupération de l'index des arguments de la commande
for cli_name_pic in arguments:
    if cli_name_pic == '--config':
        config_cmd = read_file_lines(f"./{arguments[x+1]}")

        # Retrait des '\n' des paramètres
        config_cmd[0] = config_cmd[0].replace('\n', '')
        config_cmd[1] = config_cmd[1].replace('\n', '')

        for config in config_cmd:
            config_arg = config.split(' ')
            y = 0
            # Récupération de l'index des arguments des commandes (une à une) de config.txt
            for check_arg in config_arg:
                if check_arg == 'filters':
                    filters = config_arg[y+2]

                # Vérification si l'argument correspond à --i du tableau pour pouvoir
                if check_arg == 'input':
                    input_folder = f"./{config_arg[y+2]}/"
                    if not os.path.exists(input_folder):
                        print_and_log_msg(f"Le dossier source n'existe pas, veuillez vérifier le nom.\n")
                        err_commande = True

                if check_arg == 'output':
                    output_folder = f"./{config_arg[y+2]}/"
                    if not os.path.exists(output_folder):
                        print_and_log_msg(f"Le dossier de destination n'existe pas, veuillez vérifier le nom.\n")
                        err_commande = True
                y += 1
    else:
        if cli_name_pic == '--filters':
            filters = arguments[x+1]

        if cli_name_pic == '--i':
            input_folder = f"./{arguments[x+1]}/"
            if not os.path.exists(input_folder):
                print_and_log_msg(f"Le dossier source n'existe pas, veuillez vérifier le nom.\n")
                err_commande = True

        if cli_name_pic == '--o':
            output_folder = f"./{arguments[x+1]}/"
            if not os.path.exists(output_folder):
                print_and_log_msg(f"Le dossier de destination n'existe pas, veuillez vérifier le nom.\n")
                err_commande = True

        if cli_name_pic == '--help':
            help_needed = True
    x += 1

if help_needed:
    help_msg = "Les fonctions disponibles sont : \n\n --filters \n   'convert_black_and_white'\n   'convert_blur'\n   'dilate_image'\n   'convert_rotate'\n     - param (convert_rotate:angl)\n   'convert_resize'\n     - param (convert_resize:Nombre entier déterminant l'échelle {>1 multiplie par X et <1 divise par X})\n   'add_text'\n     - param (add_text:TEXTE À AJOUTER)\n\n Sélection multiple avec [&] --> (exemple : 'convert_blur&convert_black_and_white')\n\n"\
                " --config 'config.txt' (Nom du fichier contenant les commandes à exécuter)\n    - Les commandes doivent impérativement respecter le format : \n       (--filters nomDuFiltre1&nomDuFiltre2:param --i nomDossierSource --o nomDossierDestination) \n\n"\
                " --i 'dossier_source' (Nom du dossier contenant les images à modifier)\n\n"\
                " --o 'dossier_destination' (Nom du dossier qui contiendra les images modifiées)\n"\
                "\n"
    print_and_log_msg(help_msg)
else:
    if not err_commande:
        try:
            image_transformation(filters, input_folder, output_folder)
        except:
            print_and_log_msg("La commande n'a pas été reconnue, tapez '--help' pour plus d'informations.\n")