# Design Skill — Boîte à outils graphique VPS

## Description
Compétences graphiques pour créer, optimiser et manipuler des visuels depuis le VPS. Tous les outils sont offline (aucun accès réseau à l'exécution).

## Outils disponibles

### 🖼️ ImageMagick (`convert` / `magick`)
Manipulation d'images : resize, crop, texte, filtres, montage, conversion de formats.

```bash
# Redimensionner
convert input.png -resize 800x600 output.png

# Ajouter du texte sur une image
convert input.png -gravity south -pointsize 36 -fill white -annotate +0+20 "Mon texte" output.png

# Créer une image depuis zéro (fond + texte)
convert -size 1200x630 xc:"#1a1a2e" \
  -gravity center -pointsize 48 -fill white \
  -annotate +0+0 "Mon Titre" output.png

# Montage (grille d'images)
montage img1.png img2.png img3.png -tile 3x1 -geometry +10+10 montage.png

# Convertir format
convert input.png output.webp
convert input.svg output.png

# Arrondir les coins
convert input.png \( +clone -alpha extract -draw "roundrectangle 0,0,%w,%h,20,20" \) -alpha off -compose CopyOpacity -composite output.png
```

### ⚡ Sharp CLI (`sharp`)
Traitement d'images haute performance. Plus rapide qu'ImageMagick pour les opérations courantes.

```bash
# Redimensionner
sharp -i input.jpg -o output.jpg resize 800 600

# Convertir en WebP optimisé
sharp -i input.png -o output.webp --format webp

# Recadrer
sharp -i input.jpg -o output.jpg resize 400 400 --fit cover
```

### 🧹 SVGO (`svgo`)
Optimiser et nettoyer les fichiers SVG (réduit le poids de 30-70%).

```bash
# Optimiser un SVG
svgo input.svg -o output.svg

# Optimiser un dossier entier
svgo -f ./icons/ -o ./icons-optimized/

# Voir la compression obtenue
svgo input.svg --pretty
```

### 📐 SVG → PNG (`rsvg-convert`)
Convertir des SVG en PNG/PDF avec contrôle précis de la résolution.

```bash
# SVG → PNG (haute résolution)
rsvg-convert -w 1200 -h 630 input.svg -o output.png

# SVG → PDF
rsvg-convert -f pdf input.svg -o output.pdf

# Double résolution (retina)
rsvg-convert -w 2400 -h 1260 input.svg -o output@2x.png
```

### 🗜️ Optimisation PNG

```bash
# Optimisation lossless (sans perte)
optipng -o5 image.png

# Compression lossy (réduction ~80%, qualité visuelle préservée)
pngquant --quality=65-80 --speed 1 image.png -o image-optimized.png
```

### ✏️ Potrace — Bitmap → Vectoriel

```bash
# Image → SVG vectoriel
potrace input.bmp -s -o output.svg

# PNG → BMP → SVG (potrace lit le BMP)
convert input.png input.bmp && potrace input.bmp -s -o output.svg

# Ajuster le seuil (0.0-1.0, défaut 0.5)
potrace input.bmp -s -k 0.4 -o output.svg
```

### 🎬 ffmpeg — GIF & Vidéo

```bash
# Créer un GIF depuis des images
ffmpeg -framerate 10 -i frame_%03d.png -vf "scale=600:-1" output.gif

# Extraire une frame d'une vidéo
ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 thumbnail.png

# Vidéo → GIF optimisé
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1:flags=lanczos" -c:v gif output.gif
```

## 🎨 Icônes — Phosphor Icons
Voir `references/phosphor-icons.md` pour le standard icônes MyBotia.

## 🏗️ Créer un visuel en SVG (méthode recommandée)

Pour les visuels complexes (bannières, cards, social), la meilleure approche :
1. Créer un fichier SVG (texte, formes, typo)
2. Convertir en PNG via `rsvg-convert`
3. Optimiser via `optipng` ou `pngquant`

```bash
# Exemple : bannière 1200x630
cat > banner.svg << 'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#0f0f23"/>
  <text x="600" y="280" text-anchor="middle" font-family="Arial, sans-serif" font-size="56" font-weight="bold" fill="#ffffff">Mon Titre</text>
  <text x="600" y="350" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#888888">Sous-titre descriptif</text>
</svg>
SVG

rsvg-convert -w 1200 -h 630 banner.svg -o banner.png
optipng -o5 banner.png
```

## 📏 Tailles standards

| Usage | Dimensions |
|-------|-----------|
| OG Image / Social | 1200 × 630 |
| Story / Reel | 1080 × 1920 |
| Carré Instagram | 1080 × 1080 |
| Favicon | 32×32, 180×180 |
| Avatar | 400 × 400 |
| Bannière email | 600 × 200 |
| WhatsApp profile | 640 × 640 |

## ⚠️ Notes
- Tous les outils fonctionnent **offline** (aucun accès réseau)
- Output dans `~/.openclaw/workspace/media/` pour envoi WhatsApp/Telegram
- PATH npm global : `export PATH="$HOME/.npm-global/bin:$PATH"` (nécessaire pour svgo, sharp)
- Pour les polices Google Fonts : télécharger les .ttf et les placer dans `/usr/local/share/fonts/`
