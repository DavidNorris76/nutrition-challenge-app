

import streamlit as st

# Inject CSS for Custom Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f9fc;
    }
    h1, h2, h3 {
        text-align: center;
        color: #2C3E50;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        padding: 10px;
        font-size: 1em;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2980B9;
    }
    .stMetric {
        text-align: center;
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("🌟 Nutrition Challenge App 🌟")

# Food Logging Section
st.markdown("## 🥗 Log Your Food")
with st.container():
    food_input = st.text_input("Enter the name of your food:", placeholder="e.g., Apple")
    score = st.selectbox(
        "Select the health score (1 = least healthy, 5 = healthiest):",
        [1, 2, 3, 4, 5],
        index=4
    )
    submit = st.button("Log Food")

    if submit:
        st.success(f"✅ {food_input} logged with a score of {score}!")

# Leaderboard Section
st.markdown("## 🏆 Leaderboard")
with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric("🎖️ User A", "150 pts")
    col2.metric("🎖️ User B", "140 pts")
    col3.metric("🎖️ User C", "130 pts")

# Progress Section
st.markdown("## 📊 Your Progress")
progress_value = 70  # Example progress percentage
st.progress(progress_value)
st.markdown(f"**You're {progress_value}% towards your weekly goal! 🎯**")

# Community Section
st.markdown("## 🤝 Community")
with st.expander("👥 Tips from the Community"):
    st.write("💡 **Tip #1**: Add more whole foods like fruits and vegetables to increase your score!")
    st.write("💡 **Tip #2**: Avoid processed snacks and sugary drinks.")
    st.write("💡 **Tip #3**: Stay hydrated for better health!")

# Footer Section
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Created with ❤️ using Streamlit | "
    "<a href='https://nutrition-challenge.streamlit.app/' target='_blank'>Visit App</a>"
    "</div>",
    unsafe_allow_html=True,
)
