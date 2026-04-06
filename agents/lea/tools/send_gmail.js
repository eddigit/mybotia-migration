const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

async function sendEmail(to, subject, body, from = 'coachdigitalparis@gmail.com') {
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

  const raw = Buffer.from(
    `From: ${from}\r\nTo: ${to}\r\nSubject: =?UTF-8?B?${Buffer.from(subject).toString('base64')}?=\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n${body}`
  ).toString('base64url');

  const res = await gmail.users.messages.send({ userId: 'me', requestBody: { raw } });
  console.log('Sent:', res.data.id);
}

const [,, to, subject, ...bodyParts] = process.argv;
const body = bodyParts.join(' ');
sendEmail(to, subject, body).catch(e => { console.error(e.message); process.exit(1); });
