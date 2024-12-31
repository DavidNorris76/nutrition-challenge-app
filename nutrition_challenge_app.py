

import streamlit as st

# Sample food database with points
food_data = {
    "Apple": 5, "Broccoli": 5, "Chicken Breast": 4, "Quinoa": 5,
    "Almonds": 5, "Cheeseburger": 1, "Soda": 0, "French Fries": 1,
    "Salmon": 5, "Spinach": 5, "Pizza": 1, "Ice Cream": 0,
    "Tofu": 5, "Lentils": 5, "Oats": 5, "Chocolate Bar": 1,
    "Granola": 3, "Eggs": 4, "Avocado": 5, "Sweet Potato": 5
}

# Fake user data for leaderboard
users = {
    "Alice": 75,
    "Bob": 50,
    "Charlie": 60,
    "Diana": 90,
    "Eve": 80
}

# Achievement thresholds
achievement_milestones = {
    "Novice Eater": 50,
    "Healthy Hero": 100,
    "Nutritional Mastermind": 150
}

# App title
st.title("Nutrition Challenge Tracker")

# Daily food log
st.header("Log Your Food")
food_log = st.multiselect("Select the foods you've eaten today:", options=list(food_data.keys()))

if st.button("Calculate Points"):
    # Calculate daily points
    daily_points = sum(food_data[food] for food in food_log)
    st.success(f"Your total points for today: {daily_points}")

    # Update a specific user's score for demonstration (e.g., Alice)
    users["Alice"] += daily_points
    st.write("Points have been added to Alice's total!")

# Leaderboard section
st.header("Leaderboard")
sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
st.write("### Top Users:")
for rank, (user, points) in enumerate(sorted_users, 1):
    st.write(f"{rank}. {user}: {points} points")

# Achievements section
st.header("Achievements")
st.write("### Unlocked Achievements for Alice:")
alice_points = users["Alice"]
unlocked_achievements = [
    achievement for achievement, threshold in achievement_milestones.items()
    if alice_points >= threshold
]
if unlocked_achievements:
    for achievement in unlocked_achievements:
        st.write(f"- {achievement}")
else:
    st.write("No achievements unlocked yet.")

# Footer
st.write("---")
st.write("👨‍💻 Built with Streamlit to prototype your app.")
