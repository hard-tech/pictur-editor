from PIL import Image, ImageFilter
import cv2
import logger
import numpy as np
import os
import sys
from datetime import datetime

arguments = sys.argv

# Fonction qui afficher & log les message d'erreur
def print_and_log_msg(err_message):
    maintenant = datetime.now()
    time = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    logger.log(time)
    print(f"\n{err_message}")
    logger.log(err_message)

def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = []
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'existe pas.")
        return []

def image_transformation(filters,input_folder:str,output_picture:str):

    def cat_folder_element(folder):
        folder_elements = os.listdir(folder)
        return folder_elements

    original_picture = input_folder
    modify_picture = output_picture
    image_names = cat_folder_element(input_folder)
    operation = filters.split('&')

    def save_picture(object, path, name):
        try:
            object.save(f'{path}{name}')
        except:
            print_and_log_msg(f"Impossible de sauvegarder l'image.\n")

    def load_picture(picture_name):
        try:
            image = Image.open(f'{original_picture}{picture_name}')
        except:
            print_and_log_msg(f"Impossible de charger l'image '{picture_name}'.\n")
        return image

    
    # Pour chaque image du dossier faire ...
    for image_name in image_names:        
        # initialisation de 'i' pour vérifier si l'image à déjà été modifier une 1ère fois (dans le cas où il y a plusieur filtres seul le dernier est conserver.)
        i = 0

        # Vérifier si le format de l'image est un 'jpeg' car ce format s'addapte mal à certainne modification
        if image_name.split('.')[1] == 'jpeg':
            print_and_log_msg("---- ### Erreur format fichier ### ----\n")
            print_and_log_msg(f"La modification de l'image '{image_name}' n'est pas supporter avec le format JPEG.\n")
        else :
            # Pour chaque paramètre appliquer à l'image ...
            for param_filter in operation:

                # Si le filtre appliquer est suppérieur à 1 prendre l'image dans modify_picture
                if i >= 1:
                    original_picture = modify_picture
                else:
                    # Vérifie si une l'image existe déjà dans modify_picture (path) pour appliquer a nouveau filtre sur l'image déjà modifier
                    if os.path.exists(f"{modify_picture}{image_name}"):
                        original_picture = modify_picture
                    else:
                        original_picture = input_folder
                
                try:
                    # -- Story 1  -- #
                    if param_filter == "convert_black_and_white":
                        print_and_log_msg("---- ### Noir & Blanc ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)

                        try:
                            # Convertir l'image en noir et blanc
                            image_noir_et_blanc = image.convert('L')

                            # Sauvegarde de l'image transformé
                            save_picture(image_noir_et_blanc, modify_picture, image_name)
                            
                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été transformée en noir et blanc.\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible de transformée l'image '{image_name}' en noir et blanc. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 2  -- #
                    elif param_filter == "convert_blur":
                        print_and_log_msg("---- ### Floutage ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)
                        
                        # Vérifier si l'image s'ouvre
                        try:
                            # Appliquer un flou à l'image
                            image_blur = image.filter(ImageFilter.BLUR)
                            
                            # Sauvegarde de l'image transformé
                            save_picture(image_blur, modify_picture, image_name)

                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été floutée.\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible de floutée l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 3  -- #
                    elif param_filter == "dilate_image":
                        print_and_log_msg("---- ### Dilatation ### ----\n")
                        # Charge l'image
                        image = load_picture(image_name)
                        
                        # Vérifier si l'image s'ouvre
                        try:
                            # Charge l'image
                            image = cv2.imread(f'{original_picture}{image_name}')
                            
                            # Dilater l'image
                            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            kernel = np.ones((5, 5), np.uint8)
                            image_dilated = cv2.dilate(image_gray, kernel, iterations=1)

                            # Sauvegarde de l'image transformé
                            cv2.imwrite(f'{modify_picture}{image_name}', image_dilated)

                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été dilate\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible de dilaté l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 4  -- #
                    elif param_filter == f"convert_rotate:{param_filter.split(':')[1]}":
                        
                        print_and_log_msg("---- ### Rotation ### ----\n")
                        # Faire pivoter l'image
                        value_rotate = param_filter.split(':')[1]
                        # Charge l'image
                        image = load_picture(image_name)
                        # Vérifier si l'image s'ouvre
                        try:
                            # Faire pivoter l'image
                            image_rotate = image.rotate(int(value_rotate))

                            # Sauvegarde de l'image transformé
                            save_picture(image_rotate,modify_picture,image_name)
                            
                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été tournée de {value_rotate}°.\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible d'effectuer une rotation de {value_rotate}° sur l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 5  -- #
                    elif param_filter == f"convert_resize:{param_filter.split(':')[1]}":

                        print_and_log_msg("---- ### Redimensionnement ### ----\n")
                        # Demander la nouvelle taille de l'image
                        scaling = param_filter.split(':')[1]
                        scaling = float(scaling)

                        # Chargement l'image
                        image = cv2.imread(f'{original_picture}/{image_name}')
                        height, width = image.shape[:2]
                        # Vérifier si l'image transformée existe déjà

                        try:
                            # Changer la taille de l'image
                            image_resize = cv2.resize(image, ((int(scaling *width), int(scaling *height))), interpolation=cv2.INTER_AREA)

                            # Sauvegarde de l'image transformé
                            cv2.imwrite(f'{modify_picture}/{image_name}', image_resize)

                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"La taille de l'image '{image_name}' a bien été modifiée.\n")
                            # logger.log('une erreur s\'est produite lors de l\'execution de la demande' + '\n')
                        except :
                            print_and_log_msg(f"Impossible de redimentioner l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 6  -- #
                    elif param_filter == f"add_text:{param_filter.split(':')[1]}":
                        
                        print_and_log_msg("---- ### Redimensionnement ### ----\n")
                        # Demmander ce que l'utilisateur écrire sur l'image
                        text_param = param_filter.split(':')[1]
                        text_to_add = text_param

                        # Charge l'image
                        image = cv2.imread(f'{original_picture}{image_name}')
                        
                        # Vérifier si l'image s'ouvre
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

                            # Sauvegarde de l'image transformé
                            cv2.imwrite(f'{modify_picture}{image_name}', image_with_text)
                            
                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"Le texte à bien été ajouter sur l'image '{image_name}'.\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible d'ajouter du texte sur l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")

                    # -- Story 14  -- #   
                    elif param_filter == "convert_aquaraelle":
                        print_and_log_msg("---- ### Filtre Aquarelle ### ----\n")
                        
                        # Charge l'image
                        image = load_picture(image_name)
                        
                        try:
                            # Convertir l'image en noir et blanc
                            watercolor_image = cv2.stylization(image, sigma_s=60, sigma_r=0.6)

                            # Sauvegarde de l'image transformé
                            save_picture(watercolor_image, modify_picture, image_name)
                            
                            # Retour l'état final à l'utilisateur
                            print_and_log_msg(f"L'image '{image_name}' a bien été transformée en noir et blanc.\n")
                        except :
                            # Retour erreur
                            print_and_log_msg(f"Impossible de transformée l'image '{image_name}' en noir et blanc. Veuillez vérifier les paramètre (--help).\n")

                    else:
                        # Retour erreur commande
                        print_and_log_msg("---- ### Erreur opération non reconnue ### ----\n")
                        print_and_log_msg(f"Opération non reconnue : ({param_filter}) tapper --help pour plus d'information\n")

                except:
                    print_and_log_msg(f"Une erreur c'est produite lors de l'éxécution du filtre sur l'image '{image_name}'. Veuillez vérifier les paramètre (--help).\n")
                i+=1


# init valeurs
x = 0
input_folder=''
filters=''
output_folder = ''
help = False
err_commande = False
configs = False
# Récupère l'index des arguments de la commande
for cli_name_pic in arguments:
    if cli_name_pic == '--config' :
        print('configs')
        
        config_cmd = read_file_lines(f"./{arguments[x+1]}")
        config_cmd[0] = config_cmd[0].replace('\n', '')
        configs = True

        for config in config_cmd:
            config_arg = config.split(' ')
            y = 0
            for check_arg in config_arg:
                if check_arg == '--filters':
                    filters = config_arg[y+1]

                if check_arg == '--i':
                    input_folder = f"./{config_arg[y+1]}/"
                    if not os.path.exists(input_folder):
                        print_and_log_msg(f"Le dossier source n'existe pas, verifier le nom.\n")
                        err_commande = True

                if check_arg == '--o':
                    output_folder = f"./{config_arg[y+1]}/"
                    if not os.path.exists(output_folder):
                        print_and_log_msg(f"Le dossier de destination n'existe pas, verifier le nom.\n")
                        err_commande = True
                y += 1
            # execute les filtres pour chaque ligne du config.txt
            image_transformation(filters, input_folder, output_folder)
    else :
        if cli_name_pic == '--filters':
            filters = arguments[x+1]

        if cli_name_pic == '--i':
            input_folder = f"./{arguments[x+1]}/"
            if not os.path.exists(input_folder):
                print_and_log_msg(f"Le dossier source n'existe pas, verifier le nom.\n")
                err_commande = True

        if cli_name_pic == '--o':
            output_folder = f"./{arguments[x+1]}/"
            if not os.path.exists(output_folder):
                print_and_log_msg(f"Le dossier de destination n'existe pas, verifier le nom.\n")
                err_commande = True
        
        # if cli_name_pic == '--config':
        #     config_cmd = read_file_lines(f"./{arguments[x+1]}")
        #     config_cmd[0] = config_cmd[0].replace('\n', '')
        #     configs = True

        if cli_name_pic == '--help':
            help = True
    x+=1

if help:
    help_msg = "Les fonctions sont : \n\n --filters \n   'convert_black_and_white'\n   'convert_blur'\n   'dilate_image'\n   'convert_rotate'\n     - param (convert_rotate:angl)\n   'convert_resize'\n     - param (convert_resize:Nombre entier qui détermine de combien {>1 multiplie par X et <1 divise par X})\n   'add_text'\n     - param (add_text:TEXT TO ADD)\n\n Selection multible avec [&] --> (exemple : 'convert_blur&convert_black_and_white')\n\n"\
                " --config 'config.txt' (Nom du fichier contenant les commande à executer)\n    - Les commandes doivent impérativement respecter la forme : \n       (--filters filterName1&filterName2:param --i source_name_fold --o destination_name_fold) \n\n"\
                " --i 'original_picture' (Nom du dossier contenant les images à modifier)\n\n"\
                " --o 'modify_picture' (Nom du dossier qui contiendra les images modifier)\n"\
                "\n"
    print_and_log_msg(help_msg)
else:
    if not err_commande :
        try:
            if not configs:
                image_transformation(filters, input_folder, output_folder)
        except:
            print_and_log_msg("La commande n'a pas été reconnue, tapper '--help' pour plus d'information.\n")