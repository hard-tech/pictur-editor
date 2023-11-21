from PIL import Image

# Demmander à l'utilisateur le nom de l'image à modifier
image_nom = input('Quelle est le nom de vôtre image ? : ')

try:
    # Charger l'image
    image = Image.open(f'./original_picture/{image_nom}')

    # Convertire l'image en Noir & Blanc
    image_noir_et_blanc = image.convert('L')
    image_noir_et_blanc.show()

    # Sauvegarder l'image dans ./modify_picture
    image_noir_et_blanc.save(f'./modify_picture/{image_nom}')
    
    # Retourner à l'utilisateur l'états de l'action (si err la retourné)
    print("GGWP")
except:
    print("nous n'avons pas pu ouverire le fichier (nom d'image incorrect).")