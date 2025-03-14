def suggest_business(capital):
    businesses = {
        "Very Low Budget ($1 - $100)": [
            "Dropshipping (No inventory required)",
            "Freelance Writing (Start on Upwork/Fiverr)",
            "Affiliate Marketing (Promote products & earn commission)",
            "Social Media Management (Manage small business pages)",
            "Tutoring (Teach a skill or subject online)",
            "Print-on-Demand (Sell custom t-shirts, mugs, and hoodies)",
            "Handmade Crafts (Sell handmade jewelry, candles, or art)"
        ],
        "Low Budget ($100 - $500)": [
            "Mini Importation (Buy & resell small gadgets, accessories)",
            "Local Snacks Business (Bake and sell small pastries)",
            "Digital Marketing Agency (Offer SEO, ads, and marketing services)",
            "Graphic Design Services (Create logos, flyers, and posters)",
            "Car Wash Business (Start with a mobile car wash)",
            "Online Course Selling (Create & sell courses on Udemy, Teachable)"
        ],
        "Lower Medium Budget ($500 - $2000)": [
            "E-commerce Store (Sell products via Shopify, WooCommerce)",
            "Photography/Videography (Start with a mid-range camera)",
            "Laundry Business (Start a home-based laundry service)",
            "Clothing Brand (Design & sell customized clothing)",
            "Barbershop or Salon Business (Rent a small space or work from home)",
            "Food Business (Small-scale food vending or catering)"
        ],
        "Upper Medium Budget ($2000 - $5000)": [
            "Small Scale Farming (Vegetables, poultry, fish farming)",
            "Car Rental Service (Start with a used car for Uber/Bolt)",
            "Tech Repairs & Services (Laptop/Phone repairs)",
            "Cyber Café or Gaming Center (Rent a small shop, offer internet & gaming)",
            "Event Planning & Rentals (Rent out event decor, chairs, and sound systems)"
        ],
        "Lower High Budget ($5000 - $10,000)": [
            "Logistics/Delivery Business (Rent bikes/cars for delivery services)",
            "Fitness & Gym Center (Start with a small fitness studio)",
            "Real Estate Investment (Buy and rent out small apartments)",
            "Printing & Branding Business (Offer custom printing services)",
            "Mini Supermarket (Rent a space & stock essential goods)"
        ],
        "Upper High Budget ($10,000 - $20,000)": [
            "Import/Export Business (Trade in bulk goods)",
            "Restaurant & Lounge (Open a small fast-food restaurant)",
            "Auto Dealership (Buy & resell used cars)",
            "Online Marketplace (Build an e-commerce marketplace)",
            "Tech Startup (Develop a software or app solution)"
        ],
        "Very High Budget ($20,000+)": [
            "Large-Scale Real Estate (Buy land, build & sell apartments)",
            "Hotel Business (Invest in hospitality)",
            "Manufacturing (Start a small factory)",
            "Automobile Dealership (Sell brand-new cars)",
            "Private School Business (Set up a primary/secondary school)"
        ]
    }

    # Categorizing based on budget
    if capital < 100:
        category = "Very Low Budget ($1 - $100)"
    elif 100 <= capital < 500:
        category = "Low Budget ($100 - $500)"
    elif 500 <= capital < 2000:
        category = "Lower Medium Budget ($500 - $2000)"
    elif 2000 <= capital < 5000:
        category = "Upper Medium Budget ($2000 - $5000)"
    elif 5000 <= capital < 10000:
        category = "Lower High Budget ($5000 - $10,000)"
    elif 10000 <= capital < 20000:
        category = "Upper High Budget ($10,000 - $20,000)"
    else:
        category = "Very High Budget ($20,000+)"

    print(f"\nBased on your budget (${capital}), here are some business ideas:\n")
    business_options = businesses[category]

    for i, business in enumerate(business_options, 1):
        print(f"{i}. {business}")

    # User selects a business
    try:
        choice = int(input("\nEnter the number of the business you want to learn about: "))
        selected_business = business_options[choice - 1]
        print(f"\nGreat choice! You selected: {selected_business}")
        return selected_business  # This can be used for integration
    except (ValueError, IndexError):
        print("\nInvalid choice. Please enter a valid number from the list.")
        return None

# Get user input
try:
    user_money = float(input("Enter the amount of money you have ($): "))
    selected_business = suggest_business(user_money)

    # If integrated with Flask or another framework, you can return `selected_business`
except ValueError:
    print("Invalid input. Please enter a numeric value.")
