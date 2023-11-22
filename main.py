from PIL import Image
from PIL import Image, ImageFilter
import cv2
import numpy as np
import os

original_picture = './original_picture/'
modify_picture = './modify_picture/'

def ls_original_pic():
    fichiers = os.listdir(original_picture)
    print(f'\nListe des fichiers dans {original_picture} :')
    for fichier in fichiers:
        print(fichier)

def ls_modify_pic():
    fichiers = os.listdir(modify_picture)
    print(f'\nListe des fichiers dans {modify_picture} : ')
    for fichier in fichiers:
        print(fichier)

def save_picture(object, path, name):
    object.save(f'{path}{name}')

def load_picture(picture_name):
    image = Image.open(f'{original_picture}{picture_name}')
    return image

def image_transformation(operation):
    image_name = input('\nQuel est le nom de votre image ? : ')
    try:
        # -- Story 1  -- #
        if operation == "convert_black_and_white":
            # Charge l'image
            image = load_picture(image_name)

            # Vérifier si l'image transformée existe déjà
            if image is not None:
                # Convertir l'image en noir et blanc
                image_noir_et_blanc = image.convert('L')

                # Sauvegarde de l'image transformé
                save_picture(image_noir_et_blanc, modify_picture, image_name)
                
                # Retour l'état final à l'utilisateur
                print("\nL'image a bien été transformée. \n")
                ls_modify_pic()
            else:
                # Retour erreur
                print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.")
                ls_original_pic()

        # -- Story 2  -- #
        elif operation == "convert_blur":
            # Charge l'image
            image = load_picture(image_name)
            
            # Vérifier si l'image transformée existe déjà
            if image is not None:
                # Appliquer un flou à l'image
                image_blur = image.filter(ImageFilter.BLUR)
                
                # Sauvegarde de l'image transformé
                save_picture(image_blur, modify_picture, image_name)

                # Retour l'état final à l'utilisateur
                print("\nL'image a bien été transformée.")
                ls_modify_pic()
            else:
                # Retour erreur
                print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.")
                ls_original_pic()

        # -- Story 3  -- #
        elif operation == "dilate_image":
            # Charge l'image
            image = load_picture(image_name)
            
            # Vérifier si l'image transformée existe déjà
            if image is not None:
                image = cv2.imread(f'{original_picture}/{image_name}')
                # Dilater l'image
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                kernel = np.ones((5, 5), np.uint8)
                image_dilated = cv2.dilate(image_gray, kernel, iterations=1)

                # Sauvegarde de l'image transformé
                cv2.imwrite(f'{modify_picture}/{image_name}', image_dilated)

                # Retour l'état final à l'utilisateur
                print("\nL'image a bien été transformée.")
                ls_modify_pic()
            else:
                # Retour erreur
                print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.")
                ls_original_pic()

        # -- Story 4  -- #
        elif operation == "convert_rotate":
            # Faire pivoter l'image
            value_rotate = input('\nDéterminez de combien vous voulez faire pivoter l\'image : ')
            # Charge l'image
            image = load_picture(image_name)
            # Vérifier si l'image transformée existe déjà
            if image is not None:
                # Faire pivoter l'image
                image_rotate = image.rotate(int(value_rotate))

                # Sauvegarde de l'image transformé
                save_picture(image_rotate,modify_picture,image_name)
                
                # Retour l'état final à l'utilisateur
                print("\nL'image a bien été transformée.")
                ls_modify_pic()
            else:
                # Retour erreur
                print("\nImpossible de charger l'image. Veuillez vérifier le nom du fichier.")
                ls_original_pic()

        # -- Story X  -- #
        # elif operation == "...":
        
        else:
            # Retour erreur commande
            print("\nOpération non reconnue.")

    except Exception as e:
        print(f"\nErr ({e}) --Veuillez vérifier le nom du fichier.")
        ls_original_pic()

# -- Appel des fonctions pour chaque opération sur l'image -- #

# image_transformation("convert_black_and_white")
# image_transformation("convert_blur")
# image_transformation("dilate_image")
# image_transformation("convert_rotate")