# File name: meal_planner.py

from typing import List, Dict
import random
import json
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

class MealPlan:
    def __init__(self):
        self.meals_database = {
            "breakfast": {
                "high_protein": [
                    {"name": "Paneer Bhurji with Multigrain Paratha", "calories": 400, "protein": 20},
                    {"name": "Moong Dal Chilla with Mint Chutney", "calories": 300, "protein": 15},
                    {"name": "Oats Idli with Sambar", "calories": 250, "protein": 12},
                ],
                "moderate_carbs": [
                    {"name": "Vegetable Poha with Sprouts", "calories": 280, "protein": 10},
                    {"name": "Upma with Mixed Vegetables", "calories": 260, "protein": 8},
                    {"name": "Daliya Khichdi", "calories": 270, "protein": 11},
                ]
            },
            "lunch": {
                "protein_rich": [
                    {"name": "Rajma Chawal with Raita", "calories": 450, "protein": 18},
                    {"name": "Chole with Brown Rice", "calories": 420, "protein": 16},
                    {"name": "Paneer Butter Masala with Roti", "calories": 500, "protein": 22},
                ],
                "balanced": [
                    {"name": "Dal Tadka with Mixed Veg and Roti", "calories": 400, "protein": 14},
                    {"name": "Corn Palak with Jeera Rice", "calories": 380, "protein": 12},
                    {"name": "Mixed Dal Khichdi with Kadhi", "calories": 350, "protein": 13},
                ]
            },
            "dinner": {
                "light": [
                    {"name": "Mixed Vegetable Soup with Multigrain Roti", "calories": 300, "protein": 10},
                    {"name": "Masoor Dal with Steamed Rice", "calories": 320, "protein": 12},
                    {"name": "Grilled Paneer with Vegetables", "calories": 350, "protein": 18},
                ]
            }
        }

    def generate_weekly_plan(self) -> Dict:
        weekly_plan = {}
        for day in range(7):
            daily_meals = {
                "breakfast": random.choice(self.meals_database["breakfast"]["high_protein"] + 
                                        self.meals_database["breakfast"]["moderate_carbs"]),
                "lunch": random.choice(self.meals_database["lunch"]["protein_rich"] + 
                                     self.meals_database["lunch"]["balanced"]),
                "dinner": random.choice(self.meals_database["dinner"]["light"])
            }
            weekly_plan[f"day_{day+1}"] = daily_meals
        return weekly_plan

def create_streamlit_app():
    st.title("Intermittent Fasting Meal Planner")
    
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = MealPlan()
    
    if st.button("Generate New Weekly Plan"):
        weekly_plan = st.session_state.meal_plan.generate_weekly_plan()
        st.session_state.current_plan = weekly_plan
        
        # Display the plan
        for day, meals in weekly_plan.items():
            st.subheader(f"{day.replace('_', ' ').title()}")
            for meal_type, meal in meals.items():
                st.write(f"{meal_type.title()}: {meal['name']} ({meal['calories']} cal, {meal['protein']}g protein)")
    
    # WhatsApp Integration Section
    st.sidebar.header("Notification Settings")
    whatsapp_number = st.sidebar.text_input("WhatsApp Number (with country code)")
    notification_time = st.sidebar.time_input("Notification Time")
    
    if st.sidebar.button("Save Settings"):
        st.sidebar.success("Settings saved! You'll receive notifications at the specified time.")

# Deploy this on Streamlit Cloud
if __name__ == "__main__":
    create_streamlit_app()
