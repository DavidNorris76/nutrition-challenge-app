import streamlit as st
import requests
from PIL import Image
from pyzbar.pyzbar import decode

# Open Food Facts API Base URL
API_BASE_URL = "https://world.openfoodfacts.org/api/v0/product/"
SEARCH_API_BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# Predefined food database for manual entries
FOOD_DATABASE = {
    "apple": {"score": 5, "nutritional_info": "High in fiber and vitamin C"},
    "banana": {"score": 4, "nutritional_info": "Good source of potassium and energy"},
    "chocolate": {"score": 1, "nutritional_info": "High in sugar and calories"},
    "broccoli": {"score": 5, "nutritional_info": "Rich in fiber, vitamins, and antioxidants"},
}

# Leaderboard and user scores
USER_SCORES = {
    "Alice": 45,
    "Bob": 50,
    "Charlie": 38,
    "David": 60,
    "Eve": 25,
}

# Function to fetch product data using Open Food Facts API
def get_product_data(barcode):
    url = f"{API_BASE_URL}{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data. Error {response.status_code}: {response.reason}")
        return None

# Function to fetch healthier alternatives
def get_healthier_alternatives(nutriscore_grade, categories):
    if not categories:
        return []
    
    search_category = categories.split(",")[0]  # Use the first category
    params = {
        "search_terms": search_category,
        "search_tag": "categories",
        "fields": "product_name,nutriscore_grade,image_url,brands",
        "sort_by": "nutriscore_score",
        "page_size": 5,
        "json": 1
    }
    response = requests.get(SEARCH_API_BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get("products", [])
    else:
        st.warning("Failed to fetch healthier alternatives.")
        return []

# Function to decode barcode from uploaded image
def decode_barcode(image):
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    else:
        return None

# Function to update leaderboard
def update_leaderboard(user, points):
    if user in USER_SCORES:
        USER_SCORES[user] += points
    else:
        USER_SCORES[user] = points

# Streamlit App
st.title("🌟 Nutrition Challenge App 🌟")

# Leaderboard Section
st.sidebar.title("🏆 Leaderboard")
leaderboard = sorted(USER_SCORES.items(), key=lambda x: x[1], reverse=True)
for rank, (user, score) in enumerate(leaderboard, start=1):
    st.sidebar.write(f"{rank}. {user}: {score} points")

# Section 1: Live Barcode Scanner
st.markdown("## 📷 Scan Barcode Using Your Camera or Enter a Food")
barcode_or_food = st.text_input("Enter a barcode or food name manually")

if barcode_or_food:
    # Check if input is a food in the database
    if barcode_or_food.lower() in FOOD_DATABASE:
        food = FOOD_DATABASE[barcode_or_food.lower()]
        st.success(f"Food Found: {barcode_or_food.capitalize()}")
        st.write(f"Score: {food['score']}")
        st.write(f"Details: {food['nutritional_info']}")
        update_leaderboard("Guest", food["score"])
    else:
        # Fetch product data using barcode
        product_data = get_product_data(barcode_or_food)
        if product_data and product_data.get("status") == 1:
            product = product_data["product"]
            st.markdown(f"### **{product.get('product_name', 'Unknown Product')}**")
            st.image(product.get("image_url", ""), width=150, caption=product.get("brands", "Unknown Brand"))

            # Nutri-Score
            score = product.get("nutriscore_grade", "N/A").upper()
            score_map = {
                "A": {"color": "🟢", "label": "Excellent"},
                "B": {"color": "🟢", "label": "Good"},
                "C": {"color": "🟠", "label": "Average"},
                "D": {"color": "🔴", "label": "Poor"},
                "E": {"color": "🔴", "label": "Very Poor"},
            }
            score_label = score_map.get(score, {"color": "⚪", "label": "N/A"})
            st.markdown(f"### Nutri-Score: {score_label['color']} **{score}** - {score_label['label']}")

            # Nutritional Information Section
            st.markdown("### **Nutritional Information per 100g**")
            st.markdown(
                f"""
                - **Energy:** {product.get('nutriments', {}).get('energy-kcal_100g', 'N/A')} kcal
                - **Protein:** {product.get('nutriments', {}).get('proteins_100g', 'N/A')} g
                - **Fat:** {product.get('nutriments', {}).get('fat_100g', 'N/A')} g
                - **Carbohydrates:** {product.get('nutriments', {}).get('carbohydrates_100g', 'N/A')} g
                - **Sugars:** {product.get('nutriments', {}).get('sugars_100g', 'N/A')} g
                - **Salt:** {product.get('nutriments', {}).get('salt_100g', 'N/A')} g
                """
            )
            update_leaderboard("Guest", 5 if score == "A" else 3 if score == "B" else 1)
            
            # Fetch and display healthier alternatives
            st.markdown("### **Healthier Alternatives**")
            alternatives = get_healthier_alternatives(
                product.get("nutriscore_grade", "N/A"),
                product.get("categories_tags", ""),
            )
            if alternatives:
                for alt in alternatives:
                    alt_name = alt.get("product_name", "Unknown Product")
                    alt_brand = alt.get("brands", "Unknown Brand")
                    alt_score = alt.get("nutriscore_grade", "N/A").upper()
                    alt_image = alt.get("image_url", "")

                    st.markdown(f"**{alt_name}** ({alt_brand})")
                    st.image(alt_image, width=100)
                    st.write(f"Nutri-Score: {alt_score}")
            else:
                st.info("No healthier alternatives found.")
        else:
            st.error("No product data found. Try another barcode or food.")
