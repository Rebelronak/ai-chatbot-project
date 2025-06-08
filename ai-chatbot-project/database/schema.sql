-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
    preferences TEXT -- JSON string for user preferences
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    message_type TEXT DEFAULT 'chat', -- chat, command, file_upload, etc.
    satisfaction_rating INTEGER, -- 1-5 rating from user
    response_time_ms INTEGER -- Response time in milliseconds
);

-- Knowledge base table
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    pattern TEXT NOT NULL,
    response TEXT NOT NULL,
    usage_count INTEGER DEFAULT 0,
    effectiveness_score REAL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User feedback table
CREATE TABLE IF NOT EXISTS user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    conversation_id INTEGER,
    feedback_type TEXT, -- like, dislike, suggestion, bug_report
    feedback_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Learning data table (for improving responses)
CREATE TABLE IF NOT EXISTS learning_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    expected_response TEXT,
    actual_response TEXT,
    user_satisfaction INTEGER,
    pattern_matched TEXT,
    category TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_start DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_end DATETIME,
    message_count INTEGER DEFAULT 0,
    session_duration_minutes INTEGER,
    topics_discussed TEXT -- JSON array of topics
);

-- Popular queries table
CREATE TABLE IF NOT EXISTS popular_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_pattern TEXT UNIQUE NOT NULL,
    query_count INTEGER DEFAULT 1,
    last_asked DATETIME DEFAULT CURRENT_TIMESTAMP,
    category TEXT,
    average_satisfaction REAL DEFAULT 0.0
);

-- System analytics table
CREATE TABLE IF NOT EXISTS system_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value TEXT NOT NULL,
    metric_date DATE DEFAULT (date('now')),
    additional_data TEXT -- JSON for extra metrics
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category ON knowledge_base(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_pattern ON knowledge_base(pattern);
CREATE INDEX IF NOT EXISTS idx_user_feedback_user_id ON user_feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_popular_queries_count ON popular_queries(query_count DESC);

-- Create a table to store chatbot messages
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);