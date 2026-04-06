#!/usr/bin/env python3
"""Génère la proforma Medicov corrigée en PDF avec reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "dossiers", "emilabo-marseille", "Proforma_20260304_Medicov_IBAN_CORRIGE.pdf")

def draw_box(c, x, y, w, h, fill_color=None, stroke_color=None):
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
    if fill_color:
        c.rect(x, y, w, h, fill=1, stroke=1 if stroke_color else 0)
    else:
        c.rect(x, y, w, h, fill=0, stroke=1)

def main():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    w, h = A4  # 595 x 842
    navy = HexColor('#003366')
    light_blue = HexColor('#f0f8ff')
    light_gray = HexColor('#f9f9f9')
    warning_bg = HexColor('#fff3cd')
    
    margin = 30
    
    # ===== HEADER =====
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h - 40, "PROFORMA INVOICE")
    c.setFont("Helvetica", 11)
    c.setFillColor(black)
    c.drawCentredString(w/2, h - 56, "Export - Emilabo Nitrile Gloves")
    c.setFont("Helvetica", 9)
    c.drawCentredString(w/2, h - 70, "Date: March 27, 2026  |  Proforma N°: 20260304")
    
    # Line under header
    c.setStrokeColor(navy)
    c.setLineWidth(2)
    c.line(margin, h - 78, w - margin, h - 78)
    
    # ===== SELLER / BUYER BOXES =====
    box_y = h - 200
    box_h = 110
    box_w = (w - 2*margin - 10) / 2
    
    # Seller box
    draw_box(c, margin, box_y, box_w, box_h, fill_color=light_gray, stroke_color=navy)
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 8, box_y + box_h - 14, "SELLER:")
    c.setFillColor(black)
    c.setFont("Helvetica", 8.5)
    lines_seller = [
        "VL MEDICAL SAS",
        "190 Rue Topaze",
        "13510 Éguilles, FRANCE",
        "SIRET: 853 225 100 00025",
        "VAT: FR 27853225100",
        "Contact: Jean-Luc AUBAGNAC",
        "Phone: +33 6 18 24 40 13",
        "Email: jeanluc@aubagnac.com"
    ]
    for i, line in enumerate(lines_seller):
        c.drawString(margin + 8, box_y + box_h - 28 - i*12, line)
    
    # Buyer box
    bx = margin + box_w + 10
    draw_box(c, bx, box_y, box_w, box_h, fill_color=light_gray, stroke_color=navy)
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(bx + 8, box_y + box_h - 14, "BUYER:")
    c.setFillColor(black)
    c.setFont("Helvetica", 8.5)
    lines_buyer = [
        "Medicov s.c.",
        "Nałęczowska 30",  
        "20-701 Lublin, POLAND",
        "VAT: PL7123269418",
        "Contact: Anna and Rafał Hotlos",
        "Email: biuro@medicov.eu"
    ]
    for i, line in enumerate(lines_buyer):
        c.drawString(bx + 8, box_y + box_h - 28 - i*12, line)
    
    # ===== ITEMS TABLE =====
    ty = box_y - 20
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, ty, "ITEMS")
    c.setStrokeColor(navy)
    c.setLineWidth(1.5)
    c.line(margin, ty - 4, margin + 40, ty - 4)
    
    # Table header
    ty -= 22
    cols = [margin, margin+155, margin+210, margin+255, margin+300, margin+345, margin+400, margin+460]
    col_w = [155, 55, 45, 45, 45, 55, 60, w-margin-460]
    headers = ["Description", "Sizes", "Pallets", "Boxes", "Batch", "Expiry", "Unit Price", "Total"]
    
    row_h = 16
    # Header bg
    draw_box(c, margin, ty - row_h + 4, w - 2*margin, row_h, fill_color=navy)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7.5)
    for i, hdr in enumerate(headers):
        c.drawString(cols[i] + 3, ty - 8, hdr)
    
    # Row 1: Black gloves
    ty -= row_h
    row_h_data = 28
    c.setFillColor(black)
    c.setFont("Helvetica", 7.5)
    c.drawString(cols[0] + 3, ty - 10, "BLACK nitrile gloves EMILABO")
    c.setFont("Helvetica", 6.5)
    c.drawString(cols[0] + 3, ty - 20, "Powder-free, non-sterile")
    c.setFont("Helvetica", 6.5)
    c.drawString(cols[1] + 3, ty - 10, "S(6p),M(5p),")
    c.drawString(cols[1] + 3, ty - 20, "L(7p),XL(4p)")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(cols[2] + 22, ty - 14, "22")
    c.drawCentredString(cols[3] + 22, ty - 14, "15,400")
    c.drawCentredString(cols[4] + 22, ty - 14, "54384")
    c.drawCentredString(cols[5] + 27, ty - 14, "30/11/2026")
    c.drawCentredString(cols[6] + 30, ty - 14, "€1.60")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(cols[7] + 3, ty - 14, "€24,640.00")
    
    # Row border
    c.setStrokeColor(HexColor('#dddddd'))
    c.setLineWidth(0.5)
    c.line(margin, ty - row_h_data + 4, w - margin, ty - row_h_data + 4)
    
    # Row 2: Blue gloves
    ty -= row_h_data
    c.setFillColor(black)
    c.setFont("Helvetica", 7.5)
    c.drawString(cols[0] + 3, ty - 10, "BLUE nitrile gloves EMILABO")
    c.setFont("Helvetica", 6.5)
    c.drawString(cols[0] + 3, ty - 20, "Powder-free, non-sterile")
    c.setFont("Helvetica", 6.5)
    c.drawString(cols[1] + 3, ty - 10, "S(3p),M(3p),")
    c.drawString(cols[1] + 3, ty - 20, "L(3p),XL(2p)")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(cols[2] + 22, ty - 14, "11")
    c.drawCentredString(cols[3] + 22, ty - 14, "7,700")
    c.drawCentredString(cols[4] + 22, ty - 14, "27773")
    c.drawCentredString(cols[5] + 27, ty - 14, "30/12/2026")
    c.drawCentredString(cols[6] + 30, ty - 14, "€1.50")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(cols[7] + 3, ty - 14, "€11,550.00")
    
    c.line(margin, ty - row_h_data + 4, w - margin, ty - row_h_data + 4)
    
    # Total row
    ty -= row_h_data
    draw_box(c, margin, ty - 18, w - 2*margin, 22, fill_color=HexColor('#e8f4f8'))
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(cols[7] - 5, ty - 12, "TOTAL (VAT EXEMPT - Export)")
    c.drawString(cols[7] + 3, ty - 12, "€36,190.00")
    
    ty -= 28
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(margin, ty, "Product: www.groupegaillard.fr/gants-non-steriles/332-gant-nitrile-sans-poudre-emilabo.html")
    ty -= 11
    c.drawString(margin, ty, "Packaging: 100 gloves/box • 10 boxes/carton • 70 cartons/pallet")
    
    # ===== DELIVERY =====
    ty -= 22
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, ty, "DELIVERY & PICKUP")
    c.setLineWidth(1.5)
    c.setStrokeColor(navy)
    c.line(margin, ty - 4, margin + 120, ty - 4)
    
    ty -= 18
    c.setFillColor(black)
    c.setFont("Helvetica", 8)
    delivery_info = [
        ("Incoterm:", "EXW (Ex Works) - Marseille, France"),
        ("Pickup location:", "Le Dépôt de Méditerranée Transit, 455 Chemin du Littoral, 13016 Marseille"),
        ("Destination:", "Lublin, Poland"),
        ("Transport:", "Organized and paid by buyer"),
        ("Pickup deadline:", "Immediate upon SEPA payment receipt (same day if before 3 PM)"),
    ]
    for label, val in delivery_info:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(margin + 5, ty, label)
        c.setFont("Helvetica", 8)
        c.drawString(margin + 100, ty, val)
        ty -= 13
    
    # ===== PAYMENT =====
    ty -= 10
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, ty, "PAYMENT TERMS")
    c.setLineWidth(1.5)
    c.line(margin, ty - 4, margin + 100, ty - 4)
    
    ty -= 18
    c.setFillColor(black)
    payment_info = [
        ("Payment method:", "100% SEPA bank transfer before pickup"),
        ("Currency:", "EUR (Euro)"),
        ("Amount due:", "€36,190.00"),
    ]
    for label, val in payment_info:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(margin + 5, ty, label)
        c.setFont("Helvetica", 8)
        c.drawString(margin + 100, ty, val)
        ty -= 13
    
    # ===== BANK DETAILS =====
    ty -= 10
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, ty, "BANK DETAILS - SOCIÉTÉ GÉNÉRALE")
    c.setLineWidth(1.5)
    c.line(margin, ty - 4, margin + 220, ty - 4)
    
    ty -= 10
    bank_h = 65
    draw_box(c, margin, ty - bank_h, w - 2*margin, bank_h, fill_color=light_blue, stroke_color=navy)
    c.setLineWidth(2)
    
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(w/2, ty - 15, "Account holder: VL MEDICAL SAS")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w/2, ty - 32, "IBAN: FR76 3000 3001 6400 0200 0411 902")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w/2, ty - 48, "BIC/SWIFT: SOGEFRPP")
    
    c.setFont("Helvetica", 9)
    c.drawCentredString(w/2, ty - 60, "Bank: Société Générale")
    
    # ===== VAT EXEMPTION WARNING =====
    ty -= bank_h + 15
    warn_h = 50
    draw_box(c, margin, ty - warn_h, w - 2*margin, warn_h, fill_color=warning_bg)
    c.setStrokeColor(HexColor('#ff9800'))
    c.setLineWidth(3)
    c.line(margin, ty - warn_h, margin, ty)
    
    c.setFillColor(HexColor('#d32f2f'))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margin + 8, ty - 12, "VAT EXEMPTION - MANDATORY CONDITION:")
    c.setFillColor(black)
    c.setFont("Helvetica", 7)
    c.drawString(margin + 8, ty - 24, "This invoice is VAT EXEMPT under EU export rules (Article 262 I of French Tax Code).")
    c.drawString(margin + 8, ty - 34, "BUYER COMMITMENT: Provide the signed delivery note (CMR) stamped by the carrier proving goods left French territory.")
    c.drawString(margin + 8, ty - 44, "Failure to provide this proof may result in VAT charges being applied retroactively.")
    
    # ===== GENERAL CONDITIONS =====
    ty -= warn_h + 15
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, ty, "GENERAL CONDITIONS")
    c.setLineWidth(1.5)
    c.setStrokeColor(navy)
    c.line(margin, ty - 3, margin + 130, ty - 3)
    
    ty -= 15
    c.setFillColor(black)
    c.setFont("Helvetica", 7.5)
    conditions = [
        "• Sale: Complete lot only (33 pallets, non-divisible)",
        "• Inspection: Authorized at warehouse before payment",
        "• Validity: 48 hours from issue date",
        "• Condition: New, original packaging, optimal storage conditions",
        "• Compliance: CE medical device standards",
    ]
    for cond in conditions:
        c.drawString(margin + 5, ty, cond)
        ty -= 11
    
    # ===== PAGE 2 — ACCEPTANCE =====
    c.setFont("Helvetica", 7)
    c.drawCentredString(w/2, 20, "Page 1/2")
    c.showPage()
    
    # Page 2
    ty = h - 50
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, ty, "ACCEPTANCE")
    c.setLineWidth(2)
    c.setStrokeColor(navy)
    c.line(margin, ty - 5, margin + 100, ty - 5)
    
    ty -= 40
    draw_box(c, margin, ty - 120, w - 2*margin, 120, fill_color=light_gray, stroke_color=navy)
    
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    c.drawString(margin + 15, ty - 20, "I, the undersigned _____________________________, acting on behalf of Medicov s.c.,")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 15, ty - 40, "accept this proforma invoice under the stated terms and conditions,")
    c.drawString(margin + 15, ty - 53, "including the commitment to provide the stamped CMR delivery note.")
    
    c.setFont("Helvetica", 10)
    c.drawString(margin + 15, ty - 80, "Place: _____________________     Date: _____________________")
    c.drawString(margin + 15, ty - 105, "Signature (preceded by \"Approved for order\"):")
    
    # Footer
    ty = 80
    c.setStrokeColor(navy)
    c.setLineWidth(2)
    c.line(margin, ty, w - margin, ty)
    c.setFillColor(HexColor('#666666'))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(w/2, ty - 14, "VL MEDICAL SAS • SIRET 853 225 100 00025 • Capital: €1,000")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(w/2, ty - 26, "190 Rue Topaze, 13510 Éguilles, France")
    c.drawCentredString(w/2, ty - 38, "Phone: +33 6 18 24 40 13 • Email: jeanluc@aubagnac.com")
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(w/2, ty - 52, "This proforma invoice is not a final invoice and does not constitute a request for payment until formal acceptance.")
    
    c.setFont("Helvetica", 7)
    c.drawCentredString(w/2, 20, "Page 2/2")
    
    c.save()
    print(f"PDF généré : {OUTPUT}")
    print(f"Taille : {os.path.getsize(OUTPUT)} octets")

if __name__ == "__main__":
    main()
