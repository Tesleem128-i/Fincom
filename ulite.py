import re
import re

def parse_transaction_input(input_string):
    """Parse the transaction input string to extract amount, category, and transaction type."""
    
    # Regular expression to find the amount
    amount_match = re.search(r'\$?(\d+(\.\d{1,2})?)', input_string)
    
    if amount_match:
        amount = float(amount_match.group(1))  # Extract the amount
    else:
        return None, None, None  # Return None if no amount is found

    # Determine transaction type and category
    transaction_type = None
    category = None

    # Check for keywords to determine transaction type
    if 'spent' in input_string or 'expense' in input_string or 'from' in input_string:
        transaction_type = 'expense'
    elif 'gained' in input_string or 'earned' in input_string or 'through' in input_string:
        transaction_type = 'income'

    # Extract the category based on common phrases
    # This regex captures everything after the amount and any keywords
    category_match = re.split(r'\$?\d+(\.\d{1,2})?|\b(spent|gained|earned|from|through|on)\b', input_string, flags=re.IGNORECASE)
    
    if len(category_match) > 1:
        # The category is typically the last part after the keywords
        category = category_match[-1].strip()  # Get the text after the amount and keywords
        if category:  # Check if category is not empty
            return amount, category, transaction_type
        else:
            return None, None, None  # Return None if category is empty
    else:
        return None, None, None  # Return None if no category is found

# Example usage
input1 = "I spent 500 from my card on entertainment"
input2 = "I gained $500 through cash as salary"

print(parse_transaction_input(input1))  # Output: (500.0, 'entertainment', 'expense')
print(parse_transaction_input(input2))  # Output: (500.0, 'salary', 'income')