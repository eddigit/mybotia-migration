const { jsPDF } = require('jspdf');
const fs = require('fs');

// Données de la facture Art Royal
const invoice = {
  number: "FAC-202602-027",
  issueDate: "2026-02-06",
  dueDate: "2026-02-06",  // Échéance immédiate
  status: "SENT",
  subtotal: 180,
  taxRate: 20,
  taxAmount: 36,
  total: 216,
  client: {
    company: "Art Royal",
    firstName: "Tristant",
    lastName: "Llorca",
    email: "tristan.llorca@gmail.com",
    city: "Le Boulou",
    country: "France"
  },
  items: [{
    description: "Remboursements",
    quantity: 1,
    unitPrice: 180,
    total: 180
  }]
};

const company = {
  name: "Gilles Korzec",               // Entité juridique pour les virements
  tradeName: "Coach Digital Paris",     // Nom commercial
  siret: "83404919700028",
  email: "coachdigitalparis@gmail.com",
  address: "Paris, France",
  iban: "FR7616958000013308587025176",
  bic: "QNTOFRP1XXX"                   // Qonto
};

// Générer le PDF
const doc = new jsPDF();

// Header
doc.setFontSize(24);
doc.setTextColor(59, 130, 246);
doc.text("FACTURE", 20, 25);

doc.setFontSize(12);
doc.setTextColor(100, 100, 100);
doc.text(invoice.number, 20, 35);

// Company info - Entité juridique en premier
doc.setFontSize(11);
doc.setTextColor(40, 40, 40);
doc.text(company.name, 140, 22);  // "Gilles Korzec" - IMPORTANT pour virements
doc.setFontSize(9);
doc.setTextColor(100, 100, 100);
doc.text(company.tradeName, 140, 28);  // Nom commercial
doc.text(`SIRET: ${company.siret}`, 140, 35);
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
doc.text(`${invoice.client.firstName} ${invoice.client.lastName}`, 20, 75);
doc.text(invoice.client.email, 20, 82);
doc.text(`${invoice.client.city}, ${invoice.client.country}`, 20, 89);

// Invoice details
doc.setFontSize(11);
doc.text("Détails", 140, 60);
doc.setFontSize(10);
doc.text(`Date d'émission: ${invoice.issueDate}`, 140, 68);
doc.text(`Échéance: ${invoice.dueDate}`, 140, 75);
doc.text(`Paiement: Virement bancaire`, 140, 82);
doc.text(`Statut: Envoyée`, 140, 89);

// Table header
let y = 105;
doc.setFillColor(59, 130, 246);
doc.rect(20, y, 170, 10, 'F');
doc.setTextColor(255, 255, 255);
doc.setFontSize(10);
doc.text("Description", 25, y + 7);
doc.text("Qté", 120, y + 7);
doc.text("Prix HT", 140, y + 7);
doc.text("Total HT", 165, y + 7);

// Table rows
y += 15;
doc.setTextColor(40, 40, 40);
invoice.items.forEach(item => {
  doc.text(item.description, 25, y);
  doc.text(String(item.quantity), 122, y);
  doc.text(`${item.unitPrice.toFixed(2)} €`, 140, y);
  doc.text(`${item.total.toFixed(2)} €`, 165, y);
  y += 10;
});

// Totals
y += 10;
doc.setFillColor(245, 245, 250);
doc.rect(120, y, 70, 40, 'F');

doc.setFontSize(10);
doc.setTextColor(100, 100, 100);
doc.text("Sous-total HT", 125, y + 10);
doc.text(`${invoice.subtotal.toFixed(2)} €`, 180, y + 10, { align: 'right' });

doc.text(`TVA (${invoice.taxRate}%)`, 125, y + 20);
doc.text(`${invoice.taxAmount.toFixed(2)} €`, 180, y + 20, { align: 'right' });

doc.setDrawColor(59, 130, 246);
doc.line(125, y + 25, 185, y + 25);

doc.setFontSize(12);
doc.setTextColor(59, 130, 246);
doc.text("Total TTC", 125, y + 35);
doc.text(`${invoice.total.toFixed(2)} €`, 180, y + 35, { align: 'right' });

// Payment info
y += 55;
doc.setFontSize(9);
doc.setTextColor(60, 60, 60);
doc.text("Coordonnées bancaires pour virement:", 20, y);
doc.setFontSize(10);
doc.text(`Bénéficiaire: ${company.name}`, 20, y + 8);  // IMPORTANT
doc.setFontSize(9);
doc.text(`IBAN: ${company.iban}`, 20, y + 16);
doc.text(`BIC: ${company.bic}`, 20, y + 23);

// Footer
doc.setFontSize(8);
doc.setTextColor(150, 150, 150);
doc.text(`${company.name} (${company.tradeName}) - SIRET ${company.siret}`, 105, 285, { align: 'center' });

// Save
const outputPath = '/tmp/Facture_FAC-202602-027.pdf';
const pdfBuffer = doc.output('arraybuffer');
fs.writeFileSync(outputPath, Buffer.from(pdfBuffer));

console.log(`PDF généré: ${outputPath}`);
