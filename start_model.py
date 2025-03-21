from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load GPT-2 tokenizer and model
MODEL_NAME = "gpt3_turbo"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
 