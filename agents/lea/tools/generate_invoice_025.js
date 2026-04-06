const { jsPDF } = require('jspdf');
const fs = require('fs');

// Données EXACTES du CRM - FAC-202602-025 Art Royal
const invoice = {
  number: "FAC-202602-025",
  issueDate: "2026-02-05",
  dueDate: "2026-02-05",  // Échéance immédiate
  status: "DRAFT",
  subtotal: 190,
  taxRate: 20,
  taxAmount: 38,
  total: 228,
  paymentMethod: "Virement bancaire",
  client: {
    company: "Art Royal",
    firstName: "Tristant",
    lastName: "Llorca",
    email: "tristan.llorca@gmail.com",
    city: "Le Boulou",
    country: "France"
  },
  items: [{
    description: "Solde tokens finalisation plateforme Art Royal",
    details: `Cette facture correspond aux deux reliquats qui avaient eu sur décembre, avant les fêtes, dont je t'avais parlé, mais qu'on avait mis en stand-by, et le reliquat de janvier pour les finisations.

Aujourd'hui, le site est en ligne et est finalisé, opérationnel.

Pour rappel, ces montants sont des remboursements d'IA token que j'ai utilisé. Je n'ai pas compté mes horaires.`,
    quantity: 1,
    unitPrice: 190,
    total: 190
  }]
};

const company = {
  name: "Gilles Korzec",
  tradeName: "Coach Digital Paris",
  siret: "83404919700028",
  email: "coachdigitalparis@gmail.com",
  address: "Paris, France",
  iban: "FR7616958000013308587025176",
  bic: "QNTOFRP1XXX"
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

// Company info - Entité juridique
doc.setFontSize(11);
doc.setTextColor(40, 40, 40);
doc.text(company.name, 140, 20);
doc.setFontSize(9);
doc.setTextColor(100, 100, 100);
doc.text(company.tradeName, 140, 26);
doc.text(`SIRET: ${company.siret}`, 140, 32);
doc.text(company.email, 140, 38);

// Separator
doc.setDrawColor(200, 200, 200);
doc.line(20, 48, 190, 48);

// Client info
doc.setFontSize(11);
doc.setTextColor(40, 40, 40);
doc.text("Client", 20, 58);
doc.setFontSize(10);
doc.text(invoice.client.company, 20, 66);
doc.text(`${invoice.client.firstName} ${invoice.client.lastName}`, 20, 73);
doc.text(invoice.client.email, 20, 80);
doc.text(`${invoice.client.city}, ${invoice.client.country}`, 20, 87);

// Invoice details
doc.setFontSize(11);
doc.text("Détails", 140, 58);
doc.setFontSize(10);
doc.text(`Date d'émission: ${invoice.issueDate}`, 140, 66);
doc.text(`Échéance: Immédiate`, 140, 73);
doc.text(`Paiement: ${invoice.paymentMethod}`, 140, 80);

// Table header
let y = 100;
doc.setFillColor(59, 130, 246);
doc.rect(20, y, 170, 10, 'F');
doc.setTextColor(255, 255, 255);
doc.setFontSize(10);
doc.text("Description", 25, y + 7);
doc.text("Qté", 130, y + 7);
doc.text("Prix HT", 150, y + 7);
doc.text("Total HT", 175, y + 7);

// Table rows avec détails
y += 15;
doc.setTextColor(40, 40, 40);

invoice.items.forEach(item => {
  // Description principale
  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.text(item.description, 25, y);
  
  // Quantité, prix, total
  doc.setFont('helvetica', 'normal');
  doc.text(String(item.quantity), 132, y);
  doc.text(`${item.unitPrice.toFixed(2)} €`, 150, y);
  doc.text(`${item.total.toFixed(2)} €`, 175, y);
  
  y += 8;
  
  // Détails (texte plus petit, gris)
  if (item.details) {
    doc.setFontSize(8);
    doc.setTextColor(100, 100, 100);
    const lines = doc.splitTextToSize(item.details, 100);
    lines.forEach(line => {
      doc.text(line, 25, y);
      y += 4;
    });
    y += 4;
  }
});

// Totals
y += 10;
doc.setFillColor(245, 245, 250);
doc.rect(120, y, 70, 40, 'F');

doc.setFontSize(10);
doc.setTextColor(100, 100, 100);
doc.text("Sous-total HT", 125, y + 10);
doc.setTextColor(40, 40, 40);
doc.text(`${invoice.subtotal.toFixed(2)} €`, 185, y + 10, { align: 'right' });

doc.setTextColor(100, 100, 100);
doc.text(`TVA (${invoice.taxRate}%)`, 125, y + 20);
doc.setTextColor(40, 40, 40);
doc.text(`${invoice.taxAmount.toFixed(2)} €`, 185, y + 20, { align: 'right' });

doc.setDrawColor(59, 130, 246);
doc.line(125, y + 25, 185, y + 25);

doc.setFontSize(12);
doc.setTextColor(59, 130, 246);
doc.setFont('helvetica', 'bold');
doc.text("Total TTC", 125, y + 35);
doc.text(`${invoice.total.toFixed(2)} €`, 185, y + 35, { align: 'right' });

// Payment info
y += 55;
doc.setFont('helvetica', 'normal');
doc.setFontSize(10);
doc.setTextColor(60, 60, 60);
doc.text("Coordonnées bancaires pour virement:", 20, y);
doc.setFontSize(11);
doc.setFont('helvetica', 'bold');
doc.text(`Bénéficiaire: ${company.name}`, 20, y + 8);
doc.setFont('helvetica', 'normal');
doc.setFontSize(10);
doc.text(`IBAN: ${company.iban}`, 20, y + 16);
doc.text(`BIC: ${company.bic}`, 20, y + 23);

// Footer
doc.setFontSize(8);
doc.setTextColor(150, 150, 150);
doc.text(`${company.name} (${company.tradeName}) - SIRET ${company.siret}`, 105, 285, { align: 'center' });

// Save
const outputPath = '/tmp/Facture_FAC-202602-025_ArtRoyal.pdf';
const pdfBuffer = doc.output('arraybuffer');
fs.writeFileSync(outputPath, Buffer.from(pdfBuffer));

console.log(`PDF généré: ${outputPath}`);
