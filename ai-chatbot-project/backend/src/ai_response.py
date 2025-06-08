from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")

def get_ai_response(user_input):
    inputs = tokenizer([user_input], return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=600)
    response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    return response

if __name__ == "__main__":
    print("Start chatting with the AI (type 'quit' to stop)!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = get_ai_response(user_input)
        print("AI:", response)