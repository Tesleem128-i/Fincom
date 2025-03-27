import google.generativeai as genai

# setting my api key
genai.configure(api_key="AIzaSyByWhip1y1g6VuCnCq0avs2QrabdAk3z68")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text


while True:
    user_input = input("USER: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    
    response = generate_response(user_input)
    print("FINBOT: ", response)
    