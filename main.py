from PIL import Image
from PIL import Image, ImageFilter
import cv2
import numpy as np
import os
import sys

arguments = sys.argv

def image_transformation(filters,input_folder:str,output_picture:str):

    def cat_folder_element(folder):
        folder_elements = os.listdir(folder)
        return folder_elements

    original_picture = input_folder
    modify_picture = output_picture
    image_names = cat_folder_element(input_folder)
    operation = filters.split('&')

    def ls_original_pic():
        fichiers = os.listdir(original_picture)
        print(f'\nListe des fichiers dans {original_picture} :')
        for fichier in fichiers:
            print(fichier)

    # def ls_modify_pic():
    #     fichiers = os.listdir(modify_picture)
    #     print(f'\nListe des fichiers dans {modify_picture} : ')
    #     for fichier in fichiers:
    #         print(fichier)

    def save_picture(object, path, name):
        object.save(f'{path}{name}')

    def load_picture(picture_name):
        image = Image.open(f'{original_picture}{picture_name}')
        return image

    
    # Pour chaque image du dossier faire ...
    for image_name in image_names:        
        i = 0

        # Pour chaque paramètre appliquer à l'image ...
        for param_filter in operation:

            # Si le filtre appliquer est suppérieur à 1 prendre l'image dans modify_picture
            if i >= 1:
                original_picture = modify_picture
            else:
                original_picture = input_folder
            
            try:
                # -- Story 1  -- #
                if param_filter == "convert_black_and_white":
                    
                    # Charge l'image
                    image = load_picture(image_name)

                    # Vérifier si l'image s'ouvre
                    if image is not None:
                        # Convertir l'image en noir et blanc
                        image_noir_et_blanc = image.convert('L')

                        # Sauvegarde de l'image transformé
                        save_picture(image_noir_et_blanc, modify_picture, image_name)
                        
                        # Retour l'état final à l'utilisateur
                        print("\nL'image a bien été transformée en noir et blanc.\n")
                    else:
                        # Retour erreur
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")

                # -- Story 2  -- #
                elif param_filter == "convert_blur":

                    # Charge l'image
                    image = load_picture(image_name)
                    
                    # Vérifier si l'image s'ouvre
                    if image is not None:
                        # Appliquer un flou à l'image
                        image_blur = image.filter(ImageFilter.BLUR)
                        
                        # Sauvegarde de l'image transformé
                        save_picture(image_blur, modify_picture, image_name)

                        # Retour l'état final à l'utilisateur
                        print("\nL'image a bien été floutée.\n")
                    else:
                        # Retour erreur
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")

                # -- Story 3  -- #
                elif param_filter == "dilate_image":
                    
                    # Charge l'image
                    image = load_picture(image_name)
                    
                    # Vérifier si l'image s'ouvre
                    if image is not None:
                        # Charge l'image
                        image = cv2.imread(f'{original_picture}{image_name}')
                        
                        # Dilater l'image
                        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        kernel = np.ones((5, 5), np.uint8)
                        image_dilated = cv2.dilate(image_gray, kernel, iterations=1)

                        # Sauvegarde de l'image transformé
                        cv2.imwrite(f'{modify_picture}{image_name}', image_dilated)

                        # Retour l'état final à l'utilisateur
                        print("\nL'image a bien été dilater.\n")
                    else:
                        # Retour erreur
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")

                # -- Story 4  -- #
                elif param_filter == f"convert_rotate:{param_filter.split(':')[1]}":
                    
                    # Faire pivoter l'image
                    value_rotate = param_filter.split(':')[1]
                    # Charge l'image
                    image = load_picture(image_name)
                    # Vérifier si l'image s'ouvre
                    if image is not None:
                        # Faire pivoter l'image
                        image_rotate = image.rotate(int(value_rotate))

                        # Sauvegarde de l'image transformé
                        save_picture(image_rotate,modify_picture,image_name)
                        
                        # Retour l'état final à l'utilisateur
                        print(f"\nL'image a bien été tournée de {value_rotate}°.")
                    else:
                        # Retour erreur
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")
                
                # -- Story 5  -- #
                elif param_filter == f"convert_resize:{param_filter.split(':')[1]}":
                    
                    # Récupérer la nouvelle taille de l'image
                    width_and_height = param_filter.split(':')[1]
                    value_height = int(width_and_height.split(';')[0])
                    value_width = int(width_and_height.split(';')[1])

                    # Chargement l'image
                    image = cv2.imread(f'{original_picture}{image_name}')
                    
                    # Vérifier si l'image s'ouvre
                    if image is not None:
                        # Changer la taille de l'image
                        image_resize = cv2.resize(image, (value_width, value_height), interpolation=cv2.INTER_AREA)
                        
                        # Sauvegarde de l'image transformé
                        cv2.imwrite(f'{modify_picture}{image_name}', image_resize)

                        # Retour l'état final à l'utilisateur
                        print("\nL'image a bien été redimensionner.")
                    else:
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")
                
                # -- Story 6  -- #
                elif param_filter == f"add_text:{param_filter.split(':')[1]}":
                    
                    # Demmander ce que l'utilisateur écrire sur l'image
                    text_param = param_filter.split(':')[1]
                    text_to_add = text_param

                    # Charge l'image
                    image = cv2.imread(f'{original_picture}{image_name}')
                    
                    # Vérifier si l'image s'ouvre
                    if image is not None:
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
                        print("\nLe texte à bien été ajouter à l'image.\n")
                    else:
                        # Retour erreur
                        print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.\n")

                else:
                    # Retour erreur commande
                    print("\nOpération non reconnue.")

            except:
                print(f"\nUne erreur c'est produite lors de la transformation d'un fichier.")
                ls_original_pic()
            i+=1


# init valeurs
x = 0
input_folder=''
filters=''
output_folder = ''
help = False

# Récupère l'index des arguments de la commande
for cli_name_pic in arguments:
    if cli_name_pic == '--filters':
        filters = arguments[x+1]

    if cli_name_pic == '--i':
        input_folder = f"./{arguments[x+1]}/"

    if cli_name_pic == '--o':
        output_folder = f"./{arguments[x+1]}/"
        
    if cli_name_pic == '--help':
        help = True
    x+=1

if help:
    help_msg = "\nLes fonction sont : \n\n --filters \n   'convert_black_and_white'\n   'convert_blur'\n   'dilate_image'\n   'convert_rotate'\n   'convert_resize'\n   'add_text'\n\n Selection multible avec [&] \n (exemple : 'convert_blur&convert_black_and_white')\n\n"\
                " --i 'original_picture' (Nom du dossier contenant les images à modifier)\n\n"\
                " --o 'modify_picture' (Nom du dossier qui contiendra les images modifier)\n"\
                "\n"
    print(help_msg)
else:
    image_transformation(filters, input_folder, output_folder)