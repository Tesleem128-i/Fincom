from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

MODEL_NAME = "google/flan-t5-base"  # Use Flan-T5 Base

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
