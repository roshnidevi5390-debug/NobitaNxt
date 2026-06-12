from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

VALID_API_KEY = "VerifiedNxt847001"

@app.route('/', methods=['GET'])
def search():
    key = request.args.get('key')
    
    if not key:
        return jsonify({"success": False, "error": "Missing 'key' parameter"}), 401
    
    if key != VALID_API_KEY:
        return jsonify({"success": False, "error": "Invalid API key"}), 401
    
    query = request.args.get('query')
    if not query:
        return jsonify({"success": False, "error": "Missing 'query' parameter"}), 400
    
    try:
        response = requests.get(
            'https://rootx-osint.in/',
            params={'type': 'tg_num', 'key': 'Surya_Hacker', 'query': query},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return jsonify({
                    "success": True,
                    "tg_id": data.get('tg_id', query),
                    "country": data.get('country', 'India'),
                    "country_code": data.get('country_code', '+91'),
                    "number": data.get('number'),
                    "developer": "@VerifiedNxt"
                })
        return jsonify({"success": False, "error": "No data found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
