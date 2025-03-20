import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
from start_model import tokenizer, model
import sqlite3 
# Load model directly
def get_response(prompt):
    inputs = tokenizer(prompt,return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs, max_length=150)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def fetch_from_database(user_query):
    db = sqlite3.connect('mydatabase.db')
    cursor = db.cursor()
import sqlite3

def fetch_from_database(user_query):
    """Searches the SQLite3 database for relevant information"""
    db = sqlite3.connect("fincom_web_info.db")  # Path to your SQLite database
    cursor = db.cursor()

    # Example: Searching for financial advice related to the query
    cursor.execute("SELECT advice FROM financial_data WHERE keywords LIKE ?", (f"%{user_query}%",))
    result = cursor.fetchone()

    db.close()
    
    return result[0] if result else "I couldn't find relevant info in the datab"
print(get_response("What is money?"))
