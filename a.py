def suggest_business(capital):
    businesses = {
        "Low Budget": {
            "Dropshipping": "https://www.youtube.com/watch?v=3jN5vXZJM4U",
            "Blogging or YouTube": "https://www.youtube.com/watch?v=VvD_C8Jj9mA",
            "Freelance Writing": "https://www.youtube.com/watch?v=W4xyNGg7F4A"
        },
        "Medium Budget": {
            "Mini Importation": "https://www.youtube.com/watch?v=TtS2aGnk6C4",
            "Food Business": "https://www.youtube.com/watch?v=FO5CFEKqp1o",
            "E-commerce Store": "https://www.youtube.com/watch?v=6MBcT-dkGqk"
        },
        "High Budget": {
            "Real Estate Investment": "https://www.youtube.com/watch?v=hqxA-jFqG5o",
            "Tech Startup": "https://www.youtube.com/watch?v=mMF3U6BXi_o",
            "Logistics Business": "https://www.youtube.com/watch?v=_PfpF4N7TxA"
        }
    }

    # Categorizing based on budget
    if capital < 500:
        category = "Low Budget"
    elif 500 <= capital < 5000:
        category = "Medium Budget"
    else:
        category = "High Budget"

    print(f"\nBased on your budget (${capital}), here are some business ideas:\n")
    business_options = list(businesses[category].keys())

    for i, business in enumerate(business_options, 1):
        print(f"{i}. {business}")

    # User selects a business
    try:
        choice = int(input("\nEnter the number of the business you want to learn about: "))
        selected_business = business_options[choice - 1]
        print(f"\nGreat choice! Watch this tutorial on {selected_business}:")
        print(businesses[category][selected_business])
    except (ValueError, IndexError):
        print("\nInvalid choice. Please enter a valid number from the list.")

# Get user input
try:
    user_money = float(input("Enter the amount of money you have ($): "))
    suggest_business(user_money)
except ValueError:
    print("Invalid input. Please enter a numeric value.")
