export default function handler(req, res) {
  let digits = null;

  if (req.body) {
    if (typeof req.body === 'object' && req.body.Digits) {
      digits = String(req.body.Digits);
    } else if (typeof req.body === 'string') {
      try {
        const params = new URLSearchParams(req.body);
        digits = params.get('Digits');
      } catch (e) {}
    }
  }

  if (!digits && req.query && req.query.Digits) {
    digits = String(req.query.Digits);
  }

  res.setHeader('Content-Type', 'text/xml');

  // If caller pressed 1, connect to contractor with call recording and whisper
  if (digits === '1') {
    return res.status(200).send(`<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial record="record-from-answer" timeout="20" action="https://handler.twilio.com/twiml/EH9c0189ec7805c1165f78120ccad5d9a0">
        <Number url="https://handler.twilio.com/twiml/EH0dce14f1bcec5642b212550fadcf2fab">+12082215313</Number>
    </Dial>
</Response>`);
  }

  // Initial call: Play spam filter greeting and prompt to press 1
  return res.status(200).send(`<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather numDigits="1" timeout="5" action="/api/incoming-call" method="POST">
        <Say voice="Polly.Joanna">Thank you for calling Pocatello Tree Service. To connect with our local team for a free estimate, please press 1.</Say>
    </Gather>
    <Say voice="Polly.Joanna">We did not receive a response. Goodbye.</Say>
    <Hangup/>
</Response>`);
}
