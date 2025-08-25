# File: web_server.py

from flask import Flask, render_template_string, request, jsonify
import subprocess
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase (only on server)
try:
    firebase_config_json = os.environ.get("FIREBASE_CONFIG_JSON")
    if firebase_config_json:
        import json
        firebase_config = json.loads(firebase_config_json)
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully")
    else:
        print("❌ Firebase config not found")
        db = None
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    db = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UDICTI CLI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .command-form { background: #2a2a2a; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .output { background: #000; color: #0f0; padding: 15px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
        input, select, button { padding: 10px; margin: 5px; border-radius: 4px; border: none; }
        button { background: #0864af; color: white; cursor: pointer; }
        button:hover { background: #064a8e; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 UDICTI CLI</h1>
            <p>Developer Analytics & Workflow Toolkit for UDSM</p>
            <p><code>pip install udicti-cli</code></p>
        </div>
        
        <div class="command-form">
            <h3>Run UDICTI Commands</h3>
            <form id="commandForm">
                <select id="command" name="command">
                    <option value="--help">Show Help</option>
                    <option value="welcome">Welcome Message</option>
                    <option value="show devs">Show Developers</option>
                    <option value="join">Join Community</option>
                </select>
                <button type="submit">Run Command</button>
            </form>
        </div>
        
        <div id="output" class="output" style="display:none;"></div>
    </div>

    <script>
        document.getElementById('commandForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const command = document.getElementById('command').value;
            const outputDiv = document.getElementById('output');
            
            outputDiv.style.display = 'block';
            outputDiv.textContent = 'Running command...';
            
            try {
                const response = await fetch('/run-command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command })
                });
                const result = await response.json();
                outputDiv.textContent = result.output;
            } catch (error) {
                outputDiv.textContent = 'Error: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {'status': 'healthy', 'firebase': 'connected' if db else 'disconnected'}

# API Routes for CLI
@app.route('/api/log', methods=['POST'])
def api_log():
    """Log CLI usage events"""
    try:
        data = request.get_json()
        if db:
            db.collection('cli_logs').add({
                **data,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string
            })
        return jsonify({'status': 'logged'})
    except Exception as e:
        print(f"Log error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/developers', methods=['GET'])
def api_get_developers():
    """Get all developers"""
    try:
        if not db:
            return jsonify({'error': 'Database not available'}), 500
            
        developers_ref = db.collection("developers")
        docs = developers_ref.stream()

        devs = []
        for doc in docs:
            dev_data = doc.to_dict()
            dev_data["interests"] = dev_data.get("interests", [])
            dev_data["skills"] = dev_data.get("skills", [])
            
            if all(key in dev_data for key in ["name", "email", "github"]):
                devs.append(dev_data)

        return jsonify({'developers': devs, 'count': len(devs)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/developers', methods=['POST'])
def api_add_developer():
    """Add new developer"""
    try:
        if not db:
            return jsonify({'error': 'Database not available'}), 500
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'github']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Add to Firebase
        developer_data = {
            "name": data['name'],
            "email": data['email'],
            "github": data['github'],
            "interests": data.get('interests', []),
            "skills": data.get('skills', []),
            "joined_at": firestore.SERVER_TIMESTAMP
        }
        
        # Use email as document ID
        db.collection("developers").document(data['email']).set(developer_data)
        
        return jsonify({'success': True, 'message': 'Developer added successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-command', methods=['POST'])
def run_command():
    try:
        data = request.get_json()
        command = data.get('command', '--help')
        
        # Log web usage
        if db:
            db.collection('web_usage').add({
                'command': command,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string
            })
        
        # Run the UDICTI command
        result = subprocess.run(
            ['udicti'] + command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
            
        return jsonify({'output': output})
    except subprocess.TimeoutExpired:
        return jsonify({'output': 'Command timed out'}), 408
    except Exception as e:
        return jsonify({'output': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)