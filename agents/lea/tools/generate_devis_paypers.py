#!/usr/bin/env python3
"""
Devis DEV-2026-002 — Application Paypers/Skippy pour Hannah Taieb
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "factures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Couleurs
BLEU = HexColor("#1a365d")
BLEU_CLAIR = HexColor("#e8f0fe")
GRIS = HexColor("#f5f5f5")
GRIS_TEXTE = HexColor("#555555")
ACCENT = HexColor("#2563eb")

def build_devis():
    output_path = os.path.join(OUTPUT_DIR, "DEV-2026-002-Paypers-HannahTaieb.pdf")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=20*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    titre_style = ParagraphStyle('Titre', parent=styles['Heading1'], fontSize=22, textColor=BLEU, spaceAfter=3*mm)
    sous_titre = ParagraphStyle('SousTitre', parent=styles['Normal'], fontSize=11, textColor=GRIS_TEXTE, spaceAfter=5*mm)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=13, textColor=BLEU, spaceBefore=6*mm, spaceAfter=3*mm, borderPadding=(0,0,2,0))
    normal = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, leading=14, textColor=black)
    normal_small = ParagraphStyle('SmallNormal', parent=styles['Normal'], fontSize=9, leading=12, textColor=GRIS_TEXTE)
    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontSize=10, leading=14, textColor=black, fontName='Helvetica-Bold')
    right_style = ParagraphStyle('Right', parent=styles['Normal'], fontSize=10, alignment=TA_RIGHT)
    center_style = ParagraphStyle('Center', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)
    total_style = ParagraphStyle('Total', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold', textColor=BLEU, alignment=TA_RIGHT)
    
    elements = []
    
    # === EN-TÊTE ===
    header_data = [
        [
            Paragraph("<b>G. KORZEC</b><br/>Coach Digital Paris<br/>102 avenue des Champs-Élysées<br/>75008 Paris<br/>SIRET : 834 049 197 00028<br/>Tél : +33 6 52 34 51 80<br/>coachdigitalparis@gmail.com", normal_small),
            Paragraph("<b>DEVIS</b><br/><br/><b>N° DEV-2026-002</b><br/>Date : 11 mars 2026<br/>Validité : 30 jours", ParagraphStyle('HeaderRight', parent=normal_small, alignment=TA_RIGHT, fontSize=10))
        ]
    ]
    header_table = Table(header_data, colWidths=[90*mm, 80*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8*mm))
    
    # === CLIENT ===
    elements.append(Paragraph("DESTINATAIRE", ParagraphStyle('DestLabel', parent=normal_small, fontSize=8, textColor=ACCENT)))
    client_data = [
        [Paragraph("<b>SYSTEMIC</b><br/>M. Hubert TAIEB — Président<br/>24 rue de Caumartin<br/>75009 Paris<br/>SIRET : 397 982 463 00036", normal)]
    ]
    client_table = Table(client_data, colWidths=[170*mm])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLEU_CLAIR),
        ('BOX', (0,0), (-1,-1), 0.5, ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
    ]))
    elements.append(client_table)
    elements.append(Spacer(1, 6*mm))
    
    # === OBJET ===
    elements.append(Paragraph("OBJET DU DEVIS", section_style))
    elements.append(Paragraph(
        "Conception, développement et déploiement de l'application <b>PAYPERS</b> (nom de travail) — "
        "Copilote administratif et financier tout-en-un pour jeunes adultes (18-30 ans). "
        "Application web progressive (PWA) responsive mobile-first.",
        normal
    ))
    elements.append(Spacer(1, 4*mm))
    
    # === TABLEAU PRESTATIONS ===
    elements.append(Paragraph("DÉTAIL DES PRESTATIONS", section_style))
    
    col_widths = [8*mm, 95*mm, 30*mm, 35*mm]
    
    prestations_header = [
        Paragraph("<b>N°</b>", ParagraphStyle('TH', parent=normal, textColor=white, fontSize=9, alignment=TA_CENTER)),
        Paragraph("<b>Désignation</b>", ParagraphStyle('TH', parent=normal, textColor=white, fontSize=9)),
        Paragraph("<b>Qté</b>", ParagraphStyle('TH', parent=normal, textColor=white, fontSize=9, alignment=TA_CENTER)),
        Paragraph("<b>Prix HT</b>", ParagraphStyle('TH', parent=normal, textColor=white, fontSize=9, alignment=TA_RIGHT)),
    ]
    
    prestations = [
        prestations_header,
        [
            Paragraph("1", center_style),
            Paragraph("<b>Conception & Architecture</b><br/>"
                      "— Cahier des charges fonctionnel détaillé<br/>"
                      "— Architecture technique (stack, BDD, APIs)<br/>"
                      "— Maquettes UI/UX (wireframes + design system)<br/>"
                      "— Charte graphique & branding app", normal_small),
            Paragraph("1", center_style),
            Paragraph("800 €", right_style),
        ],
        [
            Paragraph("2", center_style),
            Paragraph("<b>Développement Front-End (PWA)</b><br/>"
                      "— Interface responsive mobile-first (Next.js / React)<br/>"
                      "— 6 modules : Dashboard, Droits & Aides, Finances,<br/>"
                      "  Documents (coffre-fort), Mots de passe, Copilote IA<br/>"
                      "— Progressive Web App (installation mobile)<br/>"
                      "— Animations & micro-interactions", normal_small),
            Paragraph("1", center_style),
            Paragraph("1 200 €", right_style),
        ],
        [
            Paragraph("3", center_style),
            Paragraph("<b>Développement Back-End & Base de données</b><br/>"
                      "— API REST sécurisée (Supabase / Node.js)<br/>"
                      "— Authentification (email, Google, biométrie)<br/>"
                      "— Base de données utilisateurs, documents, profils<br/>"
                      "— Chiffrement des données sensibles (AES-256)<br/>"
                      "— Stockage sécurisé documents (coffre-fort numérique)", normal_small),
            Paragraph("1", center_style),
            Paragraph("900 €", right_style),
        ],
        [
            Paragraph("4", center_style),
            Paragraph("<b>Intégration APIs & Moteur IA</b><br/>"
                      "— Simulateur d'aides sociales (OpenFisca)<br/>"
                      "— Copilote IA conversationnel (aide admin/juridique)<br/>"
                      "— Intégration services tiers (CAF, Impôts, Ameli...)<br/>"
                      "— Module abonnements intelligents (détection, alertes)", normal_small),
            Paragraph("1", center_style),
            Paragraph("800 €", right_style),
        ],
        [
            Paragraph("5", center_style),
            Paragraph("<b>Tests, Recette & Déploiement</b><br/>"
                      "— Tests unitaires & tests d'intégration<br/>"
                      "— Phase bêta (correctifs & ajustements UX)<br/>"
                      "— Déploiement production (hébergement, SSL, DNS)<br/>"
                      "— Soumission stores (si applicable) & référencement<br/>"
                      "— Formation utilisation & back-office", normal_small),
            Paragraph("1", center_style),
            Paragraph("490 €", right_style),
        ],
        [
            Paragraph("6", center_style),
            Paragraph("<b>Hébergement & Maintenance — 3 mois inclus</b><br/>"
                      "— Hébergement cloud sécurisé<br/>"
                      "— Certificat SSL, sauvegardes automatiques<br/>"
                      "— Support technique & corrections de bugs<br/>"
                      "— Mises à jour de sécurité", normal_small),
            Paragraph("1", center_style),
            Paragraph("300 €", right_style),
        ],
    ]
    
    prest_table = Table(prestations, colWidths=col_widths, repeatRows=1)
    prest_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0,0), (-1,0), BLEU),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        # Alternating rows
        ('BACKGROUND', (0,1), (-1,1), GRIS),
        ('BACKGROUND', (0,3), (-1,3), GRIS),
        ('BACKGROUND', (0,5), (-1,5), GRIS),
        # Borders
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#dddddd")),
        ('BOX', (0,0), (-1,-1), 1, BLEU),
        # Padding
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(prest_table)
    elements.append(Spacer(1, 5*mm))
    
    # === TOTAUX ===
    totaux_data = [
        [Paragraph("Total HT", bold_style), Paragraph("<b>4 490,00 €</b>", ParagraphStyle('TR', parent=right_style, fontName='Helvetica-Bold'))],
        [Paragraph("TVA 20%", normal), Paragraph("898,00 €", right_style)],
        [Paragraph("<b>TOTAL TTC</b>", ParagraphStyle('TotalLabel', parent=bold_style, fontSize=13, textColor=BLEU)), 
         Paragraph("<b>5 388,00 €</b>", ParagraphStyle('TotalVal', parent=right_style, fontSize=13, fontName='Helvetica-Bold', textColor=BLEU))],
    ]
    totaux_table = Table(totaux_data, colWidths=[120*mm, 48*mm])
    totaux_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, BLEU),
        ('LINEABOVE', (0,2), (-1,2), 1.5, BLEU),
        ('LINEBELOW', (0,2), (-1,2), 1.5, BLEU),
        ('BACKGROUND', (0,2), (-1,2), BLEU_CLAIR),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    elements.append(totaux_table)
    elements.append(Spacer(1, 6*mm))
    
    # === CONDITIONS DE PAIEMENT ===
    elements.append(Paragraph("CONDITIONS DE PAIEMENT", section_style))
    
    conditions_data = [
        [Paragraph("✅ <b>Acompte à la commande (50%)</b>", normal), Paragraph("<b>2 694,00 €</b>", ParagraphStyle('R', parent=right_style, fontName='Helvetica-Bold', textColor=ACCENT))],
        [Paragraph("Solde à la livraison (50%)", normal), Paragraph("2 694,00 €", right_style)],
    ]
    cond_table = Table(conditions_data, colWidths=[120*mm, 48*mm])
    cond_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#e8f8e8")),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
        ('LINEBELOW', (0,0), (-1,0), 0.5, HexColor("#cccccc")),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
    ]))
    elements.append(cond_table)
    elements.append(Spacer(1, 3*mm))
    
    elements.append(Paragraph(
        "<b>Paiement par virement bancaire :</b><br/>"
        "Bénéficiaire : Gilles Korzec<br/>"
        "IBAN : FR76 1695 8000 0133 0858 7025 176<br/>"
        "BIC : QNTOFRP1XXX",
        normal_small
    ))
    elements.append(Spacer(1, 5*mm))
    
    # === DÉLAIS ===
    elements.append(Paragraph("DÉLAIS DE RÉALISATION", section_style))
    elements.append(Paragraph(
        "— <b>Démarrage</b> : dès réception de l'acompte de 50%<br/>"
        "— <b>Phase 1</b> — Conception & maquettes : 1 à 2 semaines<br/>"
        "— <b>Phase 2</b> — Développement : 4 à 6 semaines<br/>"
        "— <b>Phase 3</b> — Tests bêta & recette : 1 à 2 semaines<br/>"
        "— <b>Livraison estimée</b> : 8 à 10 semaines après validation des maquettes<br/>"
        "— Points d'avancement réguliers par WhatsApp et/ou visio",
        normal
    ))
    elements.append(Spacer(1, 5*mm))
    
    # === LIVRABLES ===
    elements.append(Paragraph("LIVRABLES INCLUS", section_style))
    elements.append(Paragraph(
        "✓ Application web progressive (PWA) responsive et installable sur mobile<br/>"
        "✓ 6 modules fonctionnels (Dashboard, Droits, Finances, Docs, MDP, IA)<br/>"
        "✓ Back-office d'administration<br/>"
        "✓ Code source complet hébergé sur GitHub<br/>"
        "✓ Documentation technique<br/>"
        "✓ 3 mois d'hébergement et maintenance inclus<br/>"
        "✓ Formation utilisation (1 session visio)",
        normal
    ))
    elements.append(Spacer(1, 5*mm))
    
    # === MENTIONS ===
    elements.append(HRFlowable(width="100%", color=HexColor("#cccccc")))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        "<i>"
        "En cas d'acceptation, merci de retourner ce devis signé avec la mention « Bon pour accord » "
        "accompagné du règlement de l'acompte de 2 694,00 €.<br/>"
        "Devis valable 30 jours à compter de sa date d'émission.</i>",
        ParagraphStyle('Mentions', parent=normal_small, fontSize=8, leading=11)
    ))
    elements.append(Spacer(1, 8*mm))
    
    # === SIGNATURES ===
    sig_data = [
        [Paragraph("<b>Le prestataire</b><br/>G. KORZEC — Coach Digital Paris<br/><br/><br/><br/>Date et signature", normal_small),
         Paragraph("<b>Le client</b><br/>SYSTEMIC<br/>M. Hubert TAIEB<br/><br/><br/><br/>Date, signature<br/>et mention « Bon pour accord »", normal_small)]
    ]
    sig_table = Table(sig_data, colWidths=[85*mm, 85*mm])
    sig_table.setStyle(TableStyle([
        ('BOX', (0,0), (0,0), 0.5, HexColor("#cccccc")),
        ('BOX', (1,0), (1,0), 0.5, HexColor("#cccccc")),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(sig_table)
    
    # Build
    doc.build(elements)
    print(f"✅ Devis généré : {output_path}")
    return output_path

if __name__ == "__main__":
    build_devis()
