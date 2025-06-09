const express = require('express');
const multer = require('multer');
const fs = require('fs');
const { transcribeFile } = require('./dg_transcribe');

const app = express();
const upload = multer({ dest: 'uploads/' });

const FORM = `<!doctype html>
<title>AB Transcription</title>
<h1>Upload audio file</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="audio" />
  <input type="submit" value="Upload" />
</form>`;

app.get('/', (req, res) => res.send(FORM));

app.post('/', upload.single('audio'), async (req, res) => {
  if (!req.file) return res.status(400).send('No file uploaded');
  try {
    const dialog = await transcribeFile(req.file.path);
    fs.unlinkSync(req.file.path);
    res.send(`<pre>${dialog}</pre>`);
  } catch (err) {
    res.status(500).send('Error: ' + err.message);
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Visit http://localhost:${port}`));
