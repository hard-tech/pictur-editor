from PIL import Image, ImageFilter
import os

original_picture = './original_picture/'
modify_picture = './modify_picture/'

def ls_original_pic():
    fichiers = os.listdir(original_picture)

    print(f'\nListe des fichier dans {original_picture} :')
    for fichier in fichiers:
        print(fichier)

def ls_modify_pic():
    fichiers = os.listdir(modify_picture)

    print(f'\nListe des fichier dans {modify_picture} : ')
    for fichier in fichiers:
        print(fichier)

def save_picture(Oject, Path, Name):
    Oject.save(f'{Path}{Name}')

# Storie 1 :
def convert_black_and_white():
    # Demmander à l'utilisateur le nom de l'image à modifier
    image_nom = input('\nQuelle est le nom de vôtre image ? : ')

    try:
        # Charger l'image
        image = Image.open(f'{original_picture}{image_nom}')
        if(os.path.exists(f'{modify_picture}{image_nom}')):
            print("\nL'image existe déjà ! \n")
        else:
            # Convertire l'image en Noir & Blanc
            image_noir_et_blanc = image.convert('L')
            # image_noir_et_blanc.show()

            # Sauvegarder l'image dans ./modify_picture
            save_picture(image_noir_et_blanc, modify_picture, image_nom)
            
            # Retourner à l'utilisateur l'états de l'action (si err la retourné)
            print("\nL'image a bien été transformé. \n")
            ls_modify_pic()
    except:
        print("\nNous n'avons pas pu ouverire le fichier (le nom de l'image est incorrect).")
        ls_original_pic()

# convert_black_and_white()

def convert_Blur():
    # Demmander à l'utilisateur le nom de l'image à modifier
    image_nom = input('\n Quelle est le nom de vôtre image ? : ')

    try:
        # Charger l'image
        image = Image.open(f'./original_picture/{image_nom}')

        # Convertire l'image en Noir & Blanc
        image_blur = image.filter(ImageFilter.BLUR)
        # image_blur.show()

        # Sauvegarder l'image dans ./modify_picture
        image_blur.save(f'./modify_picture/{image_nom}')
        
        # Retourner à l'utilisateur l'états de l'action (si err la retourné)
        print("\nL'image a bien été transformé.")
        ls_modify_pic()
        
    except:
        print("nous n'avons pas pu ouverire le fichier (nom d'image incorrect).")
        ls_original_pic()
        print('\n')

# convert_black_and_white()

def convert_Blur():
    # Demmander à l'utilisateur le nom de l'image à modifier
    image_nom = input('\n Quelle est le nom de vôtre image ? : ')

    try:
        # Charger l'image
        image = Image.open(f'./original_picture/{image_nom}')

        # Convertire l'image en Noir & Blanc
        image_blur = image.filter(ImageFilter.BLUR)
        # image_blur.show()

        # Sauvegarder l'image dans ./modify_picture
        image_blur.save(f'./modify_picture/{image_nom}')
        
        # Retourner à l'utilisateur l'états de l'action (si err la retourné)
        print("\nL'image a bien été transformé.")
        ls_modify_pic()
        
    except:
        print("nous n'avons pas pu ouverire le fichier (nom d'image incorrect).")
        ls_original_pic()
        print('\n')

# convert_Blur()