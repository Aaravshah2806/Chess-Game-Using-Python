from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import chess_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_engine import ChessEngine

app = Flask(__name__, static_folder='../simple_frontend', static_url_path='')
CORS(app)  # Enable CORS

# Global Game Instance
game_engine = ChessEngine()

import subprocess
import sys

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/launch', methods=['POST'])
def launch_game():
    try:
        # Run main.py in a separate process
        # We use sys.executable to ensure we use the same python interpreter
        subprocess.Popen([sys.executable, 'main.py'])
        return jsonify({"success": True, "message": "Game launched!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/new_game', methods=['POST'])
def new_game():
    global game_engine
    game_engine = ChessEngine()
    return jsonify({"message": "New game started", "state": game_engine.get_state()})

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(game_engine.get_state())

@app.route('/move', methods=['POST'])
def move_piece():
    data = request.json
    start_pos = data.get('start')
    end_pos = data.get('end')
    
    if not start_pos or not end_pos:
        return jsonify({"success": False, "message": "Missing start or end position"}), 400

    success, message = game_engine.move_piece(start_pos, end_pos)
    
    if success:
        return jsonify({"success": True, "message": message, "state": game_engine.get_state()})
    else:
        return jsonify({"success": False, "message": message}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
