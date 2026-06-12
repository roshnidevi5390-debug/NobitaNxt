from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔐 Your API Key
VALID_API_KEY = "VerifiedNxt847001"

@app.route('/', methods=['GET'])
def search():
    # Key check - MUST have
    key = request.args.get('key')
    
    if not key:
        return jsonify({
            "success": False,
            "error": "Missing 'key' parameter"
        }), 401
    
    if key != VALID_API_KEY:
        return jsonify({
            "success": False,
            "error": "Invalid API key"
        }), 401
    
    # Query check
    query = request.args.get('query')
    
    if not query:
        return jsonify({
            "success": False,
            "error": "Missing 'query' parameter. Use ?key=VerifiedNxt847001&query=6624927068"
        }), 400
    
    try:
        # Real API call
        response = requests.get(
            'https://rootx-osint.in/',
            params={
                'type': 'tg_num',
                'key': 'Surya_Hacker',  # Internal key
                'query': query
            },
            timeout=10
        )
        
        if response.status_code == 200:
            real_data = response.json()
            
            if real_data.get('success'):
                return jsonify({
                    "success": True,
                    "tg_id": real_data.get('tg_id', query),
                    "country": real_data.get('country', 'India'),
                    "country_code": real_data.get('country_code', '+91'),
                    "number": real_data.get('number'),
                    "developer": "@VerifiedNxt"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "No data found for this query"
                }), 404
        else:
            return jsonify({
                "success": False,
                "error": f"Real API error: {response.status_code}"
            }), 502
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch data: {str(e)}"
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
