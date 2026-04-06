#!/usr/bin/env python3
"""Rendre un fichier accessible par URL pour téléchargement direct.

Usage:
  python3 tools/upload_file.py chemin/fichier.pdf
  python3 tools/upload_file.py chemin/image.png
  python3 tools/upload_file.py factures/FA-2026-030.pdf

- Images (png, jpg, webp...) → upload Cloudinary (affichage inline dans le chat)
- Autres fichiers (PDF, Excel, ZIP...) → copie dans media/docs/ → URL files.mybotia.com

Retourne l'URL publique.
"""
import sys, os, json, time, hashlib, argparse, subprocess, urllib.request, urllib.error, shutil

MEDIA_DIR = os.path.expanduser("~/.openclaw/workspace/media")
DOCS_DIR = os.path.join(MEDIA_DIR, "docs")
FILES_BASE_URL = "https://files.mybotia.com"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"}

def get_cloudinary_creds():
    cwd = os.path.expanduser("~/.openclaw/workspace")
    try:
        cloud_name = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "cloud_name"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        api_key = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "api_key"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        api_secret = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "api_secret"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        if cloud_name and api_key and api_secret and "non trouvé" not in cloud_name:
            return cloud_name, api_key, api_secret
    except Exception:
        pass
    return None, None, None

def upload_cloudinary(file_path):
    """Upload une image sur Cloudinary pour affichage inline."""
    cloud_name, api_key, api_secret = get_cloudinary_creds()
    if not cloud_name:
        return None
    
    try:
        timestamp = str(int(time.time()))
        params = f"folder=mybotia&timestamp={timestamp}{api_secret}"
        signature = hashlib.sha1(params.encode()).hexdigest()
        
        boundary = "----PythonUploadBoundary"
        body = b""
        fields = {"api_key": api_key, "timestamp": timestamp, "signature": signature, "folder": "mybotia"}
        for k, v in fields.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        
        with open(file_path, "rb") as f:
            file_data = f.read()
        fname = os.path.basename(file_path)
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{fname}\"\r\nContent-Type: image/png\r\n\r\n".encode()
        body += file_data
        body += f"\r\n--{boundary}--\r\n".encode()
        
        req = urllib.request.Request(
            f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("secure_url")
    except Exception as e:
        print(f"   ⚠️ Upload Cloudinary échoué: {e}")
        return None

def serve_local(file_path):
    """Copier le fichier dans media/docs/ et retourner l'URL files.mybotia.com."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    
    fname = os.path.basename(file_path)
    # Ajouter timestamp pour éviter les collisions
    name, ext = os.path.splitext(fname)
    dest_name = f"{name}_{int(time.time())}{ext}"
    dest_path = os.path.join(DOCS_DIR, dest_name)
    
    shutil.copy2(file_path, dest_path)
    url = f"{FILES_BASE_URL}/docs/{dest_name}"
    return url

def upload(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Fichier non trouvé: {file_path}")
        sys.exit(1)
    
    ext = os.path.splitext(file_path)[1].lower()
    is_image = ext in IMAGE_EXTENSIONS
    file_size = os.path.getsize(file_path) / 1024
    fname = os.path.basename(file_path)
    
    print(f"📤 Upload: {fname} ({file_size:.0f} KB)")
    
    if is_image:
        # Images → Cloudinary (affichage inline)
        url = upload_cloudinary(file_path)
        if not url:
            # Fallback sur notre serveur
            url = serve_local(file_path)
    else:
        # PDF, docs, etc → notre serveur files.mybotia.com
        url = serve_local(file_path)
    
    print(f"✅ URL: {url}")
    return url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rendre un fichier accessible par URL")
    parser.add_argument("file", help="Chemin du fichier")
    args = parser.parse_args()
    upload(args.file)
