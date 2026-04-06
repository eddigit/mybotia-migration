#!/usr/bin/env python3
"""Génère la facture Aubagnac avec remise"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import os

def generate_invoice(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, 
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    
    elements = []
    
    # En-tête entreprise
    header_data = [
        [Paragraph("<b>G. KORZEC</b>", styles['Normal']), ""],
        ["SIRET : 834 049 197 00028", ""],
        ["102 avenue des Champs-Élysées", ""],
        ["75008 Paris", ""],
    ]
    header_table = Table(header_data, colWidths=[10*cm, 7*cm])
    elements.append(header_table)
    elements.append(Spacer(1, 1*cm))
    
    # Titre facture
    elements.append(Paragraph("<b>FACTURE D'ACOMPTE N° FA-2026-021</b>", 
                             ParagraphStyle(name='Title', fontSize=16, alignment=TA_CENTER)))
    elements.append(Paragraph("Date : 21 février 2026", 
                             ParagraphStyle(name='Date', fontSize=10, alignment=TA_CENTER)))
    elements.append(Spacer(1, 1*cm))
    
    # Client
    client_data = [
        [Paragraph("<b>FACTURÉ À :</b>", styles['Normal'])],
        ["Jean-Luc Aubagnac"],
        ["jeanluc@aubagnac.com"],
    ]
    client_table = Table(client_data, colWidths=[17*cm])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(client_table)
    elements.append(Spacer(1, 1*cm))
    
    # Objet
    elements.append(Paragraph("<b>Objet :</b> Acompte création agents MyBotIA + 1er mois d'abonnement", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Lignes de facturation
    table_data = [
        ['Description', 'Qté', 'Prix unitaire HT', 'Total HT']
    ]
    
    lignes = [
        {'description': 'Setup initial — Création sur-mesure 2 agents IA', 'quantite': 1, 'prix': 500.00},
        {'description': 'Agent Admin & Juridique — Formule PREMIUM (1 mois)', 'quantite': 1, 'prix': 200.00},
        {'description': 'Agent Commercial — Formule FREEMIUM La Totale (1 mois)', 'quantite': 1, 'prix': 100.00},
    ]
    
    for ligne in lignes:
        table_data.append([
            ligne['description'],
            str(ligne['quantite']),
            f"{ligne['prix']:.2f} €",
            f"{ligne['prix']:.2f} €"
        ])
    
    # Sous-total, remise, totaux
    table_data.append(['', '', '', ''])
    table_data.append(['', '', Paragraph("<b>Sous-total HT</b>", styles['Right']), "800,00 €"])
    table_data.append([Paragraph("<b>🎁 Remise spéciale Jean-Luc</b>", styles['Normal']), '', '', Paragraph("<b>- 500,00 €</b>", styles['Right'])])
    table_data.append(['', '', Paragraph("<b>TOTAL HT</b>", styles['Right']), Paragraph("<b>300,00 €</b>", styles['Right'])])
    table_data.append(['', '', Paragraph("<b>TVA 20%</b>", styles['Right']), "60,00 €"])
    table_data.append(['', '', Paragraph("<b>TOTAL TTC</b>", styles['Right']), Paragraph("<b>360,00 €</b>", styles['Right'])])
    
    invoice_table = Table(table_data, colWidths=[9*cm, 1.5*cm, 3.5*cm, 3*cm])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, 3), 1, colors.black),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#e8f5e9')),  # Ligne remise en vert clair
        ('BACKGROUND', (-1, -1), (-1, -1), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.white),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 1.5*cm))
    
    # Coordonnées bancaires
    elements.append(Paragraph("<b>COORDONNÉES BANCAIRES POUR VIREMENT INSTANTANÉ</b>", styles['Normal']))
    elements.append(Spacer(1, 0.3*cm))
    
    bank_data = [
        ['Bénéficiaire', 'Gilles Korzec'],
        ['Banque', 'Qonto'],
        ['IBAN', 'FR76 1695 8000 0133 0858 7025 176'],
        ['BIC', 'QNTOFRP1XXX'],
    ]
    bank_table = Table(bank_data, colWidths=[4*cm, 13*cm])
    bank_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(bank_table)
    elements.append(Spacer(1, 1*cm))
    
    # Mention légale
    elements.append(Paragraph("<i>Virement instantané accepté — Merci de votre confiance.</i>", 
                             ParagraphStyle(name='Footer', fontSize=9, alignment=TA_CENTER)))
    
    doc.build(elements)
    print(f"Facture générée : {output_path}")

if __name__ == "__main__":
    output = '/home/gillescoach/.openclaw/workspace/factures/FA-2026-021-Aubagnac.pdf'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_invoice(output)
