const { jsPDF } = require('jspdf');
const fs = require('fs');

const invoice = {
  number: "FA-2026-042",
  issueDate: "30/03/2026",
  dueDate: "30/03/2026",
  subtotal: 145,
  taxRate: 20,
  taxAmount: 29,
  total: 174,
  client: {
    company: "Association En Toute Franchise",
    contact: "Claude et Martine DONNETTE",
    email: "en.toutefranchise@wanadoo.fr",
    tel: "06 20 40 26 78",
    city: "France"
  },
  items: [
    {
      description: "Configuration serveur d'envoi securise + adresse no-reply dediee",
      quantity: 1,
      unitPrice: 69.00,
      total: 69.00
    },
    {
      description: "Enregistrement et configuration nom de domaine dedie aux envois",
      quantity: 1,
      unitPrice: 27.00,
      total: 27.00
    },
    {
      description: "Protocoles de securite email : SPF, DKIM, DMARC",
      quantity: 1,
      unitPrice: 49.00,
      total: 49.00
    }
  ]
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

const doc = new jsPDF();

// Header
doc.setFontSize(24);
doc.setTextColor(59, 130, 246);
doc.text("FACTURE", 20, 25);

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
doc.text(invoice.client.contact, 20, 75);
doc.text(invoice.client.email, 20, 82);
doc.text(`Tel: ${invoice.client.tel}`, 20, 89);

// Invoice details
doc.setFontSize(11);
doc.text("Details", 140, 60);
doc.setFontSize(10);
doc.text(`Date d'emission: ${invoice.issueDate}`, 140, 68);
doc.text(`Echeance: ${invoice.dueDate}`, 140, 75);
doc.text(`Paiement: Virement bancaire`, 140, 82);

// Table header
let y = 105;
doc.setFillColor(59, 130, 246);
doc.rect(20, y, 170, 10, 'F');
doc.setTextColor(255, 255, 255);
doc.setFontSize(10);
doc.text("Description", 25, y + 7);
doc.text("Qte", 120, y + 7);
doc.text("Prix HT", 140, y + 7);
doc.text("Total HT", 165, y + 7);

// Table rows
y += 15;
doc.setTextColor(40, 40, 40);
invoice.items.forEach((item, idx) => {
  // Description - handle long text
  const desc = item.description;
  doc.setFontSize(9);
  doc.text(desc, 25, y);
  doc.setFontSize(10);
  doc.text(String(item.quantity), 122, y);
  doc.text(`${item.unitPrice.toFixed(2)} EUR`, 138, y);
  doc.text(`${item.total.toFixed(2)} EUR`, 163, y);
  y += 12;
});

// Detail text for line 3 (SPF/DKIM/DMARC)
y += 2;
doc.setFontSize(8);
doc.setTextColor(80, 80, 80);
doc.text("Detail protocoles de securite :", 25, y);
y += 6;
doc.text("- SPF (Sender Policy Framework) : authentification des serveurs d'envoi autorises", 30, y);
y += 5;
doc.text("- DKIM (DomainKeys Identified Mail) : signatures cryptographiques des emails", 30, y);
y += 5;
doc.text("- DMARC (Domain-based Message Authentication) : politique anti-usurpation et rapports", 30, y);
y += 5;
doc.text("- Configuration et verification de la delivrabilite (test inbox, headers, scoring)", 30, y);

// Totals
y += 15;
doc.setFillColor(245, 245, 250);
doc.rect(120, y, 70, 40, 'F');

doc.setFontSize(10);
doc.setTextColor(100, 100, 100);
doc.text("Sous-total HT", 125, y + 10);
doc.text(`${invoice.subtotal.toFixed(2)} EUR`, 185, y + 10, { align: 'right' });

doc.text(`TVA (${invoice.taxRate}%)`, 125, y + 20);
doc.text(`${invoice.taxAmount.toFixed(2)} EUR`, 185, y + 20, { align: 'right' });

doc.setDrawColor(59, 130, 246);
doc.line(125, y + 25, 185, y + 25);

doc.setFontSize(12);
doc.setTextColor(59, 130, 246);
doc.text("Total TTC", 125, y + 35);
doc.text(`${invoice.total.toFixed(2)} EUR`, 185, y + 35, { align: 'right' });

// Payment info
y += 55;
doc.setFontSize(9);
doc.setTextColor(60, 60, 60);
doc.text("Coordonnees bancaires pour virement :", 20, y);
doc.setFontSize(10);
doc.text(`Beneficiaire: ${company.name}`, 20, y + 8);
doc.setFontSize(9);
doc.text(`IBAN: ${company.iban}`, 20, y + 16);
doc.text(`BIC: ${company.bic}`, 20, y + 23);

// Footer
doc.setFontSize(8);
doc.setTextColor(150, 150, 150);
doc.text(`${company.name} (${company.tradeName}) - SIRET ${company.siret}`, 105, 285, { align: 'center' });

// Save
const outputPath = '/home/gilles/.openclaw/workspace/factures/FA-2026-042-ETF.pdf';
const pdfBuffer = doc.output('arraybuffer');
fs.writeFileSync(outputPath, Buffer.from(pdfBuffer));

console.log(`PDF genere: ${outputPath}`);
console.log(`Total HT: ${invoice.subtotal.toFixed(2)} EUR`);
console.log(`TVA 20%: ${invoice.taxAmount.toFixed(2)} EUR`);
console.log(`Total TTC: ${invoice.total.toFixed(2)} EUR`);
