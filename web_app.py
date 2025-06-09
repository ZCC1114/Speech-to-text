from flask import Flask, request, render_template_string
from ab_transcribe import transcribe, format_dialog
import os
import tempfile

app = Flask(__name__)

HTML = """
<!doctype html>
<title>AB Transcription</title>
<h1>Upload audio file</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=audio>
  <input type=submit value=Upload>
</form>
<pre>{{ dialog }}</pre>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    dialog = None
    if request.method == 'POST':
        file = request.files.get('audio')
        if file and file.filename:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                file.save(tmp.name)
                segments = transcribe(tmp.name)
                dialog = format_dialog(segments)
            os.unlink(tmp.name)
    return render_template_string(HTML, dialog=dialog)

if __name__ == '__main__':
    app.run(debug=True)
