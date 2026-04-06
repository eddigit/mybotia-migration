#!/usr/bin/env python3
"""
Facture FA-2026-032 — SELARL Clément Delpiano — Refonte site web
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "factures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLEU = HexColor("#1a365d")
BLEU_CLAIR = HexColor("#e8f0fe")
GRIS = HexColor("#f5f5f5")
GRIS_TEXTE = HexColor("#555555")
ACCENT = HexColor("#2563eb")
VERT = HexColor("#16a34a")

def build():
    output_path = os.path.join(OUTPUT_DIR, "FA-2026-032-ClementDelpiano.pdf")
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm, topMargin=15*mm, bottomMargin=20*mm)
    
    styles = getSampleStyleSheet()
    
    titre_style = ParagraphStyle('Titre', parent=styles['Heading1'], fontSize=22, textColor=BLEU, spaceAfter=3*mm)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=13, textColor=BLEU, spaceBefore=6*mm, spaceAfter=3*mm)
    normal = ParagraphStyle('N', parent=styles['Normal'], fontSize=10, leading=14, textColor=black)
    normal_small = ParagraphStyle('NS', parent=styles['Normal'], fontSize=9, leading=12, textColor=GRIS_TEXTE)
    bold_style = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, leading=14, fontName='Helvetica-Bold')
    right_style = ParagraphStyle('R', parent=styles['Normal'], fontSize=10, alignment=TA_RIGHT)
    center_style = ParagraphStyle('C', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)
    
    elements = []
    
    # === EN-TÊTE ===
    header_data = [
        [
            Paragraph("<b>G. KORZEC</b><br/>Coach Digital Paris<br/>102 avenue des Champs-Élysées<br/>75008 Paris<br/>SIRET : 834 049 197 00028<br/>Tél : +33 6 52 34 51 80<br/>coachdigitalparis@gmail.com", normal_small),
            Paragraph("<b>FACTURE</b><br/><br/><b>N° FA-2026-032</b><br/>Date : 6 mars 2026", ParagraphStyle('HR', parent=normal_small, alignment=TA_RIGHT, fontSize=10))
        ]
    ]
    ht = Table(header_data, colWidths=[90*mm, 80*mm])
    ht.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(ht)
    elements.append(Spacer(1, 8*mm))
    
    # === CLIENT ===
    elements.append(Paragraph("FACTURÉ À", ParagraphStyle('DL', parent=normal_small, fontSize=8, textColor=ACCENT)))
    client_data = [
        [Paragraph("<b>SELARL CLÉMENT DELPIANO</b><br/>Maître Valérie CLÉMENT<br/>Avocate au Barreau de Nice<br/>Email : valerie.clement@avocat.fr", normal)]
    ]
    ct = Table(client_data, colWidths=[170*mm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLEU_CLAIR),
        ('BOX', (0,0), (-1,-1), 0.5, ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
    ]))
    elements.append(ct)
    elements.append(Spacer(1, 6*mm))
    
    # === OBJET ===
    elements.append(Paragraph("OBJET", section_style))
    elements.append(Paragraph(
        "Refonte complète du site internet professionnel du Cabinet Clément Delpiano — "
        "Conception, développement, intégration et déploiement.",
        normal
    ))
    elements.append(Spacer(1, 4*mm))
    
    # === TABLEAU PRESTATIONS ===
    elements.append(Paragraph("DÉTAIL DES PRESTATIONS", section_style))
    
    col_widths = [8*mm, 100*mm, 25*mm, 35*mm]
    
    prestations = [
        [
            Paragraph("<b>N°</b>", ParagraphStyle('TH', parent=normal, textColor=white, fontSize=9, alignment=TA_CENTER)),
            Paragraph("<b>Désignation</b>", ParagraphStyle('TH2', parent=normal, textColor=white, fontSize=9)),
            Paragraph("<b>Qté</b>", ParagraphStyle('TH3', parent=normal, textColor=white, fontSize=9, alignment=TA_CENTER)),
            Paragraph("<b>Prix HT</b>", ParagraphStyle('TH4', parent=normal, textColor=white, fontSize=9, alignment=TA_RIGHT)),
        ],
        [
            Paragraph("1", center_style),
            Paragraph("<b>Conception & Design</b><br/>"
                      "— Audit du site existant<br/>"
                      "— Maquettes UI/UX personnalisées<br/>"
                      "— Charte graphique & identité visuelle cabinet", normal_small),
            Paragraph("1", center_style),
            Paragraph("500 €", right_style),
        ],
        [
            Paragraph("2", center_style),
            Paragraph("<b>Développement site web professionnel</b><br/>"
                      "— Site vitrine responsive (desktop, tablette, mobile)<br/>"
                      "— Pages : Accueil, Cabinet, Équipe, Domaines, Contact<br/>"
                      "— Formulaire de contact sécurisé<br/>"
                      "— Optimisation SEO (référencement naturel Google)", normal_small),
            Paragraph("1", center_style),
            Paragraph("1 200 €", right_style),
        ],
        [
            Paragraph("3", center_style),
            Paragraph("<b>Intégration & Fonctionnalités avancées</b><br/>"
                      "— Intégration domaine avocat.fr<br/>"
                      "— Certificat SSL & sécurité HTTPS<br/>"
                      "— Conformité RGPD (mentions légales, cookies)<br/>"
                      "— Performance & accessibilité", normal_small),
            Paragraph("1", center_style),
            Paragraph("500 €", right_style),
        ],
        [
            Paragraph("4", center_style),
            Paragraph("<b>Déploiement & Mise en production</b><br/>"
                      "— Hébergement & configuration serveur<br/>"
                      "— Migration DNS & mise en ligne<br/>"
                      "— Tests multi-navigateurs & mobile<br/>"
                      "— Formation utilisation", normal_small),
            Paragraph("1", center_style),
            Paragraph("300 €", right_style),
        ],
    ]
    
    pt = Table(prestations, colWidths=col_widths, repeatRows=1)
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLEU),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('BACKGROUND', (0,1), (-1,1), GRIS),
        ('BACKGROUND', (0,3), (-1,3), GRIS),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#dddddd")),
        ('BOX', (0,0), (-1,-1), 1, BLEU),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 5*mm))
    
    # === TOTAUX ===
    totaux_data = [
        [Paragraph("Total HT", bold_style), Paragraph("<b>2 500,00 €</b>", ParagraphStyle('TR', parent=right_style, fontName='Helvetica-Bold'))],
        [Paragraph("TVA 20%", normal), Paragraph("500,00 €", right_style)],
        [Paragraph("<b>TOTAL TTC</b>", ParagraphStyle('TL', parent=bold_style, fontSize=13, textColor=BLEU)), 
         Paragraph("<b>3 000,00 €</b>", ParagraphStyle('TV', parent=right_style, fontSize=13, fontName='Helvetica-Bold', textColor=BLEU))],
    ]
    tt = Table(totaux_data, colWidths=[120*mm, 48*mm])
    tt.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, BLEU),
        ('LINEABOVE', (0,2), (-1,2), 1.5, BLEU),
        ('LINEBELOW', (0,2), (-1,2), 1.5, BLEU),
        ('BACKGROUND', (0,2), (-1,2), BLEU_CLAIR),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    elements.append(tt)
    elements.append(Spacer(1, 6*mm))
    
    # === RÈGLEMENTS ===
    elements.append(Paragraph("SITUATION DES RÈGLEMENTS", section_style))
    
    regl_data = [
        [
            Paragraph("<b>Date</b>", ParagraphStyle('RH', parent=normal, textColor=white, fontSize=9)),
            Paragraph("<b>Désignation</b>", ParagraphStyle('RH2', parent=normal, textColor=white, fontSize=9)),
            Paragraph("<b>Mode</b>", ParagraphStyle('RH3', parent=normal, textColor=white, fontSize=9, alignment=TA_CENTER)),
            Paragraph("<b>Montant HT</b>", ParagraphStyle('RH4', parent=normal, textColor=white, fontSize=9, alignment=TA_RIGHT)),
        ],
        [
            Paragraph("23/02/2026", normal),
            Paragraph("Acompte n°1", normal),
            Paragraph("Virement", center_style),
            Paragraph("800,00 €", right_style),
        ],
        [
            Paragraph("06/03/2026", normal),
            Paragraph("Acompte n°2", normal),
            Paragraph("Virement", center_style),
            Paragraph("500,00 €", right_style),
        ],
    ]
    rt = Table(regl_data, colWidths=[30*mm, 68*mm, 30*mm, 40*mm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLEU),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('BACKGROUND', (0,1), (-1,1), HexColor("#e8f8e8")),
        ('BACKGROUND', (0,2), (-1,2), HexColor("#e8f8e8")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#dddddd")),
        ('BOX', (0,0), (-1,-1), 1, BLEU),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 3*mm))
    
    # Récap règlements
    recap_data = [
        [Paragraph("Total réglé", bold_style), Paragraph("<b>1 300,00 €</b>", ParagraphStyle('RR', parent=right_style, fontName='Helvetica-Bold', textColor=VERT))],
        [Paragraph("<b>Solde restant dû</b>", ParagraphStyle('SL', parent=bold_style, fontSize=12, textColor=HexColor("#dc2626"))), 
         Paragraph("<b>1 700,00 €</b>", ParagraphStyle('SV', parent=right_style, fontSize=12, fontName='Helvetica-Bold', textColor=HexColor("#dc2626")))],
    ]
    rct = Table(recap_data, colWidths=[120*mm, 48*mm])
    rct.setStyle(TableStyle([
        ('LINEABOVE', (0,1), (-1,1), 1, HexColor("#dc2626")),
        ('LINEBELOW', (0,1), (-1,1), 1, HexColor("#dc2626")),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    elements.append(rct)
    elements.append(Spacer(1, 6*mm))
    
    # === PAIEMENT ===
    elements.append(Paragraph(
        "<b>Règlement du solde par virement bancaire :</b><br/>"
        "Bénéficiaire : Gilles Korzec<br/>"
        "IBAN : FR76 1695 8000 0133 0858 7025 176<br/>"
        "BIC : QNTOFRP1XXX",
        normal_small
    ))
    elements.append(Spacer(1, 5*mm))
    
    # === MENTIONS ===
    elements.append(HRFlowable(width="100%", color=HexColor("#cccccc")))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        "<i>N° TVA intracommunautaire : à demander<br/>"
        "En cas de retard de paiement, une pénalité de 3 fois le taux d'intérêt légal sera appliquée, "
        "ainsi qu'une indemnité forfaitaire de recouvrement de 40 €.</i>",
        ParagraphStyle('M', parent=normal_small, fontSize=8, leading=11)
    ))
    
    doc.build(elements)
    print(f"✅ Facture générée : {output_path}")
    return output_path

if __name__ == "__main__":
    build()
