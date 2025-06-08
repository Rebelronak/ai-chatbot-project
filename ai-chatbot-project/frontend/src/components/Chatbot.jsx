import React, { useState } from "react";

const Chatbot = () => {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);
    
    // Hardcoded API URL as a fallback
    const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";
    
    console.log("API URL:", API_URL); // Debug API URL
    console.log("Chatbot component is rendering");

    const sendMessage = async () => {
        if (!input.trim()) return; // Prevent empty messages
        
        try {
            console.log("Sending message to:", `${API_URL}/chat`);
            
            const response = await fetch(`${API_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: input }),
            });
            
            console.log("Response status:", response.status);
            const data = await response.json();
            console.log("Response data:", data);
            
            setMessages([...messages, { user: input, bot: data.response }]);
            setInput("");
        } catch (error) {
            console.error("Error fetching API:", error);
        }
    };

    return (
        <div className="chatbot">
            <div className="messages">
                {messages.length === 0 && (
                    <div className="empty-state">
                        <p>No messages yet. Type something to start chatting!</p>
                    </div>
                )}
                {messages.map((msg, index) => (
                    <div key={index} className="message-container">
                        <div className="user-message">
                            <strong>You:</strong> {msg.user}
                        </div>
                        <div className="bot-message">
                            <strong>Bot:</strong> {msg.bot}
                        </div>
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;