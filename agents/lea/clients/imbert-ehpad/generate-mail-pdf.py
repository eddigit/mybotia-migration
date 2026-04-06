#!/usr/bin/env python3
"""Génère le PDF complet du mail V7 Imbert/IGH"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

OUTPUT = "/home/gilles/.openclaw/workspace/clients/imbert-ehpad/mail-imbert-v7-complet.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm
)

styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(
    'MailTitle', parent=styles['Title'],
    fontSize=16, textColor=HexColor('#1a1a2e'),
    spaceAfter=6
))
styles.add(ParagraphStyle(
    'MailH2', parent=styles['Heading2'],
    fontSize=14, textColor=HexColor('#2c3e50'),
    spaceBefore=18, spaceAfter=8,
    borderWidth=0, borderPadding=0
))
styles.add(ParagraphStyle(
    'MailH3', parent=styles['Heading3'],
    fontSize=12, textColor=HexColor('#2980b9'),
    spaceBefore=14, spaceAfter=6
))
styles.add(ParagraphStyle(
    'MailBody', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=6,
    alignment=TA_JUSTIFY
))
styles.add(ParagraphStyle(
    'MailBodyBold', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=6,
    alignment=TA_JUSTIFY
))
styles.add(ParagraphStyle(
    'Quote', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=4,
    leftIndent=20, textColor=HexColor('#555555'),
    fontName='Helvetica-Oblique'
))
styles.add(ParagraphStyle(
    'SmallNote', parent=styles['Normal'],
    fontSize=8, leading=11, spaceAfter=4,
    textColor=HexColor('#888888'),
    fontName='Helvetica-Oblique'
))
styles.add(ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontSize=8.5, leading=11, spaceAfter=0
))
styles.add(ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontSize=8.5, leading=11, spaceAfter=0,
    fontName='Helvetica-Bold', textColor=colors.white
))
styles.add(ParagraphStyle(
    'BulletItem', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=3,
    leftIndent=15, bulletIndent=5
))

story = []

def add_header(text, level=2):
    if level == 1:
        story.append(Paragraph(text, styles['MailTitle']))
    elif level == 2:
        story.append(Paragraph(text, styles['MailH2']))
    else:
        story.append(Paragraph(text, styles['MailH3']))

def add_text(text):
    story.append(Paragraph(text, styles['MailBody']))

def add_bold(text):
    story.append(Paragraph(f"<b>{text}</b>", styles['MailBody']))

def add_quote(text):
    story.append(Paragraph(f"<i>« {text} »</i>", styles['Quote']))

def add_bullet(text):
    story.append(Paragraph(f"• {text}", styles['BulletItem']))

def add_spacer(h=6):
    story.append(Spacer(1, h))

def add_hr():
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#cccccc'), spaceBefore=8, spaceAfter=8))

def make_table(headers, rows, col_widths=None):
    """Create a styled table"""
    w = col_widths or [5.5*cm, 5.5*cm, 5.5*cm]
    data = [[Paragraph(h, styles['TableHeader']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])
    
    t = Table(data, colWidths=w)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f2f2f2')]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dddddd')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    add_spacer(8)

def make_simple_table(headers, rows, col_widths=None):
    """Simple 2-col table"""
    w = col_widths or [8*cm, 8.5*cm]
    data = [[Paragraph(h, styles['TableHeader']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])
    
    t = Table(data, colWidths=w)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f2f2f2')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    add_spacer(8)


# ============================================================
# MAIL CONTENT
# ============================================================

# Header
story.append(Paragraph("COACH DIGITAL PARIS", ParagraphStyle('Brand', parent=styles['Normal'], fontSize=8, textColor=HexColor('#999999'), alignment=TA_CENTER)))
add_spacer(4)
add_header("Suite à notre réunion du 9 mars", 1)
story.append(Paragraph("Contexte, plan d'action et votre futur collaborateur", ParagraphStyle('Sub', parent=styles['Normal'], fontSize=12, textColor=HexColor('#666666'), alignment=TA_CENTER)))
add_spacer(12)

add_hr()
add_text("Monsieur Imbert, Monsieur Cozon,")
add_spacer(4)
add_text("Merci pour l'échange de lundi. Voici ma lecture de la situation et ce que je vous propose.")
add_hr()

# ---- CONTEXTE ----
add_header("Le contexte")
add_text("Le groupe IGH gère 20 établissements (17 EHPAD, 3 cliniques) répartis sur le territoire. Le siège à Aix-en-Provence pilote l'ensemble, mais la réalité du terrain remonte mal — ou ne remonte pas.")

# ---- PROBLEMES ----
add_header("Les problèmes que vous m'avez exposés")

add_bold("1. Pas de visibilité sur la facturation")
add_text("80 lits par EHPAD, 80 factures chaque fin de mois, émises le 20, payables avant le 5 du mois suivant. Quand vous appelez un directeur pour savoir combien il a encaissé, la réponse c'est : <i>« Ah, je ne sais pas. »</i> Vous voulez arrêter ça.")

add_bold("2. Les obligations administratives ne sont pas respectées")
add_text("Documents à remplir, deadlines à tenir, signalements à faire. Les directeurs ne le font pas — ou pas à temps. Résultat : l'inspection du travail débarque, comme à La Rochelle, <i>« la rage entre les dents »</i>. Des PV, des amendes, des problèmes évitables.")

add_bold("3. Le courrier est maltraité")
add_text("Des courriers physiques arrivent dans les établissements — ARS, CPAM, préfecture, inspection du travail. Ils sont oubliés sur un bureau, pas ouverts, pas traités. Quand vous le découvrez, c'est souvent trop tard.")

add_bold("4. Les emails des établissements ne sont pas suivis")
add_text("Les boîtes mail des EHPAD reçoivent des messages importants — convocations, demandes d'information, relances administratives. Personne ne les surveille de manière systématique. Des emails critiques restent sans réponse pendant des jours, voire des semaines.")

add_bold("5. Des admissions sont perdues")
add_text("Les demandes de placement arrivent via ViaTrajectoire. C'est le plus réactif qui emporte le morceau. Certains directeurs ne traitent pas les dossiers à temps. Chaque admission perdue, c'est ~2 500€/mois de séjour en moins.")

add_bold("6. Les impayés ne sont pas suivis")
add_text("Pas de visibilité claire sur qui a payé et qui n'a pas payé. Pas de relances systématiques. L'argent traîne.")

# ---- CE QUE VOUS ATTENDEZ ----
add_header("Ce que vous attendez")
add_text("M. Imbert, vous l'avez résumé simplement :")
add_quote("Tous les matins à 10h, un rapport d'où est-ce qu'on en est.")
add_quote("La condition, c'est que ce soit simple pour moi.")
add_quote("Cadrer les directeurs et les directrices, gentiment.")

add_hr()

# ---- POURQUOI UN COLLABORATEUR IA ----
add_header("Pourquoi un collaborateur IA dédié est la bonne réponse")
add_text("Vous n'avez pas besoin d'un logiciel de plus. Vous n'avez pas besoin d'un consultant qui vient, fait un rapport, et repart. Vous avez besoin de quelqu'un qui est là tous les jours, qui connaît vos 20 établissements, et qui ne lâche rien.")
add_text("Voici pourquoi cette approche répond à chacune de vos préoccupations :")

add_hr()

# ---- SONCAS 1 : SECURITE ----
add_header("🔒 Plus jamais de mauvaise surprise", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "La preuve"],
    [
        ["L'inspection du travail débarque parce qu'un directeur a oublié un document",
         "Il connaît chaque deadline réglementaire de chaque établissement. Il alerte 5 jours avant, relance 2 jours avant, et vous prévient si ce n'est pas fait.",
         "L'EHPAD de La Rochelle ne vous aurait jamais valu cette visite — le collaborateur aurait détecté le retard et escaladé avant la deadline"],
        ["Un courrier de la préfecture dort sur un bureau pendant 3 semaines",
         "Le directeur le photographie, le collaborateur l'analyse en quelques secondes : expéditeur, objet, deadline, urgence. Rien ne passe entre les mailles.",
         "Traçabilité complète : vous savez quel courrier est arrivé où, quand, et s'il a été traité"],
        ["Des emails critiques (ARS, CPAM) restent sans réponse",
         "Il surveille les boîtes mail de chaque établissement 24/7. Email urgent non traité depuis 3 jours ? Alerte automatique.",
         "Aucun email ne peut plus « dormir » sans que vous le sachiez"],
        ["Données sensibles — le RGPD",
         "Aucun accès aux données médicales. Hébergement 100% en France, local si vous le souhaitez. Effacement automatique après 30 jours (sauf facturation : 3 ans).",
         "M. Cozon le sait : en tant qu'ancien référent RGPD, il pourra vérifier lui-même la conformité de l'architecture"],
    ]
)
add_bold("→ Vous dormez tranquille. Plus de mauvaise surprise.")

# ---- SONCAS 2 : ORGUEIL ----
add_header("🏆 Le groupe EHPAD le mieux piloté de France", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "La preuve"],
    [
        ["Aujourd'hui, le pilotage du groupe repose sur des coups de téléphone et des estimations",
         "Demain, vous avez un tableau de bord consolidé de 20 établissements, mis à jour chaque jour, accessible depuis votre téléphone",
         "Aucun autre groupe EHPAD familial de cette taille n'a ça aujourd'hui"],
        ["Les directeurs font ce qu'ils veulent",
         "Chaque action, chaque deadline, chaque document est tracé. Vous avez les données objectives pour vos réunions. Pas des « je crois que… »",
         "Quand vous recevez l'ARS ou l'inspection, vous ouvrez votre dashboard : tout est à jour, preuves à l'appui"],
    ]
)
add_bold("→ IGH devient le groupe EHPAD familial le mieux piloté de France.")

# ---- SONCAS 3 : NOUVEAUTE ----
add_header("✨ Une longueur d'avance sur vos concurrents", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "La preuve"],
    [
        ["« On a toujours fait comme ça » — appeler, relancer à la main, espérer que ce soit fait",
         "Le collaborateur IA est une rupture : il comprend un document, il sait poser les bonnes questions, il sait relancer au bon moment. Ce n'est pas un logiciel qu'on remplit — c'est un collaborateur qui agit.",
         "Vous le verrez dès le premier jour dans le groupe WhatsApp : il pose des questions intelligentes, il retient tout, il s'adapte à votre façon de travailler"],
        ["ViaTrajectoire : les demandes d'admission passent inaperçues",
         "Le collaborateur détecte chaque nouvelle demande en temps réel et alerte le directeur concerné. Plus rapide que n'importe quel humain.",
         "Le groupe le plus réactif emporte l'admission. Avec ce collaborateur, c'est toujours vous."],
    ]
)
add_bold("→ Vous prenez une avance que vos concurrents n'ont pas.")

# ---- SONCAS 4 : CONFORT ----
add_header("🛋️ Vous pilotez, il exécute", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "La preuve"],
    [
        ["Appeler 17 directeurs un par un pour avoir des chiffres",
         "1 rapport à 10h, tous les matins, automatique. Vous ouvrez, vous savez.",
         "Zéro appel, zéro relance, zéro « je te rappelle »"],
        ["Courir après les directeurs pour savoir si le boulot est fait",
         "Le collaborateur court pour vous. Il relance, il escalade, il trace.",
         "Vous ne gérez que les exceptions. Le reste est automatique."],
        ["« C'est compliqué, il faut se former »",
         "WhatsApp. Le directeur sait déjà l'utiliser. Zéro installation, zéro formation lourde.",
         "Votre collaborateur parle en français, sur WhatsApp, comme un collègue."],
    ]
)
add_bold("→ M. Cozon récupère des heures chaque semaine. M. Imbert a la tranquillité d'esprit.")

# ---- SONCAS 5 : ARGENT ----
add_header("💰 Chaque euro compte — voici les chiffres", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "L'impact financier"],
    [
        ["1 amende d'inspection du travail",
         "Évitée grâce au contrôle des deadlines",
         "5 000 à 50 000€ économisés par incident"],
        ["1 admission perdue via ViaTrajectoire",
         "Récupérée grâce à la détection en temps réel",
         "~2 500€/mois de revenus par admission"],
        ["5 admissions récupérées par an sur le groupe",
         "",
         "~150 000€/an de CA supplémentaire"],
        ["Impayés qui traînent 3-6 mois",
         "Relances systématiques dès le 1er retard",
         "Trésorerie améliorée immédiatement"],
        ["Temps de M. Cozon passé au téléphone",
         "Libéré pour des tâches à valeur ajoutée",
         "Le DG pilote au lieu de courir"],
    ]
)
add_bold("→ L'investissement est récupéré dès les premiers mois.")

# ---- SONCAS 6 : SYMPATHIE ----
add_header("🤝 Un collaborateur, pas un logiciel", 3)
make_table(
    ["Votre problème", "Ce que le collaborateur fait", "La preuve"],
    [
        ["« Encore un outil informatique que personne ne va utiliser »",
         "Ce n'est pas un outil. C'est un collaborateur. Il a un prénom, que vous choisissez. Il apprend votre vocabulaire, vos habitudes.",
         "Dès le premier jour dans le groupe WhatsApp, vous verrez : il parle comme un collègue, pas comme une machine"],
        ["Les directeurs vont résister au changement",
         "Le collaborateur ne les remplace pas, il les aide. Il leur rappelle gentiment. C'est un allié, pas un contrôleur.",
         "« Cadrer les directeurs, gentiment » — c'est exactement ce qu'il fait"],
        ["Gilles et Léa, on les connaît à peine",
         "Gilles est sur le terrain avec vous pendant l'audit. Léa est dans le groupe WhatsApp. Vous avez une équipe dédiée, joignable, réactive.",
         "Pas un prestataire lointain. Une équipe engagée."],
    ]
)
add_bold("→ C'est un partenariat, pas un contrat de prestation.")

add_hr()

# ---- CONCRETEMENT A QUOI CA SERT ----
add_header("Concrètement, à quoi ça sert ?")

add_text("M. Imbert, vous avez posé la question à M. Cozon pendant la réunion : <i>« À quoi ça va nous servir ? »</i>")
add_text("Voici la réponse, sans détour.")
add_spacer(6)

add_bold("Le lundi matin, 10h. Aujourd'hui :")
add_text("Vous décrochez le téléphone. Vous appelez La Rochelle. Pas de réponse. Vous appelez Aix. Le directeur cherche ses chiffres. Vous rappelez La Rochelle. On vous dit « je crois que c'est bon ». Vous raccrochez sans savoir si c'est vrai. Vous avez passé 45 minutes et vous n'avez couvert que 2 établissements sur 17. Pour les 15 autres, vous espérez que ça tourne.")
add_spacer(6)

add_bold("Le lundi matin, 10h. Avec votre collaborateur :")
add_text("Vous ouvrez WhatsApp. Le rapport est là. Les 17 EHPAD. Pour chacun :")
add_bullet("Taux d'occupation : 92%, 87%, 78%…")
add_bullet("Facturation du mois : émise / en attente / en retard")
add_bullet("Impayés : 3 familles en retard de plus de 30 jours (noms, montants, relances déjà envoyées)")
add_bullet("Obligations admin : 2 documents à rendre cette semaine — les directeurs ont été alertés, l'un a déjà soumis, l'autre pas encore")
add_bullet("Admissions : 4 demandes ViaTrajectoire reçues hier, 3 traitées, 1 en attente de réponse depuis 48h — le directeur a été relancé ce matin")
add_bullet("Courrier : un recommandé ARS reçu vendredi à Béziers, scanné par le directeur, analysé — demande de mise en conformité, deadline dans 15 jours")

add_text("Vous n'avez appelé personne. Vous savez tout. <b>En 3 minutes.</b>")
add_spacer(6)

add_bold("Et si quelque chose ne va pas ?")
add_text("Vous n'attendez pas lundi. Le collaborateur vous alerte en temps réel :")
add_bullet("<i>« M. Imbert, l'EHPAD de Grenoble n'a pas soumis le document CPAM dû demain. Le directeur n'a pas répondu à ma relance de ce matin. Voulez-vous que M. Cozon l'appelle ? »</i>")
add_bullet("<i>« Nouvelle demande d'admission ViaTrajectoire pour l'EHPAD de Marseille. Le directeur n'a pas consulté le dossier depuis 24h. Je relance. »</i>")
add_bullet("<i>« Alerte : 12 factures non encaissées à plus de 45 jours sur l'EHPAD d'Aix. Montant total : 34 200€. Relances individuelles envoyées aux familles. »</i>")
add_spacer(6)

add_bold("Ce que ça change pour M. Cozon :")
add_text("Au lieu de passer ses journées au téléphone à relancer les directeurs, il reçoit chaque matin la liste de ce qui ne va pas — et uniquement ce qui ne va pas. Il intervient sur les exceptions. Le reste est géré. Il passe de pompier à pilote.")

add_bold("Ce que ça change pour M. Imbert :")
add_text("Vous avez la vision complète de vos 20 établissements depuis votre téléphone. Pas de surprise. Pas de « je savais pas ». Quand l'ARS vous appelle, vous avez la réponse avant même de décrocher.")

add_bold("Ce que ça change pour les directeurs :")
add_text("Ils ne sont pas fliqués — ils sont accompagnés. Le collaborateur leur rappelle leurs obligations, les aide à ne rien oublier, et leur enlève de la charge mentale. Un directeur qui sait que rien ne passe entre les mailles travaille plus sereinement.")
add_spacer(6)

# Tableau comparatif
make_simple_table(
    ["Sans le collaborateur", "Avec le collaborateur"],
    [
        ["Vous appelez, personne ne sait", "Vous ouvrez WhatsApp, tout est là"],
        ["Les documents sont en retard, vous l'apprenez après l'amende", "Il alerte 5 jours avant, relance, escalade"],
        ["Un courrier ARS dort 3 semaines", "Scanné, analysé, deadline identifiée le jour même"],
        ["Des admissions passent inaperçues", "Détectées en temps réel, directeur relancé automatiquement"],
        ["Les impayés traînent des mois", "Relances systématiques, suivi au centime près"],
        ["M. Cozon passe ses journées au téléphone", "Il gère uniquement les exceptions"],
        ["Vous espérez que ça tourne", "<b>Vous savez que ça tourne — et quand ça ne tourne pas, vous le savez aussi</b>"],
    ]
)

add_hr()

# ---- COMMENT CA SE PASSE ----
add_header("Comment ça se passe concrètement")
add_text("Ce qui change par rapport à une approche classique : <b>votre collaborateur IA est là dès le premier jour.</b> Il ne sort pas d'un carton à la fin du projet. Il est dans la pièce avec nous dès le départ.")

add_hr()

add_bold("Jour 0 — On constitue l'équipe et votre collaborateur naît")
add_text("Dès votre accord, on crée l'équipe de démarrage :")

make_simple_table(
    ["Membre", "Rôle"],
    [
        ["<b>M. Imbert</b>", "Direction, validation, orientations stratégiques"],
        ["<b>M. Cozon</b>", "Opérationnel, connaissance terrain, priorités"],
        ["<b>Gilles Korzec</b>", "Architecte de la solution, audit, formation"],
        ["<b>Léa</b>", "Admin, juridique, suivi projet, recherches API*"],
        ["<b>Votre collaborateur IGH</b>", "Le nouveau — vous choisissez son prénom"],
    ],
    col_widths=[5*cm, 11.5*cm]
)

add_text("Groupe WhatsApp créé avec cette équipe. Votre collaborateur se présente, fait connaissance. M. Imbert et M. Cozon peuvent déjà lui parler, lui expliquer leur quotidien, lui poser des questions. Il écoute, il retient, il commence à comprendre votre groupe.")
add_bold("Dès ce moment, vous êtes dans la dynamique. Vous voyez ce que c'est, concrètement.")

add_spacer(10)
add_bold("L'audit terrain — Votre collaborateur est dedans, pas derrière")
add_text("Il ne s'agit pas de faire un audit puis de revenir 3 semaines plus tard avec un livrable. Votre collaborateur participe à chaque étape, en temps réel.")

# Audit table - 3 colonnes
make_table(
    ["Jour terrain", "Ce qui se passe", "Ce que le collaborateur fait en parallèle"],
    [
        ["<b>Jour 1 — Siège Aix</b> avec M. Imbert + M. Cozon",
         "On décortique le fonctionnement du groupe : cycle de facturation, obligations admin, relations siège-établissements",
         "Il enregistre tout. Le soir même, il vous envoie dans le groupe une synthèse structurée de ce qu'il a compris. Vous corrigez, vous complétez. Il apprend."],
        ["<b>Jour 2 — DSI / Responsable informatique</b>",
         "On cartographie les systèmes : Titan, boîtes emails des établissements, ViaTrajectoire, accès réseau",
         "Il commence à raisonner sur les connexions possibles. Il identifie les données accessibles, les points de blocage, et propose des pistes. Vous voyez sa réflexion en temps réel dans le groupe."],
        ["<b>Jour 3 — Un EHPAD sur le terrain</b>",
         "On voit le quotidien d'un directeur : comment il utilise Titan, gère le courrier, les emails, les admissions",
         "Il comprend la réalité du terrain. Il commence à structurer les alertes, les relances, les contrôles adaptés à CE directeur, CET établissement."],
        ["<b>Jour 4 — Second établissement</b>",
         "On compare, on voit les différences entre deux réalités",
         "Il ajuste. Deux EHPAD, deux réalités, mais un même cadre. Il construit une approche qui s'adapte à chaque établissement tout en gardant une vue consolidée pour le siège."],
    ]
)

add_text("Après chaque journée terrain, <b>deux jours en atelier</b> :")
add_bullet("<b>1 jour d'analyse</b> — structurer ce qui a été capté sur le terrain")
add_bullet("<b>1 jour de construction</b> — alimenter le cerveau du collaborateur, créer sa mémoire, configurer ses connaissances sur vos établissements, vos cycles, vos directeurs")

add_spacer(8)
add_bold("Ce que M. Imbert et M. Cozon voient pendant tout ce processus :")
add_text("Chaque soir, dans le groupe WhatsApp, le collaborateur partage :")
add_bullet("Ce qu'il a compris de la journée")
add_bullet("Les problèmes qu'il a identifiés")
add_bullet("Les solutions qu'il commence à construire")
add_bullet("Ses questions — parce qu'un bon collaborateur pose des questions")

add_text("Vous n'êtes pas spectateurs. Vous corrigez, vous orientez, vous apportez votre pierre. Le collaborateur se construit AVEC vous, pas dans un bureau loin de vous.")

add_spacer(8)
add_bold("Au terme de ces 12 jours, ce n'est pas un prototype qu'on vous livre — c'est un collaborateur qui connaît déjà votre groupe, qui a déjà raisonné sur vos problèmes, et qui est prêt à travailler.")

add_spacer(8)
add_bold("4 jours terrain + 8 jours atelier = 12 jours × 800€ HT = 9 600€ HT")

add_hr()

# ---- PHASE 2 et 3 ----
add_bold("Phase 2 — Connexion aux outils du groupe")
add_text("Le collaborateur est prêt, maintenant on le branche :")
add_bullet("<b>Titan/TitanLink</b> → il lit les données de facturation, lits, encaissements")
add_bullet("<b>Boîtes emails des 17 EHPAD</b> → il surveille, détecte, alerte")
add_bullet("<b>ViaTrajectoire</b> → il capte les demandes d'admission en temps réel")
add_bullet("<b>Rapport du matin</b> → il consolide tout, chaque jour à 10h")

add_spacer(6)
add_bold("Phase 3 — Démo puis déploiement")
add_text("Démo avec vos vrais établissements, vos vrais chiffres. Puis 2-3 EHPAD pilotes, puis les 20.")

add_hr()

# ---- CE QU'ON DEMANDE ----
add_bold("De votre côté, pour lancer :")
add_bullet("Vos adresses email")
add_bullet("La liste des 17 EHPAD avec les noms des directeurs")
add_bullet("Le contact de votre DSI / responsable informatique")
add_bullet("2-3 établissements pilotes (ceux qui posent le plus de problèmes)")

add_spacer(6)
add_bold("On peut démarrer cette semaine.")

add_spacer(16)
add_text("Bien cordialement,")
add_spacer(8)
add_bold("Gilles Korzec")
add_text("Coach Digital Paris")
add_text("06 52 34 51 80")

add_hr()

# ---- NOTE API ----
add_spacer(8)
story.append(Paragraph(
    "<i>* Note : qu'est-ce qu'une API ?<br/>"
    "Une API (Application Programming Interface) est simplement un pont entre deux logiciels. "
    "C'est ce qui permet à votre collaborateur IA de lire les données de Titan sans avoir besoin de se connecter manuellement "
    "— comme un assistant qui consulte un dossier dans une armoire, sauf que l'armoire est un logiciel. "
    "Pas besoin de comprendre la technique : c'est notre travail. "
    "Vous, vous voyez le résultat : les chiffres arrivent tout seuls dans votre rapport du matin.</i>",
    styles['SmallNote']
))

# BUILD
doc.build(story)
print(f"✅ PDF généré : {OUTPUT}")
