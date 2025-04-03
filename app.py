from flask import Flask, request, jsonify
import requests
import base64
import json

app = Flask(__name__)

# Home Route (Fix for 404 Error)
@app.route('/')
def home():
    return "Flask server is running! Use /update_link to update JSON file."

# Yahan apna GitHub Token aur Repo Details bharna
GITHUB_TOKEN = "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"
REPO_OWNER = "Vaibhav905036"
REPO_NAME = "Link-updator"
FILE_PATH = "vaibhav.json"

@app.route('/update_link', methods=['POST'])
def update_link():
    new_link = request.form.get('link')
    if not new_link:
        return jsonify({'error': 'No link provided'}), 400

    # Get current content from GitHub
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data['sha']
        content = base64.b64decode(file_data['content']).decode('utf-8')
    else:
        sha = None
        content = '[]'  

    # Update content
    content_list = json.loads(content)
    content_list.append(new_link)
    updated_content = json.dumps(content_list, indent=2)
    updated_content_base64 = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

    # Send update request to GitHub
    payload = {'message': 'Update vaibhav.json', 'content': updated_content_base64, 'branch': 'main'}
    if sha:
        payload['sha'] = sha

    update_response = requests.put(url, headers=headers, json=payload)
    if update_response.status_code in [200, 201]:
        return jsonify({'message': 'File updated successfully'})
    else:
        return jsonify({'error': 'Failed to update file', 'details': update_response.json()}), update_response.status_code

if __name__ == '__main__':
    app.run(debug=True)
    
