#!/usr/bin/env python3
"""
Génère la proforma VL Medical → Émergence SAS pour gants LCH Sensitex en PDF
Format identique à la proforma HEXA N° 260106, même prix de vente
"""

from fpdf import FPDF

FONT_DIR = "/home/gilles/.npm-global/lib/node_modules/openclaw/node_modules/pdfjs-dist/standard_fonts"

class ProformaPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=15)
        # Register Unicode font
        self.add_font('Liberation', '', f'{FONT_DIR}/LiberationSans-Regular.ttf', uni=True)
        self.add_font('Liberation', 'B', f'{FONT_DIR}/LiberationSans-Bold.ttf', uni=True)
        self.add_font('Liberation', 'I', f'{FONT_DIR}/LiberationSans-Italic.ttf', uni=True)
        self.add_font('Liberation', 'BI', f'{FONT_DIR}/LiberationSans-BoldItalic.ttf', uni=True)

def fmt(val):
    """Format nombre en euros français: 57 566,52 €"""
    if val < 0:
        s = f'{abs(val):,.2f}'.replace(',', ' ').replace('.', ',')
        return f'- {s} €'
    s = f'{val:,.2f}'.replace(',', ' ').replace('.', ',')
    return f'{s} €'

pdf = ProformaPDF()
pdf.add_page()
F = 'Liberation'

# === EN-TÊTE ===
pdf.set_font(F, 'B', 18)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 10, 'VL MEDICAL', new_x='LMARGIN', new_y='NEXT', align='C')

pdf.set_font(F, 'I', 8)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 4, 'Dispositifs médicaux, équipements de protection individuelle & trading divers', new_x='LMARGIN', new_y='NEXT', align='C')

pdf.set_font(F, '', 7)
pdf.cell(0, 4, '853 225 100 R.C.S. Aix-en-Provence', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.cell(0, 4, '190 Rue Topaze 13510 Éguilles', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.cell(0, 4, 'Numéro EORI : FR85322510000025', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(5)

# === CLIENT ===
xc = 110
pdf.set_font(F, 'B', 10)
pdf.set_text_color(0, 0, 0)
pdf.set_x(xc); pdf.cell(0, 5, 'Émergence Internationale SAS', new_x='LMARGIN', new_y='NEXT')
pdf.set_font(F, '', 9)
pdf.set_x(xc); pdf.cell(0, 5, 'M. OUATTARA  af.emergence@gmail.com', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(xc); pdf.cell(0, 5, '9 bis passage Dartois Bidot,', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(xc); pdf.cell(0, 5, '94100 Saint-Maur-des-Fossés', new_x='LMARGIN', new_y='NEXT')
pdf.set_font(F, '', 7)
pdf.set_x(xc); pdf.cell(0, 5, 'Siret : 89451323300011       TVA : FR82894513233', new_x='LMARGIN', new_y='NEXT')
pdf.ln(3)

# === DATE ===
pdf.set_font(F, 'B', 10)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 6, 'ÉGUILLES, le lundi 10 mars 2026', new_x='LMARGIN', new_y='NEXT')
pdf.ln(4)

# === TITRE ===
pdf.set_font(F, 'B', 11)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 7, 'PHARMACEUTICAL PRODUCTS — TRADE TERMS : CIF Cotonou', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(3)
pdf.set_font(F, 'B', 12)
pdf.cell(0, 7, 'Proforma N° 260301', new_x='LMARGIN', new_y='NEXT')
pdf.ln(2)

# === TABLEAU HEADER ===
pdf.set_fill_color(232, 238, 245)
pdf.set_font(F, 'B', 9)
pdf.set_text_color(0, 51, 102)
pdf.cell(75, 7, 'Libellé', border=1, fill=True, align='C')
pdf.cell(15, 7, 'Base', border=1, fill=True, align='C')
pdf.cell(30, 7, 'Master boxes', border=1, fill=True, align='C')
pdf.cell(25, 7, 'Price', border=1, fill=True, align='C')
pdf.cell(35, 7, 'Amount', border=1, fill=True, align='C')
pdf.ln()

pdf.set_font(F, 'I', 7)
pdf.set_text_color(80, 80, 80)
pdf.cell(180, 5, 'Natural rubber gloves, non-sterile, powder-free — Master boxes of ten Boxes of 100 gloves', new_x='LMARGIN', new_y='NEXT')

# === PRODUITS ===
products = [
    ('Latex LCH Sensitex Cartons de 10 Boîtes Size S',   2,   140, 15.50,  2170.00),
    ('Latex LCH Sensitex Cartons de 10 Boîtes Size M',  22,  1540, 15.50, 23870.00),
    ('Latex LCH Sensitex Cartons de 10 Boîtes Size L',  22,  1540, 15.50, 23870.00),
    ('Latex LCH Sensitex Cartons de 10 Boîtes Size XL',  2,   140, 15.50,  2170.00),
]

pdf.set_text_color(0, 0, 0)
for desc, base, boxes, price, amount in products:
    pdf.set_font(F, '', 9)
    pdf.cell(75, 6, desc, border='B')
    pdf.cell(15, 6, str(base), border='B', align='C')
    pdf.cell(30, 6, f'{boxes:,}'.replace(',', ' '), border='B', align='C')
    pdf.cell(25, 6, fmt(price), border='B', align='R')
    pdf.cell(35, 6, fmt(amount), border='B', align='R')
    pdf.ln()

# Avoir
pdf.set_font(F, '', 9)
pdf.cell(75, 6, 'Avoir en valeur sur no show précédente expédition', border='B')
pdf.cell(15, 6, '', border='B')
pdf.cell(30, 6, '', border='B')
pdf.cell(25, 6, '', border='B', align='R')
pdf.cell(35, 6, fmt(-360), border='B', align='R')
pdf.ln(8)

# Maritime
pdf.set_font(F, '', 8)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 4, 'Compagnie maritime : MSC          POL: Fos-sur-Mer', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 4, 'Transit time : 32 jours via Lomé', new_x='LMARGIN', new_y='NEXT')
pdf.ln(3)

# Assurance
pdf.set_text_color(0, 0, 0)
pdf.set_font(F, '', 8)
pdf.cell(75, 6, 'Insurance base achats x 1,1 + transports', border='B')
pdf.set_font(F, '', 7)
pdf.cell(15, 6, '57 155 €', border='B', align='C')
pdf.cell(30, 6, '0,72%', border='B', align='C')
pdf.set_font(F, '', 9)
pdf.cell(25, 6, '411,52 €', border='B', align='R')
pdf.cell(35, 6, '411,52 €', border='B', align='R')
pdf.ln()

# BESC
pdf.set_font(F, '', 9)
pdf.cell(75, 6, 'BESC Cotonou si requis :', border='B')
pdf.cell(15, 6, '', border='B')
pdf.cell(30, 6, '1', border='B', align='C')
pdf.cell(25, 6, '85,00 €', border='B', align='R')
pdf.cell(35, 6, '85,00 €', border='B', align='R')
pdf.ln()

# Chargement
pdf.cell(75, 6, 'Chargement du Container de 40 pieds HQ', border='B')
pdf.cell(15, 6, '', border='B')
pdf.cell(30, 6, '1', border='B', align='C')
pdf.cell(25, 6, '1 450,00 €', border='B', align='R')
pdf.cell(35, 6, '1 450,00 €', border='B', align='R')
pdf.ln()

# Fret
pdf.cell(75, 6, 'Cost of delivery to Cotonou (Centrimex offer)', border='B')
pdf.cell(15, 6, '', border='B')
pdf.cell(30, 6, '1', border='B', align='C')
pdf.cell(25, 6, '3 900,00 €', border='B', align='R')
pdf.cell(35, 6, '3 900,00 €', border='B', align='R')
pdf.ln(2)

# Total master boxes
pdf.set_font(F, 'B', 9)
pdf.cell(90, 5, 'Estimation Chargement')
pdf.cell(30, 5, 'Total Master boxes')
pdf.cell(60, 5, '3 360')
pdf.ln(5)

# === TOTAUX ===
total_ht = 57566.52

pdf.set_fill_color(212, 225, 240)
pdf.set_text_color(0, 51, 102)

# Incoterm + HT
pdf.set_font(F, 'B', 9)
pdf.cell(50, 6, 'Incoterm : CIF')
pdf.cell(65, 6, '')
pdf.cell(25, 6, 'Montant HT', align='R')
pdf.set_font(F, 'B', 11)
pdf.cell(40, 6, fmt(total_ht), align='R', fill=True)
pdf.ln()

# Origin + TVA
pdf.set_font(F, 'B', 9)
pdf.cell(50, 5, 'Origin of goods : Malaysia')
pdf.cell(65, 5, '')
pdf.set_font(F, '', 9)
pdf.cell(25, 5, 'TVA', align='R')
pdf.cell(40, 5, 'No VAT export', align='R')
pdf.ln()

# HS
pdf.set_font(F, 'B', 9)
pdf.cell(50, 5, 'HS code : 40151900')
pdf.set_font(F, 'I', 7)
pdf.set_text_color(80, 80, 80)
pdf.cell(130, 5, "Marchandise destinée à l'exportation et non soumise à TVA", align='R')
pdf.ln()

# Boxes
pdf.set_text_color(0, 51, 102)
pdf.set_font(F, 'B', 9)
pdf.cell(55, 5, 'Boxes Latex Gloves : 33 600')
pdf.set_font(F, 'I', 7)
pdf.set_text_color(80, 80, 80)
pdf.cell(125, 5, 'Marchandise remise au port de Fos-sur-Mer zone douanière', align='R')
pdf.ln()

# Containers + TTC
pdf.set_text_color(0, 51, 102)
pdf.set_font(F, 'B', 9)
pdf.cell(50, 6, 'Containers : 1')
pdf.cell(65, 6, '')
pdf.cell(25, 6, 'Net à Payer TTC', align='R')
pdf.set_font(F, 'B', 11)
pdf.cell(40, 6, fmt(total_ht), align='R', fill=True)
pdf.ln(7)

# === PAIEMENT ===
pdf.set_text_color(0, 0, 0)
pdf.set_font(F, 'B', 9)
pdf.cell(90, 5, 'Condition de paiement : Comptant')
pdf.set_font(F, '', 9)
pdf.cell(50, 5, 'À la commande', align='R')
pdf.set_font(F, 'B', 10)
pdf.cell(40, 5, fmt(22000), align='R')
pdf.ln()

pdf.set_font(F, '', 9)
pdf.cell(90, 5, 'Adresse de livraison :')
pdf.cell(50, 5, 'Au chargement', align='R')
pdf.set_font(F, 'B', 10)
pdf.cell(40, 5, fmt(35566.52), align='R')
pdf.ln()

pdf.set_font(F, '', 9)
pdf.cell(0, 4, 'Port de Cotonou', new_x='LMARGIN', new_y='NEXT')

pdf.set_font(F, 'I', 7)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 4, "Délai de mise à disposition des gants à Marseille auprès du transitaire ==> 2 jours après confirmation du devis et dépôt de l'acompte", new_x='LMARGIN', new_y='NEXT')
pdf.ln(3)

# === DESTINATION FINALE ===
pdf.set_text_color(0, 0, 0)
pdf.set_font(F, 'B', 8)
pdf.cell(0, 4, 'Marchandises exportées vers le Niger et livrées sous Douane. Client Final : Nord Sud Pharma SA', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font(F, '', 7)
pdf.cell(0, 4, 'Château 1, PL, rue des Dallols, BP. 2074 Niamey, Niger.', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(3)

# === BANQUE — bloc aligné à droite, compact ===
pdf.set_draw_color(0, 51, 102)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(2)

# Bloc gauche : mention paiement / Bloc droit : coordonnées bancaires
y_bank = pdf.get_y()

# Colonne gauche — texte paiement
pdf.set_font(F, '', 8)
pdf.set_text_color(0, 0, 0)
pdf.cell(90, 4, 'Payment by bank transfer to our account at Société Générale', new_x='LMARGIN', new_y='NEXT')
pdf.cell(90, 4, 'Paiement par virement sur notre compte bancaire', new_x='LMARGIN', new_y='NEXT')

# Colonne droite — coordonnées bancaires
pdf.set_xy(110, y_bank)
pdf.set_font(F, 'B', 9)
pdf.set_text_color(0, 51, 102)
pdf.cell(90, 5, 'SAS VL MEDICAL', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(110)
pdf.set_font(F, '', 8)
pdf.set_text_color(0, 0, 0)
pdf.cell(90, 4, '190 Rue Topaze 13510 Éguilles', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(110)
pdf.set_font(F, 'B', 10)
pdf.set_text_color(0, 51, 102)
pdf.cell(90, 5, 'IBAN FR76 3000 3001 6400 0200 0411 902', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(110)
pdf.set_font(F, 'B', 9)
pdf.cell(90, 5, 'BIC : SOGEFRPP', new_x='LMARGIN', new_y='NEXT')
pdf.ln(2)

# Pied de page — compact
pdf.set_font(F, '', 7)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 3, 'Société par action simplifiée de 1.000 €    —    N° TVA Intracommunautaire : FR 27853225100', new_x='LMARGIN', new_y='NEXT', align='C')

output = '/home/gilles/.openclaw-vlmedical/workspace-vlmedical-admin/Proforma_VL_Emergence_LCH_260301.pdf'
pdf.output(output)
print(f'PDF généré : {output}')
print(f'Total HT = TTC : {fmt(total_ht)}')
print(f'Acompte : {fmt(22000)}')
print(f'Solde : {fmt(35566.52)}')
