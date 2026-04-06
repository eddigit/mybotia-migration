#!/usr/bin/env python3
"""Génère le PDF V9 — version complète avec tous les ajouts"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

OUTPUT = "/home/gilles/.openclaw/workspace/clients/imbert-ehpad/mail-imbert-v9.pdf"

doc = SimpleDocTemplate(OUTPUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm)
styles = getSampleStyleSheet()

# Couleurs IGH
BLEU = '#0a75a9'
BLEU_FONCE = '#0e4b69'
VERT = '#7da144'
GRIS = '#424242'
FOND_CLAIR = '#f5f7fa'

styles.add(ParagraphStyle('H1', parent=styles['Title'], fontSize=16, textColor=HexColor(BLEU), spaceAfter=6, spaceBefore=12))
styles.add(ParagraphStyle('H2', parent=styles['Normal'], fontSize=13, textColor=HexColor(BLEU_FONCE), fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=12))
styles.add(ParagraphStyle('H3', parent=styles['Normal'], fontSize=11, textColor=HexColor(BLEU), fontName='Helvetica-Bold', spaceAfter=4, spaceBefore=8))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, alignment=TA_JUSTIFY, textColor=HexColor(GRIS)))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, fontName='Helvetica-Bold', textColor=HexColor(GRIS)))
styles.add(ParagraphStyle('Quote', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, leftIndent=15, textColor=HexColor(BLEU), fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('BulletCustom', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=3, leftIndent=12, textColor=HexColor(GRIS)))
styles.add(ParagraphStyle('Small', parent=styles['Normal'], fontSize=8, leading=10, textColor=HexColor('#999999'), fontName='Helvetica-Oblique', alignment=TA_CENTER))
styles.add(ParagraphStyle('CTA', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=HexColor(BLEU), fontName='Helvetica-Bold', leading=18))
styles.add(ParagraphStyle('TC', parent=styles['Normal'], fontSize=9, leading=12, textColor=HexColor(GRIS)))
styles.add(ParagraphStyle('TH', parent=styles['Normal'], fontSize=9, leading=12, fontName='Helvetica-Bold', textColor=colors.white))
styles.add(ParagraphStyle('Brand', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'), alignment=TA_CENTER))
styles.add(ParagraphStyle('Slogan', parent=styles['Normal'], fontSize=12, textColor=HexColor(BLEU), fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=10))

story = []

def hr():
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc'), spaceBefore=8, spaceAfter=8))

def section_table(headers, rows, col_widths=None):
    """Create a styled table"""
    if not col_widths:
        col_widths = [5.5*cm] * len(headers)
    
    data = [[Paragraph(h, styles['TH']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles['TC']) for c in row])
    
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor(BLEU)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dddddd')),
    ]))
    return t

# === PAGE 1 — HEADER ===
story.append(Paragraph("COACH DIGITAL PARIS", styles['Brand']))
story.append(Spacer(1, 4))
story.append(Paragraph("Suite à notre réunion du 9 mars", styles['H1']))
story.append(Paragraph("Contexte, plan d'action et Florence, votre future collaboratrice", ParagraphStyle('Sub', parent=styles['Normal'], fontSize=11, textColor=HexColor('#666666'), alignment=TA_CENTER, spaceAfter=16)))

hr()

story.append(Paragraph("Monsieur Imbert, Monsieur Cozon,", styles['Body']))
story.append(Spacer(1, 4))
story.append(Paragraph("Merci pour l'échange de lundi. J'ai pris le temps de structurer tout ce que nous avons abordé, et j'ai été plus loin : j'ai commencé à construire votre future collaboratrice.", styles['Body']))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>J'ai préparé un dossier de projet complet, accessible en ligne :</b>", styles['Body']))

# CTA box
cta_data = [[Paragraph('<b>👉 https://collab-igh.vercel.app/</b><br/><font size="8" color="#666666">Lien privé, non indexé, non connecté à Google</font>', styles['CTA'])]]
cta = Table(cta_data, colWidths=[14*cm])
cta.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f0f7ff')),
    ('BORDER', (0, 0), (-1, -1), 2, HexColor(BLEU)),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
]))
story.append(Spacer(1, 8))
story.append(cta)
story.append(Spacer(1, 12))

# === CONTEXTE ===
story.append(Paragraph("Le contexte", styles['H2']))
story.append(Paragraph("Le groupe IGH gère 20 établissements (17 EHPAD, 3 cliniques) répartis sur le territoire. Le siège à Aix-en-Provence pilote l'ensemble, mais la réalité du terrain remonte mal — ou ne remonte pas.", styles['Body']))

# === PROBLÈMES ===
story.append(Paragraph("Les 6 problèmes que vous m'avez exposés", styles['H2']))

problems = [
    ("<b>1. Pas de visibilité sur la facturation</b>", "80 lits par EHPAD, 80 factures chaque fin de mois. Quand vous appelez un directeur : \"Ah, je ne sais pas.\" Vous voulez arrêter ça."),
    ("<b>2. Les obligations administratives ne sont pas respectées</b>", "Documents pas remplis, deadlines pas tenues. L'inspection du travail débarque, comme à La Rochelle, \"la rage entre les dents\"."),
    ("<b>3. Le courrier est maltraité</b>", "Courriers ARS, CPAM, préfecture — oubliés sur un bureau, pas ouverts, pas traités."),
    ("<b>4. Les emails des établissements ne sont pas suivis</b>", "Emails critiques (convocations, relances) restent sans réponse pendant des jours."),
    ("<b>5. Des admissions sont perdues</b>", "Demandes ViaTrajectoire non traitées à temps. Chaque admission perdue = ~2 500€/mois de séjour en moins."),
    ("<b>6. Les impayés ne sont pas suivis</b>", "Pas de visibilité sur qui a payé. Pas de relances. L'argent traîne."),
]
for title, desc in problems:
    story.append(Paragraph(title, styles['Body']))
    story.append(Paragraph(desc, styles['BulletCustom']))

# === CE QUE VOUS ATTENDEZ ===
story.append(Paragraph("Ce que vous attendez", styles['H2']))
story.append(Paragraph('« Tous les matins à 10h, un rapport d\'où est-ce qu\'on en est. »', styles['Quote']))
story.append(Paragraph('« La condition, c\'est que ce soit simple pour moi. »', styles['Quote']))
story.append(Paragraph('« Cadrer les directeurs et les directrices, gentiment. »', styles['Quote']))

hr()

# === POURQUOI UN COLLABORATEUR IA ===
story.append(Paragraph("Pourquoi un collaborateur IA dédié est la bonne réponse", styles['H2']))
story.append(Paragraph("Vous n'avez pas besoin d'un logiciel de plus. Vous n'avez pas besoin d'un consultant qui vient et repart. Vous avez besoin de quelqu'un qui est là tous les jours, qui connaît vos 20 établissements, et qui ne lâche rien.", styles['Body']))

# SONCAS blocks - condensé
soncas_blocks = [
    ("🔒 Plus jamais de mauvaise surprise", [
        ("Inspection du travail qui débarque", "Alerte 5 jours avant deadline, relance, escalade", "La Rochelle ne serait jamais arrivé"),
        ("Courrier qui dort 3 semaines", "Scan → analyse en secondes : expéditeur, objet, deadline", "Traçabilité complète"),
        ("Emails critiques sans réponse", "Surveillance 24/7 des 17 boîtes mail", "Aucun email ne peut plus dormir"),
    ]),
    ("🏆 Le groupe EHPAD le mieux piloté de France", [
        ("Pilotage par téléphone et estimations", "Dashboard consolidé 20 établissements, chaque jour", "Aucun groupe familial n'a ça"),
        ("Directeurs qui font ce qu'ils veulent", "Actions, deadlines, documents tracés — données objectives", "Dashboard à jour quand l'ARS arrive"),
    ]),
    ("💰 Chaque euro compte", [
        ("1 amende inspection évitée", "Contrôle des deadlines", "5 000 à 50 000€ économisés"),
        ("5 admissions récupérées/an", "Détection temps réel ViaTrajectoire", "~150 000€/an de CA"),
        ("Impayés qui traînent", "Relances systématiques dès J+1", "Trésorerie améliorée"),
    ]),
]

for title, rows in soncas_blocks:
    story.append(Paragraph(title, styles['Slogan']))
    t = section_table(
        ["Votre problème", "Ce que Florence fait", "Impact / Preuve"],
        rows,
        col_widths=[5.5*cm, 5.5*cm, 5.5*cm]
    )
    story.append(t)
    story.append(Spacer(1, 4))

story.append(PageBreak())

# === FLORENCE ===
story.append(Paragraph("Florence — Votre collaboratrice dédiée", styles['H1']))
story.append(Paragraph("En hommage à Florence Nightingale (1820-1910), pionnière des soins infirmiers modernes et inventrice du premier tableau de bord hospitalier.", styles['Body']))
story.append(Paragraph("Florence n'est pas un logiciel. C'est une collaboratrice qui apprend, raisonne, alerte et s'adapte. Elle connaît chaque établissement, chaque directeur, chaque échéance. Elle ne dort jamais, n'oublie rien, et ne lâche rien.", styles['Body']))

story.append(Paragraph("Ses 5 missions quotidiennes", styles['H3']))
missions = [
    ("📊 Pilotage financier", "Rapport du matin à 10h : occupation, facturation, impayés — les 20 établissements"),
    ("📋 Conformité réglementaire", "Calendrier de TOUTES les obligations. Alertes 5j avant, relances, escalades"),
    ("✉️ Gestion flux entrants", "Surveillance 24/7 des 17 boîtes emails + analyse courrier scanné"),
    ("🚪 Admissions ViaTrajectoire", "Détection temps réel des demandes. Relance directeur si non traité sous 24h"),
    ("👥 Coordination directeurs", "Rappels personnalisés, relances bienveillantes, escalade à M. Cozon"),
]
for emoji_title, desc in missions:
    story.append(Paragraph(f"<b>{emoji_title}</b> — {desc}", styles['BulletCustom']))

story.append(Paragraph("Ses compétences connectées aux sources officielles", styles['H3']))
t = section_table(
    ["Source", "Ce que Florence peut faire"],
    [
        ("Légifrance", "Code santé publique, CASF, Code du travail — l'article de loi en quelques secondes"),
        ("Judilibre", "Jurisprudence Cour de cassation — décisions prud'homales, contentieux ARS"),
        ("BODACC", "Surveillance procédures collectives de vos fournisseurs"),
        ("FINESS", "Données officielles de vos 20 établissements ET de vos concurrents"),
        ("Conventions collectives", "CCN EHPAD privés (IDCC 2264) — grilles, droits, obligations"),
        ("BOAMP", "Veille marchés publics médico-sociaux — appels d'offres ARS"),
    ],
    col_widths=[4*cm, 12.5*cm]
)
story.append(t)

# Sécurité
story.append(Paragraph("Sécurité & RGPD", styles['H3']))
secu_items = [
    "• Aucun accès aux données médicales — jamais",
    "• Hébergement 100% en France",
    "• Effacement automatique après 30 jours (sauf facturation : 3 ans)",
    "• Chiffrement de bout en bout — accès restreint au COPIL",
]
for item in secu_items:
    story.append(Paragraph(item, styles['BulletCustom']))

hr()

# === CONCRÈTEMENT ===
story.append(Paragraph("Concrètement, à quoi ça sert ?", styles['H2']))
story.append(Paragraph("<b>Le lundi matin, 10h. Aujourd'hui :</b>", styles['Body']))
story.append(Paragraph("Vous appelez La Rochelle. Pas de réponse. Vous appelez Aix. Le directeur cherche ses chiffres. 45 minutes pour 2 établissements sur 17. Pour les 15 autres, vous espérez.", styles['Body']))

story.append(Paragraph("<b>Le lundi matin, 10h. Avec Florence :</b>", styles['Body']))
story.append(Paragraph("Vous ouvrez WhatsApp. Le rapport est là. 17 EHPAD : taux d'occupation, facturation, impayés, obligations admin, admissions ViaTrajectoire, courrier analysé. Vous n'avez appelé personne. Vous savez tout. En 3 minutes.", styles['Body']))

# Tableau avant/après
t = section_table(
    ["Sans Florence", "Avec Florence"],
    [
        ("Vous appelez, personne ne sait", "Vous ouvrez WhatsApp, tout est là"),
        ("Documents en retard → amende", "Alerte 5 jours avant, relance, escalade"),
        ("Courrier ARS dort 3 semaines", "Scanné, analysé, deadline le jour même"),
        ("Admissions passent inaperçues", "Détectées en temps réel, directeur relancé"),
        ("Impayés traînent des mois", "Relances systématiques, suivi au centime"),
        ("M. Cozon au téléphone toute la journée", "Il gère uniquement les exceptions"),
    ],
    col_widths=[8.25*cm, 8.25*cm]
)
story.append(t)

story.append(PageBreak())

# === MISE EN PLACE ===
story.append(Paragraph("Comment ça se passe concrètement", styles['H2']))
story.append(Paragraph("<b>Florence est là dès le premier jour.</b> Elle ne sort pas d'un carton à la fin du projet. Elle est dans la pièce avec nous dès le départ.", styles['Body']))

# Équipe
story.append(Paragraph("Jour 0 — L'équipe de démarrage", styles['H3']))
t = section_table(
    ["Membre", "Rôle"],
    [
        ("M. Imbert", "Direction, validation, orientations stratégiques"),
        ("M. Cozon", "Opérationnel, connaissance terrain, priorités"),
        ("Gilles Korzec", "Architecte de la solution, audit, formation"),
        ("Léa", "Admin, juridique, suivi projet, recherches API"),
        ("Florence", "Votre nouvelle collaboratrice — elle apprend, elle grandit avec vous"),
    ],
    col_widths=[4.5*cm, 12*cm]
)
story.append(t)

# Audit
story.append(Paragraph("L'audit terrain — Florence est dedans", styles['H3']))
t = section_table(
    ["Demi-journée", "Ce qui se passe", "Florence en parallèle"],
    [
        ("J1 matin — Direction", "Cycle de facturation, obligations, relations siège", "Synthèse le soir. Vous corrigez, elle apprend."),
        ("J1 après-midi — DSI", "Systèmes : Titan, emails, ViaTrajectoire", "Identifie connexions possibles, points de blocage"),
        ("J2 matin — EHPAD pilote 1", "Quotidien d'un directeur sur le terrain", "Structure les alertes adaptées à CET établissement"),
        ("J2 après-midi — EHPAD pilote 2", "Comparaison, différences", "Ajuste. Deux réalités, un cadre. Vue consolidée."),
    ],
    col_widths=[3.5*cm, 6*cm, 7*cm]
)
story.append(t)

hr()

# === BONUS SITE ===
story.append(Paragraph("Refonte de votre site web i-g-h.fr — 1 490€ HT", styles['H2']))
story.append(Paragraph("En complément du projet Florence, nous vous proposons <b>la refonte complète de votre site web</b>.", styles['Body']))
story.append(Paragraph("Votre site actuel date de 2018. Pour un groupe de 20 établissements, vous méritez un site à la hauteur :", styles['Body']))

site_items = [
    "• Design moderne, mobile-first, lisible",
    "• Carte interactive de vos 20 établissements",
    "• Fiches individuelles : photos, capacité, services, contact, demande de visite",
    "• Espace Familles : guide EHPAD, aides financières (APA, ASH, APL), témoignages",
    "• Espace Recrutement attractif : fiches métiers, offres par région, candidature en 1 clic",
    "• Chatbot Florence intégré — les familles peuvent poser leurs questions 24/7",
    "• SEO optimisé : visible sur \"EHPAD + ville\" pour chaque établissement",
    "• Accessible (contrastes élevés, textes lisibles) — vos visiteurs sont souvent des personnes âgées",
    "• Conforme RGPD",
]
for item in site_items:
    story.append(Paragraph(item, styles['BulletCustom']))

story.append(Paragraph("Le cahier des charges détaillé est prêt. Nous utilisons vos couleurs (bleu, vert, sarcelle) et vos 5 valeurs : Accueillir, Accompagner, Soigner, Protéger, Respecter.", styles['Body']))

hr()

# === POSSIBILITÉS SUPPLÉMENTAIRES ===
story.append(Paragraph("Ce que Florence peut vous apporter en plus", styles['H2']))
extras = [
    ("Accueil téléphonique IA", "Prendre les appels, répondre aux questions fréquentes, transférer les urgences"),
    ("Formulaires wizard", "Champs obligatoires, données structurées. Fini les \"euh euh euh\""),
    ("Veille concurrentielle", "Surveillance concurrents : nouveaux EHPAD, procédures collectives, marchés publics"),
    ("Aide à l'acquisition", "Fiche FINESS + bilans + BODACC + obligations réglementaires en 2 minutes"),
    ("Reporting mensuel", "Synthèse consolidée : KPIs, tendances, alertes, recommandations"),
]
for title, desc in extras:
    story.append(Paragraph(f"• <b>{title}</b> — {desc}", styles['BulletCustom']))

story.append(PageBreak())

# === BUDGET ===
story.append(Paragraph("Le budget", styles['H1']))

story.append(Paragraph("Mise en place : 7 680€ HT", styles['H2']))
t = section_table(
    ["Phase", "Jours", "Total HT"],
    [
        ("Phase 0 — Cadrage + Naissance Florence", "—", "Offert"),
        ("Phase 1 — Audit terrain (4 demi-journées)", "2", "1 280€"),
        ("Phase 1B — Analyse + Construction Florence", "4", "2 560€"),
        ("Phase 2 — Intégration technique", "4", "2 560€"),
        ("Phase 3 — Pilote + Formation (2 EHPAD)", "2", "1 280€"),
        ("TOTAL", "12 jours", "7 680€ HT"),
    ],
    col_widths=[8.5*cm, 3*cm, 5*cm]
)
story.append(t)
story.append(Spacer(1, 4))
story.append(Paragraph("Tarif journalier : 640€ HT — déplacements inclus.", styles['Body']))
story.append(Paragraph("<b>Refonte site web i-g-h.fr : 1 490€ HT</b> (en complément, si vous partez sur la globalité)", styles['BodyBold']))

story.append(Paragraph("Abonnement mensuel : 216€ HT / mois / établissement", styles['H2']))
t = section_table(
    ["Périmètre", "Établissements", "/mois HT", "/an HT"],
    [
        ("Phase pilote", "3", "648€", "7 776€"),
        ("Déploiement partiel", "10", "2 160€", "25 920€"),
        ("Déploiement complet", "20", "4 320€", "51 840€"),
    ],
    col_widths=[5*cm, 3.5*cm, 4*cm, 4*cm]
)
story.append(t)

story.append(Paragraph("Avantage coût", styles['H3']))
t = section_table(
    ["", "Florence", "Assistante humaine"],
    [
        ("Coût annuel (20 étab.)", "51 840€", "~70 000€ (salaire chargé)"),
        ("Disponibilité", "24/7, 365 jours", "35h/semaine, congés"),
        ("Couverture", "20 établissements", "3-4 max"),
        ("Surveillance 17 boîtes mail", "Automatique", "Impossible"),
        ("Compétences juridiques", "Légifrance, jurisprudence temps réel", "Pas de formation juridique"),
        ("Oubli", "Jamais", "Humain"),
    ],
    col_widths=[5*cm, 5.75*cm, 5.75*cm]
)
story.append(t)

story.append(Spacer(1, 8))
story.append(Paragraph("<b>216€/mois pour un EHPAD de 80 lits = 2,70€ par lit par mois.</b>", styles['BodyBold']))
story.append(Paragraph("<b>1 seule admission ViaTrajectoire sauvée = 2 500€/mois</b> → Florence se rembourse 12 fois.", styles['BodyBold']))

story.append(Spacer(1, 8))
# Récapitulatif global
story.append(Spacer(1, 4))
t_recap = section_table(
    ["Poste", "Montant HT"],
    [
        ("Mise en place Florence (12 jours)", "7 680€"),
        ("Refonte site web i-g-h.fr", "1 490€"),
        ("TOTAL", "9 170€ HT"),
    ],
    col_widths=[10*cm, 6.5*cm]
)
story.append(t_recap)
story.append(Spacer(1, 8))
story.append(Paragraph("Conditions de règlement : 50% à la signature (4 585€ HT) — 50% à la validation du pilote (4 585€ HT)", styles['Body']))

hr()

# === POUR LANCER ===
story.append(Paragraph("De votre côté, pour lancer", styles['H2']))
story.append(Paragraph("• La liste des 17 EHPAD avec les noms des directeurs", styles['BulletCustom']))
story.append(Paragraph("• Le contact de votre DSI / responsable informatique", styles['BulletCustom']))
story.append(Paragraph("• 2-3 établissements pilotes (ceux qui posent le plus de problèmes)", styles['BulletCustom']))

story.append(Spacer(1, 8))
story.append(Paragraph("<b>Florence peut être opérationnelle dans les prochains jours.</b>", styles['BodyBold']))

story.append(Spacer(1, 20))
story.append(Paragraph("Bien cordialement,", styles['Body']))
story.append(Spacer(1, 8))
story.append(Paragraph("<b>Gilles Korzec</b>", styles['Body']))
story.append(Paragraph("Coach Digital Paris", styles['Body']))
story.append(Paragraph("06 52 34 51 80", styles['Body']))

story.append(Spacer(1, 16))
hr()
story.append(Paragraph("Dossier complet en ligne : https://collab-igh.vercel.app/", styles['Small']))
story.append(Paragraph("Lien privé, non indexé, non connecté à Google.", styles['Small']))

doc.build(story)
print(f"✅ PDF V9 généré : {OUTPUT}")
