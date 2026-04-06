const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

async function sendEmailWithAttachments(to, subject, body, attachments, from = 'coachdigitalparis@gmail.com') {
  const tokenFiles = {
    'coachdigitalparis@gmail.com': 'gmail-token-coachdigital.json',
    'leacoachdigital@gmail.com': 'gmail-token-leacoachdigital.json',
    'gilleskorzec@gmail.com': 'gmail-token-gilleskorzec.json',
  };

  const tokenFile = tokenFiles[from] || 'gmail-token-coachdigital.json';
  const creds = JSON.parse(fs.readFileSync(path.join(__dirname, 'gmail-credentials.json')));
  const token = JSON.parse(fs.readFileSync(path.join(__dirname, tokenFile)));

  const { client_id, client_secret } = creds.installed || creds.web;
  const oauth2 = new google.auth.OAuth2(client_id, client_secret);
  oauth2.setCredentials(token);

  const gmail = google.gmail({ version: 'v1', auth: oauth2 });

  const boundary = 'boundary_' + Date.now();
  
  let message = '';
  message += `From: ${from}\r\n`;
  message += `To: ${to}\r\n`;
  message += `Subject: =?UTF-8?B?${Buffer.from(subject).toString('base64')}?=\r\n`;
  message += `MIME-Version: 1.0\r\n`;
  message += `Content-Type: multipart/mixed; boundary="${boundary}"\r\n\r\n`;
  
  // Body
  message += `--${boundary}\r\n`;
  message += `Content-Type: text/plain; charset=UTF-8\r\n\r\n`;
  message += body + '\r\n\r\n';
  
  // Attachments
  for (const att of attachments) {
    const filename = att.name;
    const content = fs.readFileSync(att.path);
    const b64 = content.toString('base64');
    
    message += `--${boundary}\r\n`;
    message += `Content-Type: image/jpeg; name="${filename}"\r\n`;
    message += `Content-Disposition: attachment; filename="${filename}"\r\n`;
    message += `Content-Transfer-Encoding: base64\r\n\r\n`;
    message += b64 + '\r\n';
  }
  
  message += `--${boundary}--`;

  const raw = Buffer.from(message).toString('base64url');

  const res = await gmail.users.messages.send({ userId: 'me', requestBody: { raw } });
  console.log('Sent:', res.data.id);
}

// Parse args: node script.js to subject bodyFile att1path:att1name att2path:att2name ...
const args = process.argv.slice(2);
const to = args[0];
const subject = args[1];
const bodyFile = args[2];
const body = fs.readFileSync(bodyFile, 'utf8');
const attachments = args.slice(3).map(a => {
  const [p, n] = a.split(':');
  return { path: p, name: n };
});

sendEmailWithAttachments(to, subject, body, attachments).catch(e => { console.error(e.message); process.exit(1); });
