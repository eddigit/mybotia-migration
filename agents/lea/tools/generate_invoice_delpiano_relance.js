const { jsPDF } = require('jspdf');
const fs = require('fs');

const invoice = {
  number: "PRO-2026-002",
  issueDate: "30/03/2026",
  dueDate: "15/04/2026",
  subtotal: 500,
  taxRate: 20,
  taxAmount: 100,
  total: 600,
  client: {
    company: "Cabinet Clement Delpiano",
    contact: "Valerie Clement",
    email: "valerieclement8@gmail.com",
    city: "France"
  },
  items: [
    {
      description: "Acompte sur solde facture FA-2026-032",
      detail: "Regularisation partielle - site de presentation en ligne depuis novembre 2025",
      quantity: 1,
      unitPrice: 500.00,
      total: 500.00
    }
  ]
};

const company = {
  name: "Gilles Korzec",
  tradeName: "Coach Digital Paris",
  siret: "83404919700028",
  email: "coachdigitalparis@gmail.com",
  address: "Paris, France",
  iban: "FR76 1695 8000 0133 0858 7025 176",
  bic: "QNTOFRP1XXX"
};

const doc = new jsPDF();

// PROFORMA header
doc.setFontSize(24);
doc.setTextColor(59, 130, 246);
doc.text("PROFORMA", 20, 25);

doc.setFontSize(12);
doc.setTextColor(100, 100, 100);
doc.text(invoice.number, 20, 35);

// Company info
doc.setFontSize(11);
doc.setTextColor(40, 40, 40);
doc.text(company.name, 140, 22);
doc.setFontSize(9);
doc.setTextColor(100, 100, 100);
doc.text(company.tradeName, 140, 28);
doc.text("SIRET: " + company.siret, 140, 35);
doc.text(company.email, 140, 42);

// Separator
doc.setDrawColor(200, 200, 200);
doc.line(20, 50, 190, 50);

// Client info
doc.setFontSize(11);
doc.setTextColor(40, 40, 40);
doc.text("Client", 20, 60);
doc.setFontSize(10);
doc.text(invoice.client.company, 20, 68);
doc.text(invoice.client.contact, 20, 75);
doc.text(invoice.client.email, 20, 82);

// Invoice details
doc.setFontSize(11);
doc.text("Details", 140, 60);
doc.setFontSize(10);
doc.text("Date d'emission: " + invoice.issueDate, 140, 68);
doc.text("Echeance: " + invoice.dueDate, 140, 75);
doc.text("Paiement: Virement bancaire", 140, 82);

// Table header
let y = 100;
doc.setFillColor(59, 130, 246);
doc.rect(20, y, 170, 10, 'F');
doc.setTextColor(255, 255, 255);
doc.setFontSize(10);
doc.text("Description", 25, y + 7);
doc.text("Qte", 120, y + 7);
doc.text("Prix HT", 140, y + 7);
doc.text("Total HT", 165, y + 7);

// Table row
y += 15;
doc.setTextColor(40, 40, 40);
doc.setFontSize(9);
doc.text(invoice.items[0].description, 25, y);
y += 6;
doc.setFontSize(8);
doc.setTextColor(80, 80, 80);
doc.text(invoice.items[0].detail, 25, y);
doc.setFontSize(10);
doc.setTextColor(40, 40, 40);
doc.text("1", 122, y - 6);
doc.text("500.00 EUR", 136, y - 6);
doc.text("500.00 EUR", 161, y - 6);

// Context note
y += 15;
doc.setFontSize(9);
doc.setTextColor(80, 80, 80);
doc.text("Contexte : Le site de presentation du cabinet est en ligne depuis novembre 2025 sur un", 25, y);
y += 5;
doc.text("hebergement dedie maintenu a nos frais. La validation finale, prevue en debut d'annee,", 25, y);
y += 5;
doc.text("est toujours en attente. Cette proforma couvre un acompte de regularisation sur le solde", 25, y);
y += 5;
doc.text("de la facture FA-2026-032 (solde restant : 1 700 EUR).", 25, y);

// Totals
y += 15;
doc.setFillColor(245, 245, 250);
doc.rect(120, y, 70, 40, 'F');

doc.setFontSize(10);
doc.setTextColor(100, 100, 100);
doc.text("Sous-total HT", 125, y + 10);
doc.text("500.00 EUR", 185, y + 10, { align: 'right' });

doc.text("TVA (20%)", 125, y + 20);
doc.text("100.00 EUR", 185, y + 20, { align: 'right' });

doc.setDrawColor(59, 130, 246);
doc.line(125, y + 25, 185, y + 25);

doc.setFontSize(12);
doc.setTextColor(59, 130, 246);
doc.text("Total TTC", 125, y + 35);
doc.text("600.00 EUR", 185, y + 35, { align: 'right' });

// Payment info
y += 55;
doc.setFontSize(9);
doc.setTextColor(60, 60, 60);
doc.text("Coordonnees bancaires pour virement :", 20, y);
doc.setFontSize(10);
doc.text("Beneficiaire: " + company.name, 20, y + 8);
doc.setFontSize(9);
doc.text("IBAN: " + company.iban, 20, y + 16);
doc.text("BIC: " + company.bic, 20, y + 23);

// Footer
doc.setFontSize(8);
doc.setTextColor(150, 150, 150);
doc.text(company.name + " (" + company.tradeName + ") - SIRET " + company.siret, 105, 285, { align: 'center' });

// Save
const outputPath = '/home/gilles/.openclaw/workspace/factures/PRO-2026-002-ClementDelpiano.pdf';
const pdfBuffer = doc.output('arraybuffer');
fs.writeFileSync(outputPath, Buffer.from(pdfBuffer));
console.log("PDF genere: " + outputPath);
