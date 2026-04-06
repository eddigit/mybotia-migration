#!/usr/bin/env python3
"""
Devis Byron Cannes — PDF via ReportLab
"""

import os
import requests
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, HRFlowable, KeepTogether
)
from reportlab.lib.utils import ImageReader
from io import BytesIO

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE, "factures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Couleurs
DARK = colors.HexColor("#1a1a2e")
DARK2 = colors.HexColor("#2d3748")
GOLD = colors.HexColor("#B8860B")
GRAY_TEXT = colors.HexColor("#374151")
GRAY_LIGHT = colors.HexColor("#6b7280")
GRAY_BG = colors.HexColor("#f9fafb")
GRAY_BORDER = colors.HexColor("#e5e7eb")
BLACK = colors.HexColor("#000000")
WHITE = colors.HexColor("#ffffff")

def get_photo():
    """Récupère la photo de Gilles"""
    photo_cache = os.path.join(WORKSPACE, "assets", "gilles_photo.jpg")
    if os.path.exists(photo_cache):
        return photo_cache
    os.makedirs(os.path.join(WORKSPACE, "assets"), exist_ok=True)
    r = requests.get("https://res.cloudinary.com/dniurvpzd/image/upload/v1769611030/Gilles_Coach_Digital_f9bigk.jpg")
    with open(photo_cache, "wb") as f:
        f.write(r.content)
    return photo_cache


def build_pdf():
    output_path = os.path.join(OUTPUT_DIR, "DEV-2026-001-Byron.pdf")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    width = A4[0] - 40*mm  # usable width
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    s_title = ParagraphStyle('Title2', parent=styles['Normal'],
        fontSize=22, fontName='Helvetica-Bold', textColor=BLACK, leading=26)
    s_subtitle = ParagraphStyle('Subtitle2', parent=styles['Normal'],
        fontSize=10, textColor=GRAY_LIGHT, leading=14)
    s_badge = ParagraphStyle('Badge', parent=styles['Normal'],
        fontSize=14, fontName='Helvetica-Bold', textColor=WHITE, 
        alignment=TA_RIGHT, leading=18)
    s_meta = ParagraphStyle('Meta', parent=styles['Normal'],
        fontSize=10, textColor=GRAY_LIGHT, alignment=TA_RIGHT, leading=14)
    s_party_title = ParagraphStyle('PartyTitle', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Bold', textColor=GRAY_LIGHT, 
        leading=12, spaceAfter=4, textTransform='uppercase')
    s_party_name = ParagraphStyle('PartyName', parent=styles['Normal'],
        fontSize=14, fontName='Helvetica-Bold', textColor=BLACK, leading=18, spaceAfter=4)
    s_party_detail = ParagraphStyle('PartyDetail', parent=styles['Normal'],
        fontSize=9, textColor=GRAY_TEXT, leading=14)
    s_section = ParagraphStyle('Section', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold', textColor=DARK, leading=15, 
        spaceBefore=8, spaceAfter=4)
    s_detail = ParagraphStyle('Detail', parent=styles['Normal'],
        fontSize=9, textColor=GRAY_TEXT, leading=13)
    s_detail_bold = ParagraphStyle('DetailBold', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=DARK, leading=14, spaceBefore=8)
    s_detail_gold = ParagraphStyle('DetailGold', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=GOLD, leading=13)
    s_detail_red = ParagraphStyle('DetailRed', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor("#DC2626"), leading=14, spaceBefore=8)
    s_mention = ParagraphStyle('Mention', parent=styles['Normal'],
        fontSize=7, textColor=GRAY_LIGHT, alignment=TA_CENTER, leading=10)
    s_normal = ParagraphStyle('Normal2', parent=styles['Normal'],
        fontSize=10, textColor=GRAY_TEXT, leading=14)
    s_objet = ParagraphStyle('Objet', parent=styles['Normal'],
        fontSize=10, textColor=BLACK, leading=14)
    
    elements = []
    
    # ===================== HEADER =====================
    # Photo + Identity left, Badge right
    try:
        photo_path = get_photo()
        photo = Image(photo_path, width=18*mm, height=18*mm)
        photo.hAlign = 'LEFT'
    except:
        photo = Spacer(18*mm, 18*mm)
    
    identity_content = [
        [photo, 
         [Paragraph("Gilles Korzec", s_title),
          Paragraph("Coach Digital Paris — Transformation digitale & IA", s_subtitle)],
         [Paragraph("DEVIS", s_badge),
          Paragraph("N° DEV-2026-001", s_meta),
          Paragraph("02/03/2026", s_meta),
          Paragraph("Validité : 30 jours", s_meta)]
        ]
    ]
    
    header_table = Table(identity_content, colWidths=[22*mm, 75*mm, 60*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('BACKGROUND', (2, 0), (2, 0), DARK),
        ('ROUNDEDCORNERS', [0, 0, 0, 0]),
        ('TOPPADDING', (2, 0), (2, 0), 8),
        ('BOTTOMPADDING', (2, 0), (2, 0), 8),
        ('LEFTPADDING', (2, 0), (2, 0), 10),
        ('RIGHTPADDING', (2, 0), (2, 0), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=GRAY_BORDER))
    elements.append(Spacer(1, 6*mm))
    
    # ===================== PARTIES =====================
    emetteur = [
        Paragraph("ÉMETTEUR", s_party_title),
        Paragraph("Gilles Korzec", s_party_name),
        Paragraph(
            "Coach Digital Paris<br/>"
            "102 avenue des Champs-Élysées<br/>"
            "75008 Paris<br/>"
            "SIRET : 834 049 197 00028<br/>"
            "coachdigitalparis@gmail.com", s_party_detail
        )
    ]
    
    client = [
        Paragraph("CLIENT", s_party_title),
        Paragraph("BYRON PUB", s_party_name),
        Paragraph(
            "Pascal Mattheuws<br/>"
            "49 Rue Félix Faure<br/>"
            "06400 Cannes<br/>"
            "SIRET : À compléter", s_party_detail
        )
    ]
    
    parties_table = Table([[emetteur, client]], colWidths=[width/2, width/2])
    parties_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_BG),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(parties_table)
    elements.append(Spacer(1, 6*mm))
    
    # ===================== OBJET =====================
    elements.append(Paragraph(
        "<b>Objet :</b> Création site web international premium & hébergement annuel — BYRON Cannes", 
        s_objet
    ))
    elements.append(Paragraph(
        "<b>Prototype V1 :</b> <a href='https://byroncannes2026.vercel.app/' color='#1a1a2e'>https://byroncannes2026.vercel.app/</a>", 
        s_objet
    ))
    elements.append(Spacer(1, 5*mm))
    
    # ===================== TABLEAU =====================
    table_data = [
        [Paragraph("<b>Désignation</b>", ParagraphStyle('th', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, leading=12)),
         Paragraph("<b>Qté</b>", ParagraphStyle('th', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER, leading=12)),
         Paragraph("<b>P.U. HT</b>", ParagraphStyle('th', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_RIGHT, leading=12)),
         Paragraph("<b>Total HT</b>", ParagraphStyle('th', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_RIGHT, leading=12))],
        
        [Paragraph("Création site web dynamique haut de gamme — V1<br/><font size=7 color='#6b7280'>Site premium responsive, bilingue EN/FR, dark theme immersif, animations, formulaire privatisation, galerie photos/vidéos</font>", s_detail),
         Paragraph("1", ParagraphStyle('td', fontSize=10, alignment=TA_CENTER, textColor=GRAY_TEXT)),
         Paragraph("600,00 €", ParagraphStyle('td', fontSize=10, alignment=TA_RIGHT, textColor=GRAY_TEXT)),
         Paragraph("<b>600,00 €</b>", ParagraphStyle('td', fontSize=10, fontName='Helvetica-Bold', alignment=TA_RIGHT, textColor=BLACK))],
        
        [Paragraph("Hébergement, maintenance & mises à jour — 12 mois<br/><font size=7 color='#6b7280'>Hébergement Vercel, domaine, support technique, mises à jour site</font>", s_detail),
         Paragraph("12", ParagraphStyle('td', fontSize=10, alignment=TA_CENTER, textColor=GRAY_TEXT)),
         Paragraph("29,00 €", ParagraphStyle('td', fontSize=10, alignment=TA_RIGHT, textColor=GRAY_TEXT)),
         Paragraph("<b>348,00 €</b>", ParagraphStyle('td', fontSize=10, fontName='Helvetica-Bold', alignment=TA_RIGHT, textColor=BLACK))],
        
        [Paragraph("Indexation & référencement SEO Google<br/><font size=7 color='#6b7280'>SEO international, structured data, sitemap XML, meta tags, Open Graph — Valeur : 690,00€ HT</font>", s_detail),
         Paragraph("1", ParagraphStyle('td', fontSize=10, alignment=TA_CENTER, textColor=GRAY_TEXT)),
         Paragraph("<font color='#6b7280'><strike>690,00 €</strike></font>", ParagraphStyle('td', fontSize=10, alignment=TA_RIGHT, textColor=GRAY_TEXT)),
         Paragraph("<b><font color='#B8860B'>OFFERT</font></b>", ParagraphStyle('td', fontSize=10, fontName='Helvetica-Bold', alignment=TA_RIGHT))],
    ]
    
    col_widths = [width*0.50, width*0.10, width*0.20, width*0.20]
    
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        # Rows
        ('BACKGROUND', (0, 1), (-1, 1), WHITE),
        ('BACKGROUND', (0, 2), (-1, 2), GRAY_BG),
        ('BACKGROUND', (0, 3), (-1, 3), WHITE),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, GRAY_BORDER),
        ('LINEBELOW', (0, -1), (-1, -1), 1, GRAY_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.25, GRAY_BORDER),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 4*mm))
    
    # ===================== TOTAUX =====================
    total_ht = 948.00
    tva = 0  # Auto-entrepreneur art 293B
    total_ttc = 948.00
    
    totaux_data = [
        [Paragraph("Total HT", ParagraphStyle('tl', fontSize=10, textColor=GRAY_TEXT)),
         Paragraph("948,00 €", ParagraphStyle('tv', fontSize=10, textColor=BLACK, alignment=TA_RIGHT, fontName='Helvetica-Bold'))],
        [Paragraph("TVA", ParagraphStyle('tl', fontSize=10, textColor=GRAY_TEXT)),
         Paragraph("Non applicable (art. 293 B du CGI)", ParagraphStyle('tv', fontSize=9, textColor=GRAY_LIGHT, alignment=TA_RIGHT))],
        [Paragraph(""), Paragraph("")],  # divider row
        [Paragraph("<b>TOTAL TTC</b>", ParagraphStyle('tl', fontSize=14, fontName='Helvetica-Bold', textColor=BLACK)),
         Paragraph("<b>948,00 €</b>", ParagraphStyle('tv', fontSize=14, fontName='Helvetica-Bold', textColor=BLACK, alignment=TA_RIGHT))],
    ]
    
    # Right-aligned totaux
    empty_col = width * 0.55
    totaux_col = width * 0.45
    
    wrapper_data = [[
        "",
        Table(totaux_data, colWidths=[totaux_col*0.55, totaux_col*0.45], style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), GRAY_BG),
            ('LINEBELOW', (0, 1), (-1, 1), 1.5, GRAY_BORDER),
            ('TOPPADDING', (0, 2), (-1, 2), 0),
            ('BOTTOMPADDING', (0, 2), (-1, 2), 0),
        ]))
    ]]
    
    wrapper = Table(wrapper_data, colWidths=[empty_col, totaux_col])
    wrapper.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(wrapper)
    elements.append(Spacer(1, 5*mm))
    
    # ===================== TARIF FIDÉLITÉ =====================
    elements.append(Paragraph("TARIF FIDÉLITÉ — Client partenaire depuis plus de 7 ans, renouvellement refonte", s_detail_gold))
    elements.append(Spacer(1, 2*mm))
    
    fidelite_data = [
        ["Création site web premium", "1 600,00 € HT", "600,00 € HT", "– 1 000,00 €"],
        ["Indexation SEO Google", "690,00 € HT", "OFFERT", "– 690,00 €"],
        ["TOTAL REMISÉ", "2 290,00 € HT", "948,00 € HT", "– 1 342,00 €"],
    ]
    
    fidelite_header = [
        Paragraph("<b>Prestation</b>", ParagraphStyle('fh', fontSize=8, fontName='Helvetica-Bold', textColor=WHITE)),
        Paragraph("<b>Tarif normal</b>", ParagraphStyle('fh', fontSize=8, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_RIGHT)),
        Paragraph("<b>Tarif appliqué</b>", ParagraphStyle('fh', fontSize=8, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_RIGHT)),
        Paragraph("<b>Économie</b>", ParagraphStyle('fh', fontSize=8, fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_RIGHT)),
    ]
    
    fd = [fidelite_header]
    for i, row in enumerate(fidelite_data):
        is_total = i == len(fidelite_data) - 1
        fname = 'Helvetica-Bold' if is_total else 'Helvetica'
        fd.append([
            Paragraph(row[0], ParagraphStyle('fd', fontSize=8, fontName=fname, textColor=DARK)),
            Paragraph(row[1], ParagraphStyle('fd', fontSize=8, textColor=GRAY_LIGHT, alignment=TA_RIGHT)),
            Paragraph(row[2], ParagraphStyle('fd', fontSize=8, fontName=fname, textColor=GOLD if not is_total else BLACK, alignment=TA_RIGHT)),
            Paragraph(row[3], ParagraphStyle('fd', fontSize=8, fontName=fname, textColor=colors.HexColor("#16a34a"), alignment=TA_RIGHT)),
        ])
    
    ft = Table(fd, colWidths=[width*0.35, width*0.22, width*0.22, width*0.21])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, GRAY_BORDER),
        ('LINEABOVE', (0, -1), (-1, -1), 1, DARK),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#f0fdf4")),
    ]))
    elements.append(ft)
    elements.append(Spacer(1, 5*mm))
    
    # ===================== DÉTAILS PRESTATIONS =====================
    elements.append(Paragraph("DÉTAIL DES PRESTATIONS INCLUSES", s_section))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_BORDER))
    elements.append(Spacer(1, 2*mm))
    
    elements.append(Paragraph("<b>SITE WEB DYNAMIQUE HAUT DE GAMME — VERSION 1</b>", s_detail_bold))
    details_site = [
        "Design immersif dark theme premium, 100% responsive (mobile, tablette, desktop)",
        "Site bilingue anglais / français (anglais par défaut pour la cible internationale)",
        "Pages : Accueil immersive avec vidéo, Espaces & Privatisation, Club & DJ, Contact & Réservation",
        "Formulaire de demande de privatisation intégré sur chaque page",
        "Galerie photos et vidéos des espaces et événements",
        "Animations premium : parallax, scroll reveal, vidéo background, effets 3D",
    ]
    for d in details_site:
        elements.append(Paragraph(f"• {d}", s_detail))
    
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph("<b>ÉVOLUTIONS PRÉVUES (incluses — après retours client)</b>", s_detail_bold))
    evolutions = [
        "Module de réservation en ligne des événements et privatisations",
        "Carte des menus dynamique avec interface d'administration dédiée — modification des menus en toute autonomie, mise à jour automatique sur le site",
    ]
    for d in evolutions:
        elements.append(Paragraph(f"• {d}", s_detail))
    
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph("<b>HÉBERGEMENT, MAINTENANCE & MISES À JOUR — 12 MOIS</b>", s_detail_bold))
    hebergement = [
        "Hébergement haute performance Vercel (CDN mondial, SSL inclus)",
        "Nom de domaine inclus",
        "Support technique et mises à jour du site",
        "Sauvegardes régulières",
    ]
    for d in hebergement:
        elements.append(Paragraph(f"• {d}", s_detail))
    
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph("<b>INDEXATION SEO GOOGLE (OFFERTE — valeur 690€ HT)</b>", s_detail_bold))
    seo = [
        "Référencement international ciblé : « event venue Cannes », « private hire Cannes », « corporate event French Riviera », « MIPIM venue Cannes »...",
        "Données structurées LocalBusiness + EventVenue pour Google",
        "Sitemap XML, meta tags optimisés, Open Graph pour les réseaux sociaux",
    ]
    for d in seo:
        elements.append(Paragraph(f"• {d}", s_detail))
    
    elements.append(Spacer(1, 4*mm))
    
    # ===================== NON COMPRIS =====================
    elements.append(Paragraph("⚠ CE DEVIS NE COMPREND PAS", s_detail_red))
    non_compris = [
        "Community management & gestion des réseaux sociaux",
        "Agent manager communication dédié (création visuels, veille événementielle, pilotage réseaux)",
    ]
    for d in non_compris:
        elements.append(Paragraph(f"• {d}", s_detail))
    elements.append(Spacer(1, 2*mm))
    elements.append(Paragraph(
        "→ Sur acceptation de ce devis, une offre complémentaire <b>Agent Manager Communication</b> "
        "(réseaux sociaux, visuels, veille événementielle, communication 24/7) sera proposée "
        "à un <b>tarif préférentiel de 300 à 600€ HT/mois</b>.",
        s_detail
    ))
    
    elements.append(Spacer(1, 6*mm))
    
    # ===================== PAIEMENT =====================
    bank_data = [[
        Paragraph(
            "<b>💳 RÈGLEMENT PAR VIREMENT BANCAIRE</b><br/><br/>"
            "<b>Bénéficiaire : Gilles Korzec</b><br/>"
            "IBAN : FR76 1695 8000 0133 0858 7025 176<br/>"
            "BIC : QNTOFRP1XXX<br/><br/>"
            "Règlement à réception du devis signé. Acompte de 40% minimum à la commande, solde à la livraison.",
            ParagraphStyle('bank', fontSize=9, textColor=GRAY_TEXT, leading=14)
        )
    ]]
    
    bt = Table(bank_data, colWidths=[width])
    bt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_BG),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('BOX', (0, 0), (-1, -1), 0.5, GRAY_BORDER),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 4*mm))

    # ===================== SIGNATURE =====================
    sig_data = [
        [Paragraph("<b>Bon pour accord</b><br/><br/><br/><br/>Date et signature du client :", 
                    ParagraphStyle('sig', fontSize=9, textColor=GRAY_TEXT, leading=14)),
         ""]
    ]
    st = Table(sig_data, colWidths=[width*0.5, width*0.5])
    st.setStyle(TableStyle([
        ('BOX', (0, 0), (0, 0), 0.5, GRAY_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(st)
    elements.append(Spacer(1, 4*mm))
    
    # ===================== MENTIONS =====================
    elements.append(Paragraph(
        "Gilles Korzec — SIRET 834 049 197 00028 — 102 avenue des Champs-Élysées, 75008 Paris<br/>"
        "TVA non applicable, art. 293 B du CGI — Auto-entrepreneur",
        s_mention
    ))
    
    # Build
    doc.build(elements)
    print(f"✅ PDF généré : {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
