from start_model import model, tokenizer
import torch

def generate_response(prompt, max_length=50):  # Reduce max_length
    """Generates a response using GPT-2 with optimized settings."""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=max_length, 
                             temperature=0.7, top_k=50, top_p=0.8, 
                             no_repeat_ngram_size=3, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interactive chatbot loop with history
conversation_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Maintain conversation context
    conversation_history.append(f"You: {user_input}")
    context = " ".join(conversation_history[-3:])  # Keep only the last 3 exchanges

    response = generate_response(context)
    conversation_history.append(f"GPT-2: {response}")

    print("GPT-2:", response)
