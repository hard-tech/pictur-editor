# Outil de Transformation d'Images

Cet outil Python permet de réaliser différentes transformations sur des images. Il utilise les bibliothèques PIL (Pillow) et OpenCV pour effectuer des opérations telles que la conversion en noir et blanc, le flou, la dilatation, la rotation, le redimensionnement, et l'ajout de texte.

## Prérequis

- Python 3.x
- Bibliothèques requises : Pillow (PIL) et OpenCV (`pip install -r requirements.txt`)

## Structure des Dossiers

- `original_picture/` : Dossier contenant les images originales.
- `modify_picture/` : Dossier où les images transformées seront sauvegardées.

## Comment Utiliser

- Exécutez le script en ligne de commande et suivez les instructions.

## Filtres Disponibles

- `convert_black_and_white`: Convertit l'image en noir et blanc.
- `convert_blur`: Applique un effet de flou à l'image.
- `dilate_image`: Effectue une dilatation de l'image.
- `convert_rotate`: Rotation de l'image.
  - Paramètre : `angl` (angle de rotation).
- `convert_resize`: Redimensionne l'image.
  - Paramètre : `Nombre entier` (détermine l'échelle de modification).
- `add_text`: Ajoute du texte à l'image.
  - Paramètre : `TEXTE À AJOUTER`.

## Exemple d'Utilisation

```bash
python3 main.py --filters "convert_black_and_white&add_text:LL" --i original_picture --o modify_picture