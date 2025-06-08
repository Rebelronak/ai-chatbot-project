import json
import os
import random
import re
from datetime import datetime
from typing import Optional, Dict, List, Any

class PriyeAIDatabase:
    def __init__(self):
        # Get the directory where this script is located
        self.db_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(self.db_dir, 'db.json')
        
        print(f"🔍 Looking for database at: {self.db_file}")
        
        self.data = self.load_database()
        print(f"✅ Database loaded successfully!")

    def load_database(self) -> dict:
        """Load database from JSON file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"📊 Database loaded from: {self.db_file}")
                return data
            else:
                print(f"❌ Database file not found at: {self.db_file}")
                print("Creating new database...")
                default_data = {
                    "messages": [],
                    "knowledge_base": {}
                }
                self.save_database_to_file(default_data)
                return default_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error: {e}")
            print("Creating new database due to JSON error...")
            default_data = {"messages": [], "knowledge_base": {}}
            self.save_database_to_file(default_data)
            return default_data
        except Exception as e:
            print(f"❌ Database load error: {e}")
            return {"messages": [], "knowledge_base": {}}

    def save_database_to_file(self, data: dict) -> None:
        """Save database to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Database saved to: {self.db_file}")
        except Exception as e:
            print(f"❌ Save error: {e}")

    def save_database(self) -> None:
        """Save current database state"""
        self.save_database_to_file(self.data)

    def normalize_message(self, message: str) -> str:
        """Normalize message for better matching"""
        # Convert to lowercase
        normalized = message.lower().strip()
        
        # Remove extra spaces
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove punctuation
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        return normalized

    def fuzzy_match(self, pattern: str, message: str, threshold: float = 0.6) -> bool:
        """Simple fuzzy matching based on word overlap"""
        pattern_words = set(pattern.lower().split())
        message_words = set(message.lower().split())
        
        if not pattern_words or not message_words:
            return False
        
        # Calculate overlap
        overlap = len(pattern_words.intersection(message_words))
        similarity = overlap / min(len(pattern_words), len(message_words))
        
        return similarity >= threshold

    def find_best_response(self, user_message: str) -> Optional[str]:
        """Find the best response for user message using pattern matching"""
        user_message_lower = user_message.lower()
        knowledge_base = self.data.get("knowledge_base", {})
        
        print(f"🔍 Searching for: '{user_message}'")
        print(f"📚 Available categories: {list(knowledge_base.keys())}")
        
        # Normalize Hindi/English variations
        normalized_message = self.normalize_message(user_message_lower)
        
        # Check each category in knowledge base
        for category_name, category_data in knowledge_base.items():
            if isinstance(category_data, list):
                for item in category_data:
                    if "patterns" in item and "responses" in item:
                        # Check if any pattern matches the user message
                        for pattern in item["patterns"]:
                            pattern_normalized = self.normalize_message(pattern.lower())
                            if (pattern_normalized in normalized_message or 
                                normalized_message in pattern_normalized or
                                self.fuzzy_match(pattern.lower(), user_message_lower)):
                                
                                response = random.choice(item["responses"])
                                print(f"✅ Match found in '{category_name}' with pattern '{pattern}'")
                                return response
        
        print(f"❌ No match found for: '{user_message}'")
        return None

    def save_conversation(self, user_id: str, user_message: str, ai_response: str) -> None:
        """Save conversation to database"""
        conversation = {
            "user_id": user_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["messages"].append(conversation)
        self.save_database()

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        knowledge_base = self.data.get("knowledge_base", {})
        
        total_patterns = 0
        total_responses = 0
        categories = len(knowledge_base)
        
        for category_data in knowledge_base.values():
            if isinstance(category_data, list):
                for item in category_data:
                    if "patterns" in item:
                        total_patterns += len(item["patterns"])
                    if "responses" in item:
                        total_responses += len(item["responses"])
        
        return {
            "total_conversations": len(self.data.get("messages", [])),
            "total_patterns": total_patterns,
            "total_responses": total_responses,
            "categories": categories,
            "database_size_kb": os.path.getsize(self.db_file) / 1024 if os.path.exists(self.db_file) else 0
        }

def test_database():
    """Test function to verify database functionality"""
    print("Testing Hindi-English Database:")
    print("=" * 50)
    
    db = PriyeAIDatabase()
    
    test_messages = [
        "Hello",
        "Kaise ho?", 
        "Programming ke bare mein batao",
        "Joke sunao",
        "Who created you?",
        "Tumhe kisne banaya?",
        "What is Python?",
        "AI ke bare mein batao",
        "Khana banana sikhao"
    ]
    
    for message in test_messages:
        response = db.find_best_response(message)
        if response:
            print(f"Q: {message}")
            print(f"A: {response}")
        else:
            print(f"Q: {message}")
            print(f"A: No specific response found")
        print("-" * 50)
    
    print("\nDatabase Statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_database()