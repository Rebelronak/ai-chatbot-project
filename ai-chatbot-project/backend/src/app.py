from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os
import json
import random
import re
from ai_response import get_ai_response

# Enhanced database connection with better error handling
def load_database():
    """Load database with comprehensive error handling"""
    try:
        # Try to import the database utility
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        database_path = os.path.join(parent_dir, 'database')
        
        if database_path not in sys.path:
            sys.path.append(database_path)
            
        # Try to import PriyeAIDatabase
        from db_utils import PriyeAIDatabase  # noqa: E402
        db = PriyeAIDatabase()
        print("✅ Enhanced database connected successfully!")
        
        # Test database
        stats = db.get_statistics()
        print(f"📊 Database stats: {stats['total_patterns']} patterns, {stats['total_responses']} responses")
        
        return db
        
    except ImportError as e:
        print(f"⚠️ Database import failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

# Initialize database
priye_db = load_database()

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        privacy_mode = data.get('privacy_mode', False)
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"📩 Received: '{user_message}' (Privacy: {privacy_mode}, User: {user_id})")
        
        # Get AI response using enhanced function
        ai_response = get_ai_response(user_message)
        
        # Only save conversation if NOT in privacy mode
        if not privacy_mode and priye_db:
            try:
                priye_db.save_conversation(user_id, user_message, ai_response)
                print("💾 Conversation saved to database")
            except Exception as e:
                print(f"⚠️ Save error: {e}")
        else:
            print("🔒 Privacy mode: Conversation not saved")
        
        print(f"📤 Sending response: '{ai_response[:50]}...'")
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'privacy_mode': privacy_mode,
            'source': 'database' if priye_db else 'fallback'
        })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            'response': 'Sorry, main abhi kuch technical issues face kar rahi hun. Thoda baad try kariye!',
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database_connected': priye_db is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get database statistics"""
    if priye_db:
        try:
            stats = priye_db.get_statistics()
            return jsonify({
                'status': 'success',
                'stats': stats
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'error': 'Database not connected'
        }), 500

# Add these routes BEFORE the "if __name__ == '__main__':" line

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'name': 'Priye.AI Backend',
        'version': '1.0.0',
        'creator': 'Ronak Kanani',
        'status': 'running',
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/api/health (GET)',
            'stats': '/api/stats (GET)'
        },
        'database_connected': priye_db is not None
    })

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return '', 204  # No content response

if __name__ == '__main__':
    print("🚀 Starting Priye.AI Backend...")
    print(f"📊 Database available: {priye_db is not None}")
    
    if priye_db:
        try:
            stats = priye_db.get_statistics()
            print(f"📈 Loaded {stats['total_patterns']} patterns and {stats['total_responses']} responses")
        except:
            print("⚠️ Could not load database stats")
    
    print("🌐 Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)