require('dotenv').config();
const express = require('express');
const twilio  = require('twilio');
const path    = require('path');

const app    = express();
const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public'))); // serves public/index.html at "/"

app.post('/api/send-sos', async (req, res) => {
  const { contacts, location, timestamp } = req.body;

  if (!Array.isArray(contacts) || contacts.length === 0) {
    return res.status(400).json({ status: 'error', message: 'No contacts provided' });
  }

  const message = `SOS ALERT!\nTime: ${timestamp}\nLocation: ${location}\nThis is an automated emergency message.`;

  try {
    const results = await Promise.all(
      contacts.map(to =>
        client.messages.create({
          body: message,
          from: process.env.TWILIO_FROM_NUMBER,
          to
        })
      )
    );
    console.log('SMS sent:', results.map(r => r.sid));
    res.json({ status: 'ok', sent: results.length });
  } catch (err) {
    console.error('Twilio error:', err.message);
    res.status(500).json({ status: 'error', message: err.message });
  }
});

app.listen(3000, () => console.log('SOS server running on http://localhost:3000'));
