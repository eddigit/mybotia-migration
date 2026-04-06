#!/usr/bin/env python3
"""
Générateur de factures/devis PDF pour Coach Digital Paris
Lit les données depuis Notion et génère un PDF via wkhtmltopdf

Usage:
  python3 tools/generate_invoice.py <notion_page_id>
  python3 tools/generate_invoice.py --test  (génère une facture test)
  python3 tools/generate_invoice.py --data '{"numero":"PRO-2026-001", ...}'
"""

import json
import os
import sys
import subprocess
import tempfile
import requests
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(WORKSPACE, "factures")

# Notion config
NOTION_TOKEN_FILE = "/home/gilles/.openclaw/credentials/notion"

def get_notion_token():
    with open(NOTION_TOKEN_FILE) as f:
        return f.read().strip()

def get_photo_base64():
    """Récupère la photo de Gilles en base64 pour l'embed dans le PDF"""
    import base64
    photo_cache = os.path.join(WORKSPACE, "assets", "gilles_photo.jpg")
    if os.path.exists(photo_cache):
        with open(photo_cache, "rb") as f:
            return base64.b64encode(f.read()).decode()
    # Télécharger si pas en cache
    os.makedirs(os.path.join(WORKSPACE, "assets"), exist_ok=True)
    r = requests.get("https://res.cloudinary.com/dniurvpzd/image/upload/v1769611030/Gilles_Coach_Digital_f9bigk.jpg")
    with open(photo_cache, "wb") as f:
        f.write(r.content)
    return base64.b64encode(r.content).decode()


def generate_html(data):
    """Génère le HTML de la facture — design moderne épuré"""
    import base64
    
    # Calculs
    total_ht = data.get("total_ht", 0)
    tva_rate = data.get("tva_rate", 20)
    tva_amount = total_ht * tva_rate / 100
    total_ttc = total_ht + tva_amount
    
    # Photo base64
    try:
        photo_b64 = get_photo_base64()
        photo_src = f"data:image/jpeg;base64,{photo_b64}"
    except:
        photo_src = ""
    
    # Lignes de facturation
    lignes_html = ""
    for i, ligne in enumerate(data.get("lignes", [])):
        bg = "#ffffff" if i % 2 == 0 else "#f9fafb"
        lignes_html += f"""
        <tr style="background: {bg};">
            <td style="padding: 14px 16px; border-bottom: 1px solid #f0f0f0; text-align: left; color: #111827; font-size: 14px; font-weight: 500;">{ligne.get('description', '')}</td>
            <td style="padding: 14px 16px; border-bottom: 1px solid #f0f0f0; text-align: center; color: #374151; font-size: 14px;">{ligne.get('quantite', 1)}</td>
            <td style="padding: 14px 16px; border-bottom: 1px solid #f0f0f0; text-align: right; color: #374151; font-size: 14px;">{ligne.get('prix_unitaire', 0):,.2f} €</td>
            <td style="padding: 14px 16px; border-bottom: 1px solid #f0f0f0; text-align: right; font-weight: 700; color: #000000; font-size: 15px;">{ligne.get('montant', 0):,.2f} €</td>
        </tr>"""
    
    # Détails sous les lignes
    details_html = ""
    if data.get("details"):
        details_html = '<div style="margin: 25px 0; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 10px; border-left: 4px solid #1a1a2e;">'
        details_html += '<p style="font-weight: 600; margin-bottom: 12px; color: #1a1a2e; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Détail des prestations</p><ul style="margin: 0; padding-left: 18px;">'
        for detail in data["details"]:
            details_html += f'<li style="margin-bottom: 8px; color: #4b5563; font-size: 13px; line-height: 1.5;">{detail}</li>'
        details_html += '</ul></div>'
    
    # Type de document
    doc_type = data.get("type", "FACTURE PROFORMA").upper()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #111; font-size: 15px; background: #fff; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px; }}
        
        /* HEADER */
        .header {{ margin-bottom: 40px; padding-bottom: 25px; border-bottom: 2px solid #f0f0f0; }}
        .header-top {{ display: table; width: 100%; margin-bottom: 0; }}
        .header-left {{ display: table-cell; vertical-align: middle; width: 60%; }}
        .header-right {{ display: table-cell; vertical-align: middle; width: 40%; text-align: right; }}
        .identity {{ display: table; }}
        .avatar {{ display: table-cell; vertical-align: middle; padding-right: 15px; }}
        .avatar img {{ width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #e5e7eb; }}
        .identity-text {{ display: table-cell; vertical-align: middle; }}
        .name {{ font-size: 26px; font-weight: 800; color: #000000; letter-spacing: -0.5px; }}
        .subtitle {{ font-size: 13px; color: #6b7280; margin-top: 4px; letter-spacing: 0.3px; font-weight: 500; }}
        .doc-badge {{ display: inline-block; background: linear-gradient(135deg, #1a1a2e 0%, #2d3748 100%); color: white; padding: 10px 24px; border-radius: 6px; font-size: 15px; font-weight: 800; letter-spacing: 1.5px; }}
        .doc-meta {{ font-size: 14px; color: #6b7280; margin-top: 8px; font-weight: 500; }}
        
        /* PARTIES */
        .parties {{ display: table; width: 100%; margin-bottom: 30px; }}
        .party {{ display: table-cell; width: 48%; vertical-align: top; }}
        .party-spacer {{ display: table-cell; width: 4%; }}
        .party-box {{ background: #f9fafb; border-radius: 10px; padding: 20px; }}
        .party-title {{ font-size: 10px; text-transform: uppercase; color: #9ca3af; letter-spacing: 1.5px; margin-bottom: 10px; font-weight: 600; }}
        .party-name {{ font-size: 18px; font-weight: 800; color: #000000; margin-bottom: 8px; }}
        .party-detail {{ font-size: 13px; color: #374151; line-height: 1.8; font-weight: 400; }}
        
        /* TABLE */
        table {{ width: 100%; border-collapse: collapse; margin: 25px 0; border-radius: 10px; overflow: hidden; }}
        th {{ background: linear-gradient(135deg, #1a1a2e 0%, #2d3748 100%); color: white; padding: 14px 16px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }}
        th:nth-child(2), th:nth-child(3) {{ text-align: center; }}
        th:last-child {{ text-align: right; }}
        
        /* TOTAUX */
        .totaux-wrapper {{ display: table; width: 100%; margin-top: 10px; }}
        .totaux-spacer {{ display: table-cell; width: 55%; }}
        .totaux-box {{ display: table-cell; width: 45%; }}
        .totaux-inner {{ background: #f9fafb; border-radius: 10px; padding: 20px; }}
        .totaux-row {{ display: table; width: 100%; padding: 8px 0; }}
        .totaux-label {{ display: table-cell; text-align: left; color: #374151; font-size: 14px; font-weight: 500; }}
        .totaux-value {{ display: table-cell; text-align: right; color: #111827; font-size: 14px; font-weight: 600; }}
        .totaux-divider {{ border-top: 2px solid #e5e7eb; margin: 8px 0; }}
        .totaux-total .totaux-label {{ font-size: 20px; font-weight: 800; color: #000000; }}
        .totaux-total .totaux-value {{ font-size: 20px; font-weight: 800; color: #000000; }}
        
        /* FOOTER */
        .bank {{ background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 20px; border-radius: 10px; margin-top: 35px; border: 1px solid #e5e7eb; }}
        .bank-title {{ font-weight: 800; margin-bottom: 10px; color: #000000; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .bank-detail {{ font-size: 14px; color: #374151; line-height: 2; font-weight: 500; }}
        .bank-highlight {{ font-weight: 800; color: #000000; font-size: 16px; }}
        .mentions {{ font-size: 10px; color: #9ca3af; margin-top: 25px; text-align: center; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <div class="header-top">
                <div class="header-left">
                    <div class="identity">
                        <div class="avatar">
                            <img src="{photo_src}" alt="Gilles Korzec">
                        </div>
                        <div class="identity-text">
                            <div class="name">Gilles Korzec</div>
                            <div class="subtitle">Coach Digital Paris — Transformation digitale & IA</div>
                        </div>
                    </div>
                </div>
                <div class="header-right">
                    <div class="doc-badge">{doc_type}</div>
                    <div class="doc-meta">N° {data.get('numero', 'XXX')}</div>
                    <div class="doc-meta">{data.get('date', datetime.now().strftime('%d/%m/%Y'))}</div>
                </div>
            </div>
        </div>

        <!-- ÉMETTEUR / CLIENT -->
        <div class="parties">
            <div class="party">
                <div class="party-box">
                    <div class="party-title">Émetteur</div>
                    <div class="party-name">Gilles Korzec</div>
                    <div class="party-detail">
                        Coach Digital Paris<br>
                        102 avenue des Champs-Élysées<br>
                        75008 Paris<br>
                        SIRET : 834 049 197 00028<br>
                        coachdigitalparis@gmail.com
                    </div>
                </div>
            </div>
            <div class="party-spacer"></div>
            <div class="party">
                <div class="party-box">
                    <div class="party-title">Client</div>
                    <div class="party-name">{data.get('client_nom', '')}</div>
                    <div class="party-detail">
                        {data.get('client_adresse', '').replace(chr(10), '<br>')}<br>
                        SIRET : {data.get('client_siret', 'N/A')}<br>
                        À l'attention de : {data.get('client_contact', '')}
                    </div>
                </div>
            </div>
        </div>

        <!-- OBJET -->
        <p style="margin-bottom: 20px; font-size: 15px;"><strong style="color: #000000;">Objet :</strong> <span style="color: #111827; font-weight: 500;">{data.get('objet', '')}</span></p>

        <!-- TABLEAU -->
        <table>
            <thead>
                <tr>
                    <th style="width: 50%; border-radius: 8px 0 0 0;">Désignation</th>
                    <th style="width: 15%;">Qté</th>
                    <th style="width: 17%;">P.U. HT</th>
                    <th style="width: 18%; border-radius: 0 8px 0 0;">Total HT</th>
                </tr>
            </thead>
            <tbody>
                {lignes_html}
            </tbody>
        </table>

        {details_html}

        <!-- TOTAUX -->
        <div class="totaux-wrapper">
            <div class="totaux-spacer"></div>
            <div class="totaux-box">
                <div class="totaux-inner">
                    <div class="totaux-row">
                        <span class="totaux-label">Total HT</span>
                        <span class="totaux-value">{total_ht:,.2f} €</span>
                    </div>
                    <div class="totaux-row">
                        <span class="totaux-label">TVA ({tva_rate}%)</span>
                        <span class="totaux-value">{tva_amount:,.2f} €</span>
                    </div>
                    <div class="totaux-divider"></div>
                    <div class="totaux-row totaux-total">
                        <span class="totaux-label">Total TTC</span>
                        <span class="totaux-value">{total_ttc:,.2f} €</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- PAIEMENT -->
        <div class="bank">
            <div class="bank-title">💳 Règlement par virement bancaire</div>
            <div class="bank-detail">
                <span class="bank-highlight">Bénéficiaire : Gilles Korzec</span><br>
                IBAN : FR76 1695 8000 0133 0858 7025 176<br>
                BIC : QNTOFRP1XXX
            </div>
        </div>

        <!-- MENTIONS LÉGALES -->
        <div class="mentions">
            Gilles Korzec — SIRET 834 049 197 00028 — 102 avenue des Champs-Élysées, 75008 Paris<br>
            {data.get('mention_tva', 'TVA applicable selon le régime en vigueur')}
        </div>
    </div>
</body>
</html>"""
    return html


def generate_pdf(data, output_path=None):
    """Génère le PDF à partir des données"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not output_path:
        filename = f"{data.get('numero', 'facture').replace('/', '-')}.pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)
    
    html = generate_html(data)
    
    # Écrire le HTML temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html)
        html_path = f.name
    
    try:
        # Générer le PDF
        result = subprocess.run([
            'wkhtmltopdf',
            '--encoding', 'UTF-8',
            '--page-size', 'A4',
            '--margin-top', '10mm',
            '--margin-bottom', '10mm',
            '--margin-left', '10mm',
            '--margin-right', '10mm',
            '--enable-local-file-access',
            html_path,
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0 and not os.path.exists(output_path):
            print(f"Erreur wkhtmltopdf: {result.stderr}")
            return None
        
        print(f"✅ PDF généré : {output_path}")
        
        # Auto-upload Cloudinary pour accès direct
        try:
            upload_result = subprocess.run(
                ["python3", "tools/upload_file.py", output_path],
                capture_output=True, text=True,
                cwd=os.path.expanduser("~/.openclaw/workspace")
            )
            if upload_result.returncode == 0:
                for line in upload_result.stdout.strip().split("\n"):
                    if "URL:" in line:
                        url = line.split("URL:")[1].strip()
                        print(f"🌐 Téléchargement : {url}")
                        break
        except Exception:
            pass
        
        return output_path
    
    finally:
        os.unlink(html_path)


def send_email_with_pdf(to, subject, body, pdf_path, sender="coachdigitalparis@gmail.com"):
    """Envoie un email avec le PDF en pièce jointe"""
    import base64
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    token_name = sender.replace("@gmail.com", "")
    token_file = os.path.join(SCRIPT_DIR, f'gmail-token-{token_name}.json')
    
    with open(token_file) as f:
        token = json.load(f)
    with open(os.path.join(SCRIPT_DIR, 'gmail-credentials.json')) as f:
        creds = json.load(f)['installed']
    
    # Refresh token si nécessaire
    test = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/profile',
        headers={'Authorization': f'Bearer {token["access_token"]}'}
    )
    if test.status_code == 401:
        r = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'refresh_token': token['refresh_token'],
            'grant_type': 'refresh_token'
        })
        token['access_token'] = r.json()['access_token']
        with open(token_file, 'w') as f:
            json.dump(token, f, indent=2)
    
    # Construire le mail
    msg = MIMEMultipart()
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Pièce jointe PDF
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    
    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(pdf_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
    msg.attach(attachment)
    
    # Envoyer
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    r = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={'Authorization': f'Bearer {token["access_token"]}', 'Content-Type': 'application/json'},
        json={'raw': raw}
    )
    
    if r.status_code == 200:
        print(f"✅ Email envoyé à {to} avec PDF joint (ID: {r.json()['id']})")
        return r.json()['id']
    else:
        print(f"❌ Erreur envoi: {r.status_code} - {r.text}")
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Facture test
        test_data = {
            "type": "FACTURE PROFORMA",
            "numero": "PRO-2026-001",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "client_nom": "SYSTEMIC",
            "client_siret": "397 982 463 00036",
            "client_adresse": "24 rue de Caumartin\n75009 Paris",
            "client_contact": "M. Uber Taieb",
            "objet": "Étude complète et développement projet PAYPERS",
            "lignes": [
                {
                    "description": "Étude complète et développement projet PAYPERS",
                    "quantite": 1,
                    "prix_unitaire": 1000.00,
                    "montant": 1000.00
                }
            ],
            "details": [
                "Veille stratégique complète : analyse concurrentielle, benchmark des API disponibles, vecteurs de décision",
                "Prototype fonctionnel de l'application (~10h de développement)",
                "Infrastructure serveur : VPS dédié pour héberger, tester et faire évoluer le prototype",
                "Accès LLM professionnels : tokens sur 3 modèles d'IA pour un mois complet",
                "Mise en place d'une collaboratrice IA dédiée et exclusive (valeur 990€/mois)"
            ],
            "total_ht": 1000.00,
            "tva_rate": 20,
            "mention_tva": "TVA applicable selon le régime en vigueur"
        }
        generate_pdf(test_data)
    
    elif len(sys.argv) > 1 and sys.argv[1] == "--data":
        data = json.loads(sys.argv[2])
        generate_pdf(data)
    
    else:
        print("Usage:")
        print("  python3 generate_invoice.py --test")
        print("  python3 generate_invoice.py --data '{...}'")
