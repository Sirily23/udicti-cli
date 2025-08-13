from flask import Flask, render_template_string, request, jsonify
import subprocess
import os

app = Flask(__name__)

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
        </div>
        
        <div class="command-form">
            <h3>Run UDICTI Commands</h3>
            <form id="commandForm">
                <select id="command" name="command">
                    <option value="--help">Show Help</option>
                    <option value="welcome">Welcome Message</option>
                    <option value="show devs">Show Developers</option>
                    <option value="dashboard personal">Personal Dashboard</option>
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
    return {'status': 'healthy'}

@app.route('/run-command', methods=['POST'])
def run_command():
    try:
        data = request.get_json()
        command = data.get('command', '--help')
        
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