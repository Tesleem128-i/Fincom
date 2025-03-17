import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from start_model import tokenizer, model
# Load model directly
def get_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")  # Send to GPU
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test
print(get_response("What are the best investment strategies for 2024?"))