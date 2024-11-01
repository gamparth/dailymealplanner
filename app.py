# File: app.py
from flask import Flask, jsonify
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from google.cloud import texttospeech
from translate import Translator

app = Flask(__name__)
load_dotenv()

class HindiVoiceGenerator:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.translator = Translator(to_lang="hi")

    def translate_to_hindi(self, text):
        try:
            return self.translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def generate_voice_message(self, text):
        hindi_text = self.translate_to_hindi(text)
        synthesis_input = texttospeech.SynthesisInput(text=hindi_text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="hi-IN",
            name="hi-IN-Standard-A",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content

class MealPlanner:
    def __init__(self):
        self.meals_database = {
            "lunch": [
                {
                    "name": "Rajma Chawal with Raita",
                    "prep_time": "45 mins",
                    "calories": 550,
                    "protein": "22g",
                    "carbs": "65g",
                    "fats": "18g",
                    "instructions": [
                        "1. Soak rajma overnight",
                        "2. Pressure cook rajma with bay leaf, cardamom",
                        "3. Prepare masala with onion, tomato, ginger-garlic",
                        "4. Mix cooked rajma with masala",
                        "5. Cook brown rice separately",
                        "6. Prepare cucumber raita with roasted cumin"
                    ]
                },
                {
                    "name": "Chole with Brown Rice and Green Salad",
                    "prep_time": "40 mins",
                    "calories": 520,
                    "protein": "20g",
                    "carbs": "68g",
                    "fats": "15g",
                    "instructions": [
                        "1. Soak chickpeas overnight",
                        "2. Pressure cook with tea bag for color",
                        "3. Prepare onion-tomato masala",
                        "4. Mix with spices and simmer",
                        "5. Cook brown rice",
                        "6. Prepare fresh green salad"
                    ]
                },
                {
                    "name": "Paneer Butter Masala with Multigrain Roti",
                    "prep_time": "35 mins",
                    "calories": 580,
                    "protein": "24g",
                    "carbs": "45g",
                    "fats": "22g",
                    "instructions": [
                        "1. Prepare tomato-cashew gravy",
                        "2. Sauté paneer cubes separately",
                        "3. Mix gravy with cream and butter",
                        "4. Add paneer to the gravy",
                        "5. Prepare multigrain roti dough",
                        "6. Cook rotis on tawa"
                    ]
                }
            ],
            "dinner": [
                {
                    "name": "Mixed Dal and Vegetable Khichdi",
                    "prep_time": "30 mins",
                    "calories": 420,
                    "protein": "18g",
                    "carbs": "52g",
                    "fats": "12g",
                    "instructions": [
                        "1. Wash rice and mixed dals",
                        "2. Chop vegetables finely",
                        "3. Prepare tempering with ghee and spices",
                        "4. Cook all ingredients in pressure cooker",
                        "5. Garnish with ghee and roasted cumin"
                    ]
                },
                {
                    "name": "Grilled Paneer with Quinoa and Vegetables",
                    "prep_time": "35 mins",
                    "calories": 450,
                    "protein": "22g",
                    "carbs": "48g",
                    "fats": "16g",
                    "instructions": [
                        "1. Marinate paneer with spices",
                        "2. Cook quinoa with vegetables",
                        "3. Grill or pan-fry paneer",
                        "4. Steam mixed vegetables",
                        "5. Prepare mint-yogurt dip"
                    ]
                },
                {
                    "name": "Masoor Dal with Steamed Rice and Vegetables",
                    "prep_time": "30 mins",
                    "calories": 400,
                    "protein": "16g",
                    "carbs": "55g",
                    "fats": "10g",
                    "instructions": [
                        "1. Cook masoor dal in pressure cooker",
                        "2. Prepare tempering with spices",
                        "3. Cook rice separately",
                        "4. Steam vegetables with minimal spices",
                        "5. Garnish with coriander leaves"
                    ]
                }
            ]
        }
        self.voice_generator = HindiVoiceGenerator()

    def format_english_message(self, meal_plan):
        return f"""
🍱 Intermittent Fasting Meal Plan for {meal_plan['date']}

⏰ Eating Window Suggestion:
First Meal: 12:00 PM - 1:00 PM
Last Meal: 7:00 PM - 8:00 PM

🌞 LUNCH (First Meal)
• {meal_plan['lunch']['name']}
• Prep Time: {meal_plan['lunch']['prep_time']}
• Calories: {meal_plan['lunch']['calories']}
• Protein: {meal_plan['lunch']['protein']}
• Carbs: {meal_plan['lunch']['carbs']}
• Fats: {meal_plan['lunch']['fats']}

Instructions:
{chr(10).join(meal_plan['lunch']['instructions'])}

🌙 DINNER (Last Meal)
• {meal_plan['dinner']['name']}
• Prep Time: {meal_plan['dinner']['prep_time']}
• Calories: {meal_plan['dinner']['calories']}
• Protein: {meal_plan['dinner']['protein']}
• Carbs: {meal_plan['dinner']['carbs']}
• Fats: {meal_plan['dinner']['fats']}

Instructions:
{chr(10).join(meal_plan['dinner']['instructions'])}

📊 Daily Totals:
• Total Calories: {meal_plan['total_calories']}
• Total Protein: {meal_plan['total_protein']}
• Total Carbs: {meal_plan['total_carbs']}
• Total Fats: {meal_plan['total_fats']}

💧 Remember to stay hydrated during fasting hours!

👩‍🍳 Voice instructions in Hindi will follow.
Please reply with 👍 to approve this menu.
"""

    def format_voice_content(self, meal_plan):
        return f"""
नमस्ते! कल के दो भोजन की विधि:

दोपहर का खाना - {meal_plan['lunch']['name']}:
{chr(10).join(meal_plan['lunch']['instructions'])}

रात का खाना - {meal_plan['dinner']['name']}:
{chr(10).join(meal_plan['dinner']['instructions'])}

कृपया ध्यान दें:
दोपहर का खाना दोपहर 12 से 1 बजे के बीच
रात का खाना शाम 7 से 8 बजे के बीच बनाना है।
"""

    def get_next_day_meals(self):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d")
        
        meals = {
            "date": tomorrow,
            "lunch": random.choice(self.meals_database["lunch"]),
            "dinner": random.choice(self.meals_database["dinner"])
        }
        
        # Calculate totals
        meals["total_calories"] = meals["lunch"]["calories"] + meals["dinner"]["calories"]
        meals["total_protein"] = f"{int(meals['lunch']['protein'][:-1]) + int(meals['dinner']['protein'][:-1])}g"
        meals["total_carbs"] = f"{int(meals['lunch']['carbs'][:-1]) + int(meals['dinner']['carbs'][:-1])}g"
        meals["total_fats"] = f"{int(meals['lunch']['fats'][:-1]) + int(meals['dinner']['fats'][:-1])}g"
        
        # Generate both message formats
        meals["english_message"] = self.format_english_message(meals)
        voice_content = self.format_voice_content(meals)
        meals["voice_message"] = self.voice_generator.generate_voice_message(voice_content)
        
        return meals

@app.route('/get-tomorrow-meals', methods=['GET'])
def get_tomorrow_meals():
    planner = MealPlanner()
    meals = planner.get_next_day_meals()
    return jsonify(meals)

if __name__ == '__main__':
    app.run(port=5000)
