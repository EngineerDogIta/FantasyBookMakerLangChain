import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte

# Configurazione
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = 'user_data'

# Crea la cartella per i dati utente se non esiste
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_user_file_path(user_id):
    """Restituisce il percorso del file per un determinato utente"""
    return os.path.join(app.config['UPLOAD_FOLDER'], f'user_{user_id}.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/save', methods=['POST'])
def save_content():
    """Salva il contenuto sul server"""
    try:
        data = request.get_json()
        user_id = data.get('userId', 'default')
        content = data.get('content', '')
        
        if not content:
            return jsonify({'success': False, 'error': 'Nessun contenuto fornito'}), 400
        
        # Salva il contenuto in un file
        file_path = get_user_file_path(user_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'content': content,
                'last_updated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Contenuto salvato con successo',
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load', methods=['GET'])
def load_content():
    """Carica il contenuto dal server"""
    try:
        user_id = request.args.get('userId', 'default')
        file_path = get_user_file_path(user_id)
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': True,
                'content': '',
                'last_updated': None
            })
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'success': True,
            'content': data.get('content', ''),
            'last_updated': data.get('last_updated')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
