from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Expecting JSON
    # Build markdown content from new schema
    sectors = data.get('relevant_sectors', [])
    sectors_md = ''.join(f"- {sector}\n" for sector in sectors)
    markdown_content = (
        f"# Submission\n\n"
        f"**Location:** {data.get('location', '')}\n\n"
        f"**Planning Horizon:** {data.get('planning_horizon', '')}\n\n"
        f"**Available Investment:** {data.get('available_investment', '')} EUR\n\n"
        f"**Relevant Sectors:**\n"
        f"{sectors_md}"
    )
    output_path = Path("output.md")
    output_path.write_text(markdown_content)

    return jsonify({"status": "ok", "message": "Markdown file saved!"})

if __name__ == '__main__':
    app.run(debug=True)
