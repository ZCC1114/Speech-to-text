const fs = require('fs');
const path = require('path');
const { Deepgram } = require('@deepgram/sdk');

const apiKey = process.env.DEEPGRAM_API_KEY;
if (!apiKey) {
  console.error('DEEPGRAM_API_KEY environment variable not set');
  process.exit(1);
}

const dgClient = new Deepgram(apiKey);

async function transcribeFile(filePath) {
  const mime = 'audio/' + path.extname(filePath).slice(1);
  const buffer = fs.readFileSync(filePath);
  const { results } = await dgClient.transcription.preRecorded({ buffer, mimetype: mime }, { punctuate: true, diarize: true });
  const words = results.channels[0].alternatives[0].words;

  const lines = [];
  let currentSpeaker = null;
  let textBuffer = [];
  const speakerMap = {};
  let nextLabel = 'A';

  const labelFor = (spk) => {
    if (!(spk in speakerMap)) {
      speakerMap[spk] = nextLabel;
      nextLabel = nextLabel === 'A' ? 'B' : 'A';
    }
    return speakerMap[spk];
  };

  for (const w of words) {
    if (currentSpeaker === null) currentSpeaker = w.speaker;
    if (w.speaker !== currentSpeaker) {
      lines.push(`${labelFor(currentSpeaker)}: ${textBuffer.join(' ')}`);
      textBuffer = [w.word];
      currentSpeaker = w.speaker;
    } else {
      textBuffer.push(w.word);
    }
  }
  if (textBuffer.length) {
    lines.push(`${labelFor(currentSpeaker)}: ${textBuffer.join(' ')}`);
  }
  return lines.join('\n');
}

if (require.main === module) {
  if (process.argv.length < 3) {
    console.error('Usage: node dg_transcribe.js <audio_path>');
    process.exit(1);
  }
  transcribeFile(process.argv[2]).then(dialog => {
    console.log(dialog);
  }).catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

module.exports = { transcribeFile };
