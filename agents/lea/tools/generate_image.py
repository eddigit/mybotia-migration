#!/usr/bin/env python3
"""Générer une image via Replicate API.

Usage:
  python3 tools/generate_image.py "un chat sur la lune"
  python3 tools/generate_image.py "logo minimaliste" --model flux-pro
  python3 tools/generate_image.py "bannière web" --size 1200x630
  python3 tools/generate_image.py "portrait pro" --model sdxl --output media/portrait.png

Modèles disponibles:
  flux-schnell  — Rapide, ~0.003€/image (défaut)
  flux-pro      — Haute qualité, ~0.05€/image
  sdxl          — Stable Diffusion XL, ~0.02€/image
"""
import sys, os, json, time, argparse, subprocess, urllib.request, urllib.error, hashlib

# Récupérer le token
def get_token():
    result = subprocess.run(
        ["python3", "tools/get_credential.py", "replicate", "api_token"],
        capture_output=True, text=True,
        cwd=os.path.expanduser("~/.openclaw/workspace")
    )
    token = result.stdout.strip()
    if not token or "non trouvé" in token:
        print("❌ Token Replicate non trouvé dans les credentials")
        sys.exit(1)
    return token

def get_cloudinary_creds():
    """Récupérer les credentials Cloudinary depuis PostgreSQL."""
    try:
        cwd = os.path.expanduser("~/.openclaw/workspace")
        cloud_name = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "cloud_name"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        api_key = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "api_key"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        api_secret = subprocess.run(["python3", "tools/get_credential.py", "cloudinary", "api_secret"], capture_output=True, text=True, cwd=cwd).stdout.strip()
        if cloud_name and api_key and api_secret and "non trouvé" not in cloud_name:
            return cloud_name, api_key, api_secret
    except Exception:
        pass
    return None, None, None

def upload_cloudinary(file_path):
    """Upload un fichier sur Cloudinary et retourne l'URL."""
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

MODELS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "flux-pro": "black-forest-labs/flux-1.1-pro",
    "sdxl": "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
}

def api_request(url, token, data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Erreur API ({e.code}): {error_body}")
        sys.exit(1)

def generate(prompt, model_key="flux-schnell", width=1024, height=1024, output_path=None):
    token = get_token()
    model_id = MODELS.get(model_key, model_key)
    
    print(f"🎨 Génération avec {model_key}...")
    print(f"   Prompt: {prompt}")
    print(f"   Taille: {width}x{height}")
    
    # Construire l'input selon le modèle
    model_input = {"prompt": prompt}
    
    if "flux" in model_key:
        # Flux accepte uniquement certains aspect ratios
        FLUX_RATIOS = ["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21"]
        ratio = f"{width}:{height}"
        # Simplifier le ratio
        from math import gcd
        g = gcd(width, height)
        simplified = f"{width//g}:{height//g}"
        if simplified in FLUX_RATIOS:
            model_input["aspect_ratio"] = simplified
        elif ratio in FLUX_RATIOS:
            model_input["aspect_ratio"] = ratio
        else:
            # Trouver le ratio le plus proche
            target = width / height
            best = min(FLUX_RATIOS, key=lambda r: abs(int(r.split(":")[0])/int(r.split(":")[1]) - target))
            model_input["aspect_ratio"] = best
        if model_key == "flux-schnell":
            model_input["go_fast"] = True
    else:
        model_input["width"] = width
        model_input["height"] = height
    
    # Lancer la prédiction
    if ":" in model_id:
        # Version spécifique (sdxl)
        version = model_id.split(":")[1]
        data = {"version": version, "input": model_input}
        result = api_request("https://api.replicate.com/v1/predictions", token, data)
    else:
        # Modèle officiel (flux)
        data = {"input": model_input}
        result = api_request(f"https://api.replicate.com/v1/models/{model_id}/predictions", token, data)
    
    pred_url = result.get("urls", {}).get("get", result.get("url"))
    if not pred_url:
        print(f"❌ Pas d'URL de suivi: {json.dumps(result, indent=2)}")
        sys.exit(1)
    
    # Attendre le résultat
    print("   ⏳ En cours...", end="", flush=True)
    for i in range(120):  # max 2 min
        time.sleep(1)
        status = api_request(pred_url, token)
        state = status.get("status")
        if state == "succeeded":
            print(" ✅")
            break
        elif state == "failed":
            print(f"\n❌ Échec: {status.get('error', 'erreur inconnue')}")
            sys.exit(1)
        elif state == "canceled":
            print("\n❌ Annulé")
            sys.exit(1)
        if i % 5 == 0:
            print(".", end="", flush=True)
    else:
        print("\n❌ Timeout (2 min)")
        sys.exit(1)
    
    # Récupérer l'image
    output = status.get("output")
    if isinstance(output, list):
        image_url = output[0]
    elif isinstance(output, str):
        image_url = output
    else:
        print(f"❌ Format de sortie inattendu: {output}")
        sys.exit(1)
    
    # Télécharger
    if not output_path:
        os.makedirs(os.path.expanduser("~/.openclaw/workspace/media"), exist_ok=True)
        timestamp = int(time.time())
        output_path = os.path.expanduser(f"~/.openclaw/workspace/media/generated_{timestamp}.png")
    
    # Expand le path
    output_path = os.path.expanduser(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"   📥 Téléchargement...")
    req = urllib.request.Request(image_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(output_path, "wb") as f:
            f.write(resp.read())
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"   ✅ Sauvegardé: {output_path} ({size_kb:.0f} KB)")
    
    # Coût estimé
    costs = {"flux-schnell": 0.003, "flux-pro": 0.05, "sdxl": 0.02}
    cost = costs.get(model_key, 0.01)
    print(f"   💰 Coût estimé: ~{cost}€")
    
    # Upload Cloudinary
    cloud_url = upload_cloudinary(output_path)
    if cloud_url:
        print(f"   🌐 URL: {cloud_url}")
        return cloud_url
    
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer une image via Replicate")
    parser.add_argument("prompt", help="Description de l'image à générer")
    parser.add_argument("--model", "-m", default="flux-schnell", choices=list(MODELS.keys()), help="Modèle (défaut: flux-schnell)")
    parser.add_argument("--size", "-s", default="1024x1024", help="Taille WxH (défaut: 1024x1024)")
    parser.add_argument("--output", "-o", help="Chemin de sortie")
    
    args = parser.parse_args()
    w, h = args.size.split("x")
    generate(args.prompt, args.model, int(w), int(h), args.output)
