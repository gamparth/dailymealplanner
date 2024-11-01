# File: app.py

from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from google.cloud import texttospeech
import json
from google.oauth2 import service_account
import tempfile
from translate import Translator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

class HindiVoiceGenerator:
    def __init__(self):
        try:
            # Get credentials from environment variable
            credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if not credentials_json:
                logger.error("Google Cloud credentials not found in environment variables")
                raise Exception("Google Cloud credentials not found")

            # Create a temporary file to store credentials
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file.write(credentials_json)
                temp_file_path = temp_file.name

            # Initialize credentials
            credentials = service_account.Credentials.from_service_account_file(
                temp_file_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )

            # Remove temporary file
            os.unlink(temp_file_path)

            # Initialize client with credentials
            self.client = texttospeech.TextToSpeechClient(credentials=credentials)
            self.translator = Translator(to_lang="hi")
            
        except Exception as e:
            logger.error(f"Error initializing Hindi Voice Generator: {str(e)}")
            raise

    def translate_to_hindi(self, text):
        try:
            return self.translator.translate(text)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text

    def generate_voice_message(self, text):
        try:
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
        except Exception as e:
            logger.error(f"Error generating voice message: {str(e)}")
            raise

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
                        "2. Pressure cook with bay leaf and cardamom",
                        "3. Prepare onion-tomato masala base",
                        "4. Cook rajma with masala",
                        "5. Prepare brown rice separately",
                        "6. Make cucumber raita"
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
                        "2. Pressure cook with tea bag",
                        "3. Prepare masala gravy",
                        "4. Mix and simmer chole",
                        "5. Cook brown rice",
                        "6. Prepare fresh salad"
                    ]
                },
                {
                    "name": "Quinoa Bowl with Grilled Vegetables",
                    "prep_time": "35 mins",
                    "calories": 480,
                    "protein": "18g",
                    "carbs": "58g",
                    "fats": "16g",
                    "instructions": [
                        "1. Rinse quinoa thoroughly",
                        "2. Cook quinoa with vegetable stock",
                        "3. Grill assorted vegetables",
                        "4. Prepare lemon-herb dressing",
                        "5. Assemble bowl",
                        "6. Add toasted seeds"
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
                        "3. Prepare tempering",
                        "4. Pressure cook everything",
                        "5. Add ghee and cumin"
                    ]
                },
                {
                    "name": "Grilled Paneer with Mint Chutney",
                    "prep_time": "25 mins",
                    "calories": 450,
                    "protein": "22g",
                    "carbs": "48g",
                    "fats": "16g",
                    "instructions": [
                        "1. Marinate paneer",
                        "2. Prepare mint chutney",
                        "3. Grill paneer",
                        "4. Steam vegetables",
                        "5. Serve with multigrain roti"
                    ]
                },
                {
                    "name": "Masoor Dal with Steamed Rice",
                    "prep_time": "30 mins",
                    "calories": 400,
                    "protein": "16g",
                    "carbs": "55g",
                    "fats": "10g",
                    "instructions": [
                        "1. Wash and cook masoor dal",
                        "2. Prepare tempering",
                        "3. Cook rice",
                        "4. Steam vegetables",
                        "5. Garnish with herbs"
                    ]
                }
            ]
        }
        try:
            self.voice_generator = HindiVoiceGenerator()
        except Exception as e:
            logger.error(f"Error initializing voice generator: {str(e)}")
            self.voice_generator = None

    def format_english_message(self, meal_plan):
        return f"""
🍱 Intermittent Fasting Meal Plan for {meal_plan['date']}

⏰ Eating Window:
First Meal (Lunch): 12:00 PM - 1:00 PM
Last Meal (Dinner): 7:00 PM - 8:00 PM

🌞 LUNCH
• {meal_plan['lunch']['name']}
• Prep Time: {meal_plan['lunch']['prep_time']}
• Calories: {meal_plan['lunch']['calories']}
• Protein: {meal_plan['lunch']['protein']}
• Carbs: {meal_plan['lunch']['carbs']}
• Fats: {meal_plan['lunch']['fats']}

Instructions:
{chr(10).join(meal_plan['lunch']['instructions'])}

🌙 DINNER
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
"""

    def format_voice_content(self, meal_plan):
        return f"""
नमस्ते! कल के भोजन की विधि:

दोपहर का खाना - {meal_plan['lunch']['name']}:
{chr(10).join(meal_plan['lunch']['instructions'])}

रात का खाना - {meal_plan['dinner']['name']}:
{chr(10).join(meal_plan['dinner']['instructions'])}

कृपया ध्यान दें:
दोपहर का खाना दोपहर 12 से 1 बजे के बीच
रात का खाना शाम 7 से 8 बजे के बीच तैयार करें।
"""

    def get_next_day_meals(self):
        try:
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
            
            # Generate messages
            meals["english_message"] = self.format_english_message(meals)
            voice_content = self.format_voice_content(meals)
            
            if self.voice_generator:
                meals["voice_message"] = self.voice_generator.generate_voice_message(voice_content)
            else:
                meals["voice_message"] = None
                logger.warning("Voice generator not available, skipping voice message generation")
            
            return meals
            
        except Exception as e:
            logger.error(f"Error generating meal plan: {str(e)}")
            raise

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "message": "Intermittent Fasting Meal Planner API is running",
        "endpoints": {
            "GET /": "Health check",
            "GET /get-tomorrow-meals": "Get tomorrow's meal plan"
        }
    })

@app.route('/get-tomorrow-meals', methods=['GET'])
def get_tomorrow_meals():
    try:
        planner = MealPlanner()
        meals = planner.get_next_day_meals()
        return jsonify(meals)
    except Exception as e:
        logger.error(f"Error in get_tomorrow_meals endpoint: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to generate meal plan"
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not found",
        "message": "The requested resource does not exist"
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
