# Outil de Transformation d'Images

Cet outil Python permet de réaliser différentes transformations sur des images. Il utilise les bibliothèques PIL (Pillow) et OpenCV pour effectuer des opérations telles que la conversion en noir et blanc, le flou, la dilatation, la rotation, le redimensionnement, et l'ajout de texte.

## Prérequis

- Python 3.x
- Bibliothèques requises : Pillow (PIL) et OpenCV (`pip install pillow opencv-python`)

## Structure des Dossiers

- `original_picture/` : Dossier contenant les images originales.
- `modify_picture/` : Dossier où les images transformées seront sauvegardées.

## Comment Utiliser

1. Placez les images que vous souhaitez transformer dans le dossier `original_picture/`.
2. Exécutez le script en ligne de commande et suivez les instructions.

## Commandes Disponibles

- `convert_black_and_white`: Convertit une image en noir et blanc.
- `convert_blur`: Applique un flou à une image.
- `dilate_image`: Dilate une image.
- `convert_rotate`: Fait pivoter une image.
- `convert_resize`: Redimensionne une image.
- `add_text`: Ajoute du texte à une image.

## Exemple d'Utilisation

```bash
python image_transform.py convert_black_and_white
