import torch
import wikipediaapi
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")

# Set user agent
user_agent = "MyFinancialChatbot/1.0 (contact: projectfinodido@gmail.com)"
wiki_wiki = wikipediaapi.Wikipedia("en", user_agent=user_agent)


def fetch_wikipedia_summary(query):
    """Fetches summary from Wikipedia for the given query."""
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    return "Sorry, I couldn't find relevant information."

def answer_financial_question(question):
    """Fetches context dynamically and answers the question."""
    # Get financial data from Wikipedia
    context = fetch_wikipedia_summary(question)

    # Tokenize and process
    inputs = tokenizer(question, context, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    start_scores, end_scores = outputs.start_logits, outputs.end_logits
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1  # Include last word

    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index])
    )

    return answer if answer.strip() else "Sorry, I couldn't find an answer."

if __name__ == "__main__":
    question = "What is stock market investment?"
    answer = answer_financial_question(question)
    print(f"Answer: {answer}")
