from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Expecting JSON
    markdown_content = f"# Submission\n\nName: {data['name']}\n\nDetails: {data['details']}"
    
    output_path = Path("output.md")
    output_path.write_text(markdown_content)

    return jsonify({"status": "ok", "message": "Markdown file saved!"})

if __name__ == '__main__':
    app.run(debug=True)
