import sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)

from train_model import model
def fetch_from_database(user_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT card_balnce,cash_balance FROM users whereid = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()
    return result if result else (None,None)
def should_fecth_balance(prompt):
    keywords = ["balance", "how much money", "how much do I have", "how much money do I have","can i afford"] # uses this keyword to know when to access the database
    return any(keyword in prompt.lower() for keyword in keywords)

def generate_response(user_id, prompt):
    if should_fecth_balance(prompt):
        card_balance, cash_balance = fetch_from_database(user_id) # generates from database if needed 

        if card_balance is None and cash_balance is None:
            return "I couldn't find your account details. Please check your profile settings."
        
        # Add balance information to the prompt
        prompt += f" My current card balance is ${card_balance:.2f} and cash balance is ${cash_balance:.2f}."
    
    # AI Model generates response
    response = model.generate_content(prompt)
    return response.text
@app.route("/get_financial_advice", methods=["POST"])
def get_financial_advice():
    """API endpoint for generating financial advice."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400
    
    user_id = data.get("user_id")
    prompt = data.get("prompt", "").strip()

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    advice = generate_response(user_id, prompt)
    return jsonify({"response": advice})

if __name__ == "__main__":
    app.run(debug=True)
# This is the code for the model chat bot add it to the code and template 


@app.route("/finbot", methods=["POST"])
def finbot():
    data = request.json
    prompt = data.get("prompt", "")

    print(f"Received message: {prompt}")  # Debugging line

    if not prompt:
        return jsonify("Please enter a valid message.")

    try:
        response = model.generate_content(prompt)
        print(f"AI Response: {response.text}")  # Debugging line
        return jsonify(response.text)
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify(f"AI Error: {str(e)}")




