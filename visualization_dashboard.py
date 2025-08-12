#!/usr/bin/env python3
"""
Local File Browser Dashboard for Cyberwheel Visualizations
Runs on port 8051 to browse available visualization data
"""

import os
import http.server
import socketserver
from urllib.parse import unquote
import json

class CyberwheelFileHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/rds/general/user/moa324/home/projects/cyberwheel", **kwargs)
    
    def do_GET(self):
        if self.path == '/api/experiments':
            self.send_api_response()
        elif self.path == '/' or self.path == '/index.html':
            self.send_dashboard()
        else:
            super().do_GET()
    
    def send_api_response(self):
        # Collect experiment data
        data_dir = "/rds/general/user/moa324/home/projects/cyberwheel/data"
        experiments = {
            "training": [],
            "models": [],
            "graphs": []
        }
        
        # Check training runs
        runs_dir = os.path.join(data_dir, "runs")
        if os.path.exists(runs_dir):
            experiments["training"] = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
        
        # Check models
        models_dir = os.path.join(data_dir, "models")
        if os.path.exists(models_dir):
            experiments["models"] = [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
        
        # Check graphs
        graphs_dir = os.path.join(data_dir, "graphs")
        if os.path.exists(graphs_dir):
            experiments["graphs"] = [d for d in os.listdir(graphs_dir) if os.path.isdir(os.path.join(graphs_dir, d))]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(experiments).encode())
    
    def send_dashboard(self):
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Cyberwheel Data Browser</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .section h2 { color: #444; margin-top: 0; }
        .experiment-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .experiment-item { background: #f9f9f9; padding: 10px; border-radius: 5px; border-left: 4px solid #007acc; }
        .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0; }
        .service { background: #e8f4fd; padding: 15px; border-radius: 5px; text-align: center; }
        .service a { color: #007acc; text-decoration: none; font-weight: bold; }
        .service a:hover { text-decoration: underline; }
        .status { color: #666; font-style: italic; }
        .count { background: #007acc; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Cyberwheel Data Browser</h1>
        
        <div class="services">
            <div class="service">
                <h3>🔥 TensorBoard</h3>
                <a href="http://localhost:6006" target="_blank">Training Metrics</a>
                <div class="status">Port 6006</div>
            </div>
            <div class="service">
                <h3>🌐 Interactive Visualizer</h3>
                <a href="http://localhost:8050" target="_blank">Network Animations</a>
                <div class="status">Port 8050</div>
            </div>
            <div class="service">
                <h3>📂 File Browser</h3>
                <a href="http://localhost:8051" target="_blank">Data Explorer</a>
                <div class="status">Port 8051 (This Page)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Training Experiments <span class="count" id="training-count">0</span></h2>
            <div id="training-experiments" class="experiment-list">
                Loading...
            </div>
        </div>
        
        <div class="section">
            <h2>🤖 Trained Models <span class="count" id="models-count">0</span></h2>
            <div id="model-experiments" class="experiment-list">
                Loading...
            </div>
        </div>
        
        <div class="section">
            <h2>🎮 Interactive Visualizations <span class="count" id="graphs-count">0</span></h2>
            <div id="graph-experiments" class="experiment-list">
                Loading...
            </div>
        </div>
        
        <div class="section">
            <h2>🚀 Quick Commands</h2>
            <pre style="background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto;">
# Start all services
launch_local_visualization.bat

# Individual services
tensorboard --logdir=data/runs --port=6006
python -m cyberwheel visualizer 8050
python visualization_dashboard.py

# Generate new visualizations
python -m cyberwheel visualizer --experiment-name MODEL_NAME --graph-name GRAPH_NAME
            </pre>
        </div>
    </div>
    
    <script>
        fetch('/api/experiments')
            .then(response => response.json())
            .then(data => {
                // Update training experiments
                const trainingDiv = document.getElementById('training-experiments');
                document.getElementById('training-count').textContent = data.training.length;
                trainingDiv.innerHTML = data.training.length > 0 
                    ? data.training.map(exp => `<div class="experiment-item">${exp}</div>`).join('')
                    : '<div class="status">No training experiments found</div>';
                
                // Update models
                const modelsDiv = document.getElementById('model-experiments');
                document.getElementById('models-count').textContent = data.models.length;
                modelsDiv.innerHTML = data.models.length > 0 
                    ? data.models.map(exp => `<div class="experiment-item">${exp}</div>`).join('')
                    : '<div class="status">No trained models found</div>';
                
                // Update graphs
                const graphsDiv = document.getElementById('graph-experiments');
                document.getElementById('graphs-count').textContent = data.graphs.length;
                graphsDiv.innerHTML = data.graphs.length > 0 
                    ? data.graphs.map(exp => `<div class="experiment-item">${exp}</div>`).join('')
                    : '<div class="status">No interactive visualizations found</div>';
            })
            .catch(error => {
                console.error('Error loading experiments:', error);
                document.getElementById('training-experiments').innerHTML = '<div class="status">Error loading data</div>';
                document.getElementById('model-experiments').innerHTML = '<div class="status">Error loading data</div>';
                document.getElementById('graph-experiments').innerHTML = '<div class="status">Error loading data</div>';
            });
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

def main():
    PORT = 8051
    print(f"🌐 Starting Cyberwheel File Browser on port {PORT}")
    print(f"📂 Browse your data at: http://localhost:{PORT}")
    print("🔥 TensorBoard: http://localhost:6006")
    print("🎮 Interactive Visualizer: http://localhost:8050")
    print("\nPress Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), CyberwheelFileHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
