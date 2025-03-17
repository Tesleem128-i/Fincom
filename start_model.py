# Load model directly
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")