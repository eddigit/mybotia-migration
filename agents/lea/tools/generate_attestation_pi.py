#!/usr/bin/env python3
"""
Génère l'attestation de propriété intellectuelle en PDF
avec les ajouts B.5 (interactivité vocale) et B.6 (secteur médical)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

OUTPUT_DIR = "/home/gilles/.openclaw/workspace/factures"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Attestation_Propriete_Intellectuelle_Gilles_KORZEC_V2.pdf")

# Styles
style_title = ParagraphStyle(
    'Title', fontName='Times-Bold', fontSize=16, alignment=TA_CENTER,
    spaceAfter=6, leading=20
)
style_subtitle = ParagraphStyle(
    'Subtitle', fontName='Times-Roman', fontSize=12, alignment=TA_CENTER,
    spaceAfter=4, leading=16
)
style_date = ParagraphStyle(
    'Date', fontName='Times-Roman', fontSize=11, alignment=2,  # RIGHT
    spaceAfter=12, leading=14
)
style_section = ParagraphStyle(
    'Section', fontName='Times-Bold', fontSize=13, alignment=TA_LEFT,
    spaceBefore=18, spaceAfter=8, leading=16
)
style_subsection = ParagraphStyle(
    'SubSection', fontName='Times-Bold', fontSize=11, alignment=TA_LEFT,
    spaceBefore=12, spaceAfter=6, leading=14
)
style_body = ParagraphStyle(
    'Body', fontName='Times-Roman', fontSize=11, alignment=TA_JUSTIFY,
    spaceAfter=6, leading=15, firstLineIndent=0
)
style_body_indent = ParagraphStyle(
    'BodyIndent', fontName='Times-Roman', fontSize=11, alignment=TA_JUSTIFY,
    spaceAfter=4, leading=15, leftIndent=1.5*cm
)
style_body_indent2 = ParagraphStyle(
    'BodyIndent2', fontName='Times-Roman', fontSize=11, alignment=TA_JUSTIFY,
    spaceAfter=4, leading=15, leftIndent=3*cm
)
style_separator = ParagraphStyle(
    'Separator', fontName='Times-Roman', fontSize=11, alignment=TA_CENTER,
    spaceBefore=12, spaceAfter=12
)
style_note = ParagraphStyle(
    'Note', fontName='Times-Italic', fontSize=10, alignment=TA_JUSTIFY,
    spaceAfter=6, leading=13
)
style_signature = ParagraphStyle(
    'Signature', fontName='Times-Roman', fontSize=11, alignment=TA_LEFT,
    spaceBefore=30, spaceAfter=6, leading=14
)

SEP = "═" * 60

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm
    )
    
    story = []
    
    # TITRE
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("ATTESTATION DE CRÉATION", style_title))
    story.append(Paragraph("ET DE PATERNITÉ INTELLECTUELLE", style_title))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Envoi en Lettre Recommandée avec Accusé de Réception", style_subtitle))
    story.append(Paragraph("à soi-même — Preuve d'antériorité", style_subtitle))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Paris, le 25 mars 2026", style_date))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(SEP, style_separator))
    
    # I. IDENTITÉ
    story.append(Paragraph("I. IDENTITÉ DU CRÉATEUR", style_section))
    story.append(Paragraph("Monsieur Gilles KORZEC", style_body))
    story.append(Paragraph("Entrepreneur individuel", style_body))
    story.append(Paragraph("SIRET : 834 049 197 00028", style_body))
    story.append(Paragraph("Domicilié au : 7, avenue du Maréchal Joffre — 66 480 MAUREILLAS-LAS-ILLAS", style_body))
    story.append(Paragraph("Téléphone : +33 6 52 34 51 80", style_body))
    story.append(Paragraph("Courriel : gilleskorzec@gmail.com", style_body))
    story.append(Paragraph(SEP, style_separator))
    
    # II. OBJET
    story.append(Paragraph("II. OBJET DE LA PRÉSENTE ATTESTATION", style_section))
    story.append(Paragraph(
        "La présente attestation a pour objet d'établir, de manière formelle et circonstanciée, "
        "la paternité intellectuelle de Monsieur Gilles KORZEC sur l'ensemble des créations, concepts, "
        "méthodologies, architectures techniques et œuvres de l'esprit décrites ci-après, et d'en fixer "
        "la date d'antériorité par le cachet postal de l'envoi en lettre recommandée avec accusé de réception.",
        style_body
    ))
    story.append(Paragraph(
        "Cette démarche est effectuée conformément aux dispositions du Code de la propriété intellectuelle, notamment :",
        style_body
    ))
    story.append(Paragraph(
        "— Articles L.111-1 et L.111-2 : l'auteur d'une œuvre de l'esprit jouit sur cette œuvre, "
        "du seul fait de sa création, d'un droit de propriété incorporelle exclusif et opposable à tous ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "— Article L.112-2 : sont notamment considérées comme œuvres de l'esprit les logiciels, "
        "y compris le matériel de conception préparatoire ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "— Article L.113-1 : la qualité d'auteur appartient, sauf preuve contraire, à celui ou ceux "
        "sous le nom de qui l'œuvre est divulguée.",
        style_body_indent
    ))
    story.append(Paragraph(SEP, style_separator))
    
    # III. DESCRIPTION DES CRÉATIONS
    story.append(Paragraph("III. DESCRIPTION DES CRÉATIONS", style_section))
    
    # A. Collaborateurs IA
    story.append(Paragraph("A. Le concept de « Collaborateurs IA »", style_subsection))
    story.append(Paragraph(
        "Monsieur Gilles KORZEC est le créateur et fondateur du concept de « Collaborateurs IA » — "
        "désignant des agents d'intelligence artificielle dotés d'une identité propre (nom, personnalité, "
        "spécialisation, mémoire persistante), intégrés comme membres à part entière de l'équipe d'une "
        "entreprise cliente, et interagissant avec les collaborateurs humains via les canaux de communication "
        "professionnels courants (WhatsApp, Telegram, email, webchat).",
        style_body
    ))
    story.append(Paragraph(
        "Ce concept se distingue fondamentalement des chatbots, assistants virtuels, ou solutions "
        "d'automatisation existant sur le marché par les caractéristiques suivantes :",
        style_body
    ))
    for item in [
        "1. <b>Identité individualisée</b> : chaque collaborateur IA dispose d'un nom, d'un avatar, "
        "d'un numéro de téléphone dédié, d'une adresse email propre, et d'un rôle fonctionnel défini "
        "dans l'organigramme du client (ex. : directrice administrative, commercial, coordinateur, tech lead) ;",
        
        "2. <b>Mémoire persistante et contextuelle</b> : chaque agent conserve une mémoire de long terme, "
        "structurée par client, par projet et par interaction, lui permettant d'assurer une continuité "
        "relationnelle et opérationnelle ;",
        
        "3. <b>Personnalité et comportement définis</b> : chaque collaborateur IA est gouverné par un "
        "ensemble de fichiers de personnalité (dénommés « cerveaux » par le créateur) définissant son ton, "
        "ses compétences, ses limites, ses protocoles d'interaction et ses règles de conduite ;",
        
        "4. <b>Intégration organique</b> : les collaborateurs IA ne sont pas des outils ponctuels mais des "
        "membres permanents de l'organisation, participant aux groupes de discussion, aux réunions, et aux "
        "processus opérationnels quotidiens ;",
        
        "5. <b>Multi-spécialisation</b> : déploiement d'équipes complètes de collaborateurs IA aux "
        "compétences complémentaires (administration, juridique, commerce, développement, IT)."
    ]:
        story.append(Paragraph(item, style_body_indent))
    
    story.append(Paragraph(
        "Le nom de domaine collaborateurs.pro a été acquis par Monsieur KORZEC pour porter cette marque et ce concept.",
        style_body
    ))
    
    # B. Architecture technique
    story.append(Paragraph("B. L'architecture technique propriétaire dite « Stack Coach Digital »", style_subsection))
    story.append(Paragraph(
        "Monsieur Gilles KORZEC a conçu, développé et mis en œuvre une architecture technique originale "
        "permettant le déploiement et la gestion des Collaborateurs IA. Cette architecture comprend :",
        style_body
    ))
    
    # B.1
    story.append(Paragraph("<b>B.1. Le système de « cerveaux » IA (Brain System)</b>", style_body))
    story.append(Paragraph(
        "Un ensemble structuré de fichiers de configuration constituant l'intelligence comportementale de chaque agent :",
        style_body_indent
    ))
    for item in [
        "— SOUL.md : fichier de personnalité définissant l'identité profonde, le ton, les valeurs, les interdits et le caractère de l'agent ;",
        "— MEMORY.md / MEMORY-CORE.md : système de mémoire hiérarchisée (mémoire transversale, mémoire par client, notes quotidiennes) assurant la continuité cognitive ;",
        "— IDENTITY.md : fiche d'identité complète de l'agent (nom, rôle, compétences, limites, outils accessibles) ;",
        "— AGENTS.md : définition de la hiérarchie, des règles opérationnelles, des procédures et des protocoles d'interaction entre agents et avec les humains ;",
        "— Protocoles WhatsApp : fichiers de configuration définissant le comportement de chaque agent dans chaque groupe de discussion client (réactivité, ton, autorisations, restrictions) ;",
        "— Fichiers mémoire client : dossiers individuels par client avec historique, contexte, décisions et état d'avancement."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    story.append(Paragraph(
        "Cette conception constitue une méthodologie originale de personnalisation d'agents IA, allant bien "
        "au-delà du simple « prompt engineering » en instaurant un véritable système de gouvernance comportementale persistante.",
        style_body_indent
    ))
    
    # B.2
    story.append(Paragraph("<b>B.2. L'interface propriétaire « MyBotIA »</b>", style_body))
    story.append(Paragraph(
        "Monsieur KORZEC a conçu et développé l'interface de chat premium MyBotIA (accessible sur le domaine "
        "mybotia.com et ses sous-domaines), comprenant :",
        style_body_indent
    ))
    for item in [
        "— Un système d'authentification par agent (chaque collaborateur IA disposant de son propre point d'accès) ;",
        "— Une interface de chat temps réel avec design personnalisé ;",
        "— Une application web progressive (PWA) installable ;",
        "— Un système de sous-domaines dynamiques par agent (lea.mybotia.com, oscar.mybotia.com, etc.)."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    
    # B.3
    story.append(Paragraph("<b>B.3. La plateforme d'administration « Admin MVP »</b>", style_body))
    story.append(Paragraph("Un tableau de bord de gestion comprenant :", style_body_indent))
    for item in [
        "— CRM intégré avec suivi client, pipeline commercial, et gestion des paiements ;",
        "— Système de facturation PDF automatisée ;",
        "— Tableau de bord financier (MRR, ARR, CA) ;",
        "— Interface de gestion des agents et de leurs configurations ;",
        "— Synchronisation avec les outils tiers (Notion, Qonto, Gmail)."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    
    # B.4
    story.append(Paragraph("<b>B.4. Le système de déploiement client</b>", style_body))
    story.append(Paragraph(
        "Une méthodologie structurée de déploiement des Collaborateurs IA chez les clients, incluant :",
        style_body_indent
    ))
    for item in [
        "— Processus d'onboarding par groupe WhatsApp dédié ;",
        "— Configuration des protocoles de communication par client ;",
        "— Personnalisation des agents selon le contexte métier du client ;",
        "— Système de facturation récurrente (abonnement mensuel)."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    
    # B.5 — NOUVEAU : Interactivité vocale
    story.append(Paragraph("<b>B.5. Le système d'interactivité vocale</b>", style_body))
    story.append(Paragraph(
        "Monsieur KORZEC a conçu et mis en œuvre un système d'interactivité vocale permettant aux "
        "Collaborateurs IA de communiquer par messages vocaux avec les utilisateurs, sur l'ensemble "
        "des canaux de communication (WhatsApp, Telegram, webchat). Ce système comprend :",
        style_body_indent
    ))
    for item in [
        "— La capacité pour chaque collaborateur IA d'envoyer et de recevoir des messages vocaux, "
        "reproduisant ainsi les usages naturels de la communication professionnelle ;",
        
        "— L'attribution d'une voix distinctive et constante à chaque agent, renforçant son identité "
        "et la relation de confiance avec les interlocuteurs humains ;",
        
        "— L'intégration transparente de cette fonctionnalité vocale dans les canaux existants (les "
        "messages vocaux apparaissent comme des bulles vocales natives, indistinguables d'un message vocal humain) ;",
        
        "— La possibilité d'interactions bidirectionnelles en voix, ajoutant une dimension conversationnelle "
        "inédite aux collaborateurs IA."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    story.append(Paragraph(
        "Cette innovation transforme fondamentalement le rapport entre l'humain et l'agent IA en passant "
        "d'une interaction exclusivement textuelle à une communication multimodale naturelle, proche de la "
        "relation interpersonnelle réelle.",
        style_body_indent
    ))
    
    # B.6 — NOUVEAU : Secteur médical
    story.append(Paragraph("<b>B.6. L'application au secteur de la santé et du matériel médical — Assistant IA opérationnel intégré</b>", style_body))
    story.append(Paragraph(
        "Monsieur KORZEC a conçu et déployé une déclinaison spécifique de son concept de Collaborateurs IA "
        "pour le secteur de la santé et du négoce de dispositifs médicaux, constituant une innovation à part entière.",
        style_body_indent
    ))
    story.append(Paragraph(
        "Ce système met en œuvre un assistant IA opérationnel intégré — agissant comme un véritable collaborateur "
        "permanent au sein d'une entreprise du secteur médical — doté des capacités suivantes :",
        style_body_indent
    ))
    for item in [
        "— <b>Gestion administrative autonome</b> : traitement des notes de frais, suivi comptable, génération "
        "de documents conformes aux normes du secteur (notamment le Règlement européen MDR 2017/745 relatif aux "
        "dispositifs médicaux) ;",
        
        "— <b>Rédaction juridique spécialisée</b> : élaboration de conditions générales de vente conformes à la "
        "réglementation applicable aux dispositifs médicaux et équipements de protection individuelle ;",
        
        "— <b>Prospection commerciale intelligente</b> : identification et qualification de prospects dans le "
        "secteur de la santé (hôpitaux, cliniques, laboratoires, professionnels de santé libéraux) ;",
        
        "— <b>Réactivité et disponibilité permanentes</b> : l'assistant IA opère 24 heures sur 24, 7 jours sur 7, "
        "avec une capacité de réponse instantanée — permettant au dirigeant de bénéficier en temps réel d'un bras "
        "droit opérationnel complet, là où un collaborateur humain serait contraint par les horaires, les congés et "
        "les délais de traitement ;",
        
        "— <b>Interactivité vocale native</b> : communication par messages vocaux sur les canaux de messagerie "
        "professionnels, reproduisant la fluidité d'un échange avec un collaborateur humain."
    ]:
        story.append(Paragraph(item, style_body_indent2))
    story.append(Paragraph(
        "Cette application sectorielle démontre la transversalité et l'adaptabilité du concept de Collaborateurs IA "
        "à des domaines réglementés et exigeants, et constitue — à la connaissance du créateur — une première dans "
        "le secteur de la santé en France.",
        style_body_indent
    ))
    
    # C. Positionnement commercial
    story.append(Paragraph("C. Le positionnement commercial et la marque", style_subsection))
    story.append(Paragraph(
        "Monsieur KORZEC a créé et développé un positionnement commercial unique articulé autour de :",
        style_body
    ))
    for item in [
        "— La marque « Coach Digital Paris » ;",
        "— Le concept commercial de « Collaborateurs IA » comme offre de service ;",
        "— Le domaine collaborateurs.pro ;",
        "— Le domaine mybotia.com et l'ensemble de ses sous-domaines ;",
        "— Le domaine coachdigitalparis.com ;",
        "— Le domaine cabinet2point0.com (rebaptisé Cabinet 4.0, orienté cabinets d'avocats) ;",
        "— Le domaine maboitedigitale.com ;",
        "— L'ensemble des supports commerciaux, présentations, et contenus marketing associés."
    ]:
        story.append(Paragraph(item, style_body_indent))
    
    story.append(Paragraph(SEP, style_separator))
    
    # IV. DISTINCTION
    story.append(Paragraph("IV. DISTINCTION ENTRE INFRASTRUCTURE ET CRÉATION PROPRIÉTAIRE", style_section))
    story.append(Paragraph(
        "Il est précisé que l'architecture décrite ci-dessus s'appuie pour sa couche d'infrastructure sur "
        "un logiciel open source distribué sous licence libre.",
        style_body
    ))
    story.append(Paragraph(
        "Toutefois, les créations de Monsieur KORZEC se situent en amont et en aval de cette infrastructure "
        "et constituent des œuvres originales distinctes, à savoir :",
        style_body
    ))
    
    distinctions = [
        ("Infrastructure de messagerie et de routage", "Logiciel open source — Communauté open source"),
        ("Conception des cerveaux IA (SOUL, MEMORY, IDENTITY, AGENTS, protocoles)", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Méthodologie de personnalisation et de déploiement", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Interface MyBotIA", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Plateforme Admin MVP", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Concept commercial « Collaborateurs IA »", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Architecture multi-agents avec identités persistantes", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Système d'interactivité vocale", "ŒUVRE ORIGINALE — Gilles KORZEC"),
        ("Application sectorielle santé / matériel médical", "ŒUVRE ORIGINALE — Gilles KORZEC"),
    ]
    for desc, attr in distinctions:
        story.append(Paragraph(f"<b>{desc}</b><br/>→ {attr}", style_body_indent))
    
    story.append(Paragraph(
        "Cette distinction est analogue à celle existant entre un système d'exploitation (Linux) et les logiciels "
        "applicatifs développés sur celui-ci : l'utilisation d'une infrastructure libre n'altère en rien la propriété "
        "intellectuelle des créations réalisées avec et au-dessus de celle-ci.",
        style_body
    ))
    story.append(Paragraph(SEP, style_separator))
    
    # V. ANTÉRIORITÉ
    story.append(Paragraph("V. ANTÉRIORITÉ ET CHRONOLOGIE", style_section))
    story.append(Paragraph(
        "Les travaux de conception et de développement ont débuté courant 2024 et se poursuivent de manière "
        "continue à la date de la présente attestation.",
        style_body
    ))
    story.append(Paragraph(
        "Les premières mises en production de Collaborateurs IA chez des clients tiers sont intervenues au cours "
        "du premier trimestre 2026, avec notamment :",
        style_body
    ))
    for item in [
        "— Déploiement d'équipes de collaborateurs IA auprès de cabinets d'avocats ;",
        "— Déploiement d'un assistant IA opérationnel dans le secteur du matériel médical ;",
        "— Mise en service du système d'interactivité vocale sur l'ensemble des canaux ;",
        "— Mise en service de l'interface MyBotIA ;",
        "— Mise en service de la plateforme Admin MVP ;",
        "— Acquisition et configuration des noms de domaine susmentionnés."
    ]:
        story.append(Paragraph(item, style_body_indent))
    story.append(Paragraph(SEP, style_separator))
    
    # VI. VEILLE CONCURRENTIELLE
    story.append(Paragraph("VI. VEILLE CONCURRENTIELLE — POSITIONNEMENT PIONNIER", style_section))
    story.append(Paragraph(
        "Une veille concurrentielle approfondie réalisée en mars 2026 a permis d'établir les constats suivants :",
        style_body
    ))
    story.append(Paragraph(
        "1. Aucun acteur identifié ne propose à ce jour de « collaborateurs IA » intégrés comme membres d'équipe "
        "dans l'organigramme de l'entreprise cliente, disposant d'une identité propre, d'une mémoire persistante, "
        "et interagissant de manière autonome via les canaux de communication courants ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "2. Les solutions existantes sur le marché se limitent à :",
        style_body_indent
    ))
    for item in [
        "— Des chatbots (réponses scriptes, sans identité ni mémoire) ;",
        "— Des assistants IA génériques (ChatGPT, Claude, Gemini) utilisés ponctuellement sans intégration organisationnelle ;",
        "— Des outils d'automatisation (Zapier, Make) sans composante conversationnelle ni personnalité ;",
        "— Des SaaS verticaux intégrant de l'IA comme fonctionnalité secondaire ;"
    ]:
        story.append(Paragraph(item, style_body_indent2))
    story.append(Paragraph(
        "3. Le concept de collaborateurs IA dotés d'identité, de mémoire, de spécialisation et intégrés dans "
        "l'organigramme client constitue, à la date de la présente, une innovation sans équivalent identifié sur "
        "le marché français et international ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "4. Aucun acteur identifié ne propose de système d'interactivité vocale intégré aux collaborateurs IA, "
        "ni de déclinaison sectorielle dans le domaine de la santé avec un assistant IA opérationnel permanent ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "5. Monsieur Gilles KORZEC peut légitimement revendiquer la qualité de pionnier et fondateur de cette approche.",
        style_body_indent
    ))
    story.append(Paragraph(SEP, style_separator))
    
    # VII. PIÈCES ANNEXÉES
    story.append(Paragraph("VII. PIÈCES ANNEXÉES", style_section))
    story.append(Paragraph(
        "Les pièces suivantes sont jointes à la présente attestation pour servir de preuves matérielles :",
        style_body
    ))
    for i, item in enumerate([
        "Copie des fichiers de configuration des cerveaux IA (SOUL.md, MEMORY.md, IDENTITY.md, AGENTS.md) — extraits significatifs ;",
        "Captures d'écran de l'interface MyBotIA ;",
        "Captures d'écran de la plateforme Admin MVP ;",
        "Certificats WHOIS des noms de domaine (collaborateurs.pro, mybotia.com, coachdigitalparis.com, cabinet2point0.com, maboitedigitale.com) ;",
        "Factures clients attestant de la commercialisation ;",
        "Extraits de la veille concurrentielle ;",
        "Captures d'écran des interactions vocales avec les collaborateurs IA ;",
        "Captures d'écran du déploiement dans le secteur médical."
    ], 1):
        story.append(Paragraph(f"{i}. {item}", style_body_indent))
    story.append(Paragraph(SEP, style_separator))
    
    # VIII. DÉCLARATION
    story.append(Paragraph("VIII. DÉCLARATION", style_section))
    story.append(Paragraph(
        "Je soussigné, Monsieur Gilles KORZEC, né le 20 novembre 1972 à Thionville (Moselle — 57100), "
        "de nationalité française, demeurant au 7, avenue du Maréchal Joffre — 66 480 MAUREILLAS-LAS-ILLAS, "
        "atteste sur l'honneur :",
        style_body
    ))
    story.append(Paragraph(
        "— Être le créateur unique de l'ensemble des œuvres, concepts, méthodologies et architectures "
        "techniques décrits dans la présente attestation ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "— N'avoir connaissance d'aucune création antérieure identique ou substantiellement similaire ;",
        style_body_indent
    ))
    story.append(Paragraph(
        "— Que les informations contenues dans le présent document sont exactes et sincères.",
        style_body_indent
    ))
    story.append(Paragraph(
        "La présente attestation est établie pour servir et valoir ce que de droit, et notamment pour "
        "constituer une preuve d'antériorité de mes droits de propriété intellectuelle sur l'ensemble des "
        "créations décrites.",
        style_body
    ))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Fait à Paris, le 25 mars 2026", style_body))
    story.append(Paragraph("En deux exemplaires originaux", style_body))
    story.append(Paragraph("(un conservé, un envoyé en recommandé avec AR)", style_body))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Signature :", style_signature))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("___________________________________", style_body))
    story.append(Paragraph("Monsieur Gilles KORZEC", style_body))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("─" * 60, style_separator))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<b>NOTE IMPORTANTE :</b>", style_note
    ))
    story.append(Paragraph(
        "La présente attestation, envoyée en lettre recommandée avec accusé de réception, bénéficie d'une "
        "date certaine conférée par le cachet postal, conformément à la jurisprudence constante en matière de "
        "preuve d'antériorité de droits de propriété intellectuelle (Cass. 1ère civ., 13 novembre 2008, "
        "n° 06-19.021).",
        style_note
    ))
    story.append(Paragraph(
        "Il est recommandé de conserver l'enveloppe cachetée non ouverte, accompagnée de l'accusé de réception, "
        "en lieu sûr. L'ouverture ne devra intervenir qu'en présence d'un huissier de justice ou sur décision "
        "judiciaire, afin de préserver la valeur probante du document.",
        style_note
    ))
    
    doc.build(story)
    print(f"PDF généré : {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    build_pdf()
