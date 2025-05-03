from flask import Flask, render_template, request, jsonify
import nltk
import random
import requests
import re
from nltk.chat.util import Chat, reflections

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# OpenWeatherMap API key and endpoint
WEATHER_API_KEY = '88612e6031496e2912f8f607a3f2792b'  # Replace with your API key
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Define pairs of patterns and responses
pairs = [
    (r"hi|hello|hey", ["Hello! How can I assist you today?", "Hey there! How's it going?"]),
    (r"how are you?", ["I'm just a chatbot, but I'm doing great! How about you?", "I'm good, thanks for asking!"]),
    (r"what is your name?", ["I'm your friendly chatbot. You can call me 'Harry'."]),
    (r"tell me a joke", ["Why don't skeletons fight each other? They don't have the guts.", "Why was the math book sad? It had too many problems."]),
    (r"bye|goodbye", ["Goodbye! It was nice chatting with you.", "See you later! Come back anytime."]),
    (r"(.*) (your name|you)?", ["I am Harry a Chatbot."]),
    (r"what can you do?", ["I can chat with you, tell jokes, and provide weather information."]),
    (r"(.*)", ["I'm not sure what you're saying. Can you try rephrasing?", "Hmm, that’s an interesting question. Let me think..."])
]

# Create the chatbot
class MyChatbot(Chat):
    def __init__(self, pairs, reflections):
        super().__init__(pairs, reflections)

    def respond(self, input_text):
        if any(greeting in input_text.lower() for greeting in ["hi", "hello", "hey"]):
            return random.choice(["Hello! How are you today?", "Hey there! What's up?"])
        
        response = super().respond(input_text)
        
        if not response:
            return random.choice(["I didn’t quite catch that. Could you say it differently?", "Can you elaborate on that?"])
        return response

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(WEATHER_URL, params=params)
    data = response.json()

    if data.get('cod') != 200:
        return "Sorry, I couldn't get the weather information for that location."
    
    main = data.get('main')
    weather = data.get('weather')[0]
    description = weather.get('description')
    temp = main.get('temp')

    return f"The weather in {city} is {description} with a temperature of {temp}°C."

# Initialize Flask app
app = Flask(__name__)
chatbot = MyChatbot(pairs, reflections)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    # Make sure to catch variations of "weather"
    weather_pattern = re.compile(r'\b(weather|wheather)\b.*\b(in|for)?\s*(\w+)\b', re.IGNORECASE)

    # Search for the weather pattern
    match = weather_pattern.search(user_input.lower())
    if match:
        city = match.group(3)  # The third group is the city
        weather_info = get_weather(city)
        return jsonify({"response": weather_info})

    bot_response = chatbot.respond(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)