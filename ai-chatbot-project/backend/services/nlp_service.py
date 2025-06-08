def process_message(message):
    # Simple logic for demonstration
    if "hello" in message.lower():
        return "Hi there! How can I assist you today?"
    elif "owner" in message.lower():
        return "This chatbot was created by Ronak Kanani."
    else:
        return "I'm sorry, I didn't understand that. Can you rephrase?"