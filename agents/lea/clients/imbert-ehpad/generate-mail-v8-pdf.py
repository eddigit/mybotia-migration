#!/usr/bin/env python3
"""Génère le PDF V8 — version courte avec lien vers site"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

OUTPUT = "/home/gilles/.openclaw/workspace/clients/imbert-ehpad/mail-imbert-v8.pdf"
SITE_URL = "https://collab-igh.vercel.app/"  # À remplacer quand on aura l'URL

doc = SimpleDocTemplate(OUTPUT, pagesize=A4, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()

styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=18, textColor=HexColor('#0a75a9'), spaceAfter=8))
styles.add(ParagraphStyle('Sub', parent=styles['Normal'], fontSize=12, textColor=HexColor('#666666'), alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Quote', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8, leftIndent=20, textColor=HexColor('#0a75a9'), fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('Link', parent=styles['Normal'], fontSize=13, leading=18, spaceAfter=8, alignment=TA_CENTER, textColor=HexColor('#0a75a9'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, leading=12, spaceAfter=4, textColor=HexColor('#999999'), fontName='Helvetica-Oblique', alignment=TA_CENTER))
styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=4, leftIndent=15))
styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=10, leading=13))
styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=10, leading=13, fontName='Helvetica-Bold', textColor=colors.white))

story = []

def hr():
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc'), spaceBefore=10, spaceAfter=10))

# Header
story.append(Paragraph("COACH DIGITAL PARIS", ParagraphStyle('Brand', parent=styles['Normal'], fontSize=9, textColor=HexColor('#999999'), alignment=TA_CENTER)))
story.append(Spacer(1, 6))
story.append(Paragraph("Suite à notre réunion du 9 mars", styles['Title2']))
story.append(Paragraph("Votre dossier de projet est en ligne", styles['Sub']))

hr()

story.append(Paragraph("Monsieur Imbert, Monsieur Cozon,", styles['Body']))
story.append(Spacer(1, 8))
story.append(Paragraph("Merci pour l'échange de lundi. J'ai pris le temps de structurer tout ce que nous avons abordé.", styles['Body']))
story.append(Spacer(1, 8))
story.append(Paragraph("Plutôt qu'un long document, j'ai préparé un <b>dossier de projet complet</b>, accessible en ligne :", styles['Body']))

story.append(Spacer(1, 16))

# Big CTA
cta_data = [[Paragraph(f'<b>👉 Accéder au dossier du projet Florence</b><br/><font size="9" color="#666666">{SITE_URL}</font>', ParagraphStyle('CTA', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=HexColor('#0a75a9'), leading=22))]]
cta = Table(cta_data, colWidths=[14*cm])
cta.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f0f7ff')),
    ('BORDER', (0, 0), (-1, -1), 2, HexColor('#0a75a9')),
    ('TOPPADDING', (0, 0), (-1, -1), 16),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(cta)

story.append(Spacer(1, 8))
story.append(Paragraph("Ce lien est privé et strictement confidentiel. Il n'est pas référencé sur les moteurs de recherche. Seules les personnes disposant du lien peuvent y accéder.", styles['Small']))

story.append(Spacer(1, 20))
hr()

# Sommaire
story.append(Paragraph("Vous y retrouverez :", styles['BodyBold']))
story.append(Spacer(1, 8))

items = [
    ("<b>1. Le contexte</b> — Ma lecture de la situation du groupe IGH et de vos 20 établissements", ""),
    ("<b>2. Les 6 problèmes que vous m'avez exposés</b> — Facturation, obligations admin, courrier, emails, admissions ViaTrajectoire, impayés — tels que vous les avez décrits", ""),
    ("<b>3. Ce que vous attendez</b> — Vos mots, M. Imbert :", ""),
]

for text, _ in items:
    story.append(Paragraph(f"• {text}", styles['BulletItem']))

story.append(Paragraph('« Tous les matins à 10h, un rapport d\'où est-ce qu\'on en est. »', styles['Quote']))

items2 = [
    "<b>4. Pourquoi un collaborateur IA dédié est la bonne réponse</b> — Et ce que ça change concrètement pour vous, pour M. Cozon, et pour vos directeurs",
    "<b>5. Florence, votre collaboratrice</b> — Qui elle est, ses missions, ses compétences — y compris ses connexions aux bases juridiques et réglementaires françaises",
    "<b>6. Concrètement, à quoi ça sert</b> — Le scénario avant/après de votre lundi matin à 10h",
    "<b>7. Le plan de mise en place</b> — Les phases, l'audit terrain par population, comment Florence se construit avec vous dès le premier jour",
    "<b>8. Le budget</b> — Mise en place et abonnement mensuel, avec les avantages coût par rapport à une solution humaine",
]

for text in items2:
    story.append(Paragraph(f"• {text}", styles['BulletItem']))

story.append(Spacer(1, 20))
hr()

# What we need
story.append(Paragraph("<b>De votre côté, pour lancer :</b>", styles['Body']))
story.append(Paragraph("• Vos adresses email", styles['BulletItem']))
story.append(Paragraph("• La liste des 17 EHPAD avec les noms des directeurs", styles['BulletItem']))
story.append(Paragraph("• Le contact de votre DSI / responsable informatique", styles['BulletItem']))
story.append(Paragraph("• 2-3 établissements pilotes", styles['BulletItem']))

story.append(Spacer(1, 12))
story.append(Paragraph("<b>On peut démarrer dans les prochains jours.</b>", styles['Body']))

story.append(Spacer(1, 24))
story.append(Paragraph("Bien cordialement,", styles['Body']))
story.append(Spacer(1, 12))
story.append(Paragraph("<b>Gilles Korzec</b>", styles['Body']))
story.append(Paragraph("Coach Digital Paris", styles['Body']))
story.append(Paragraph("06 52 34 51 80", styles['Body']))

doc.build(story)
print(f"✅ PDF V8 généré : {OUTPUT}")
