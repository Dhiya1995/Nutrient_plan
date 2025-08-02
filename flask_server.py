import os
import json
from flask import Flask, render_template, request, jsonify
import re
from textblob import TextBlob

# --- Define a local Web server --- #
app = Flask(__name__)

# Your existing routes
@app.route("/")
def hello():
    message = "Hello World!"
    return render_template('index.html', message=message)

@app.route("/index.html")
def index():
    message = "Welcome to index.html!"
    return render_template('index.html', message=message)

@app.route("/history.html")
def history():
    message = "Welcome to history.html!"
    return render_template('history.html', message=message)

@app.route("/track.html")
def track():
    message = "Welcome to track.html!"
    return render_template('track.html', message=message)

@app.route("/preference.html")
def preference():
    message = "Welcome to preference.html!"
    return render_template('preference.html', message=message)

@app.route("/Recipes.html")
def Recipes():
    message = "Welcome to Recipes.html!"
    return render_template('Recipes.html', message=message)

@app.route("/food-database", methods = ['GET', 'POST'])
def foodDatabase():
    if request.method == 'GET':
        json_file = os.path.join(app.root_path, 'food_data', 'localFoods.json')

        with open(json_file) as file:
            data = json.load(file)
            return jsonify(data)

    elif request.method == 'POST':
        json_file = os.path.join(app.root_path, 'food_data', 'localFoods.json')
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as file:
                json.dump([], file)

        stored_data = None
        received_data = None

        with open(json_file, 'r') as file:
            stored_data = json.load(file)

        received_data = request.form.to_dict()
        received_data["tags"] = json.loads(received_data["tags"])

        if not any(temp["name"] == received_data["name"] for temp in stored_data):
            stored_data.append(received_data.copy())

        json_stored_data = json.dumps(stored_data)
        with open(json_file, 'w') as file:
            file.seek(0)
            file.write(json_stored_data)
            file.truncate()
        
        return json_stored_data
    

@app.route("/food-dislike", methods = ['GET', 'POST', 'DELETE'])
def foodDislike():
    user = request.args.get('user', default = 'test', type = str)
    if request.method == 'GET':
        json_file = os.path.join(app.root_path, 'user_data', '{}_dislike.txt'.format(user))	
        if not os.path.isfile(json_file):	
            with open(json_file, 'w') as file:	
                json.dump({"user": "test", "dislike": []}, file)

        with open('user_data/{}_dislike.txt'.format(user)) as file:
            data = json.load(file)
            return jsonify(data)

    elif request.method == 'POST' or request.method == 'DELETE':
        json_file = os.path.join(app.root_path, 'user_data', '{}_dislike.txt'.format(user))
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as file:
                json.dump({"user": "test", "dislike": []}, file)

        with open('user_data/{}_dislike.txt'.format(user), 'r+') as file:
            stored_data = json.load(file)
            received_data = request.form.to_dict()
            print(received_data)
            stored_data["dislike"].append(received_data["dislike"])
            json_data = json.dumps(stored_data)
            file.seek(0)
            file.write(json_data)
            file.truncate()
            return json_data


@app.route("/food-tag-query", methods = ['POST'])
def foodTagQuery():
    if request.method == 'POST':
        json_file = os.path.join(app.root_path, 'food_data', 'localFoods.json')

        with open(json_file, 'r') as file:
            stored_data = json.load(file)
            # print(stored_data)

            received_data = request.form.to_dict()
            print(received_data)
            target_nutrient = received_data["nutrient"]
            target_condition = received_data["condition"]
            foods_qualified = []

            for food_dict in stored_data:
                # print(food_dict)
                if target_nutrient == "proteins" and target_condition == "high":
                    if ("High Proteins" in food_dict["tags"]): 
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)
                elif target_nutrient == "proteins" and target_condition == "low":
                    if ("Low Proteins" in food_dict["tags"]):
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)

                elif target_nutrient == "carbohydrates" and target_condition == "high":
                    if ("High Carbohydrates" in food_dict["tags"]): 
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)                       
                elif target_nutrient == "carbohydrates" and target_condition == "low":
                    if ("Low Carbohydrates" in food_dict["tags"]):
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)

                elif target_nutrient == "fats" and target_condition == "high":
                    if ("High Fats" in food_dict["tags"]):
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)
                elif target_nutrient == "fats" and target_condition == "low":
                    if ("Low Fats" in food_dict["tags"]):
                        foods_qualified.append(food_dict.copy())
                        print(foods_qualified)                     

            json_foods_qualified = json.dumps({"selected_foods": foods_qualified})
            print(json_foods_qualified)
            return json_foods_qualified




import random

# Meal database
meal_db = {
    'underweight': {
        'breakfast': ['Idly with sambar', 'Oatmeal with banana', 'Smoothie with peanut butter', 'Boiled eggs and toast', 'Dosa with chutney'],
        'lunch': ['Sambar rice', 'Grilled chicken with rice', 'Paneer curry with roti', 'Turkey sandwich', 'Aloo paratha with yogurt'],
        'dinner': ['Dal with rice', 'Salmon with quinoa', 'Vegetable stir fry with tofu', 'Chicken soup with bread', 'Palak paneer with roti']
    },
    'normal': {
        'breakfast': ['Greek yogurt with berries', 'Vegetable omelette', 'Peanut butter toast', 'Poha', 'Dosa with chutney'],
        'lunch': ['Grilled fish with vegetables', 'Dal with rice', 'Chicken Caesar salad', 'Chole bhature', 'Vegetable biryani'],
        'dinner': ['Chapati with vegetable curry', 'Brown rice with lentils', 'Baked chicken and veggies', 'Kadhi pakora with rice', 'Dosa with sambar']
    },
    'overweight': {
        'breakfast': ['Protein shake', 'Low-fat yogurt and nuts', 'Egg whites and avocado', 'Upma', 'Masala oats'],
        'lunch': ['Grilled chicken salad', 'Quinoa bowl with veggies', 'Tofu wrap', 'Baingan bharta with roti', 'Methi thepla'],
        'dinner': ['Steamed vegetables and fish', 'Low-carb soup', 'Zucchini noodles with sauce', 'Cabbage sabzi with chapati', 'Palak-methi paratha']
    },
    'obese': {
        'breakfast': ['Green smoothie', 'Boiled egg whites', 'Avocado toast', 'Moong dal chilla', 'Vegetable poha'],
        'lunch': ['Grilled vegetable salad', 'Soup with lean protein', 'Steamed tofu and greens', 'Aloo-gobhi with roti', 'Rajma with rice'],
        'dinner': ['Veggie stir-fry', 'Lentil soup', 'Grilled chicken breast', 'Tofu curry with brown rice', 'Vegetable soup with salad']
    }
}

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return 'underweight'
    elif 18.5 <= bmi < 24.9:
        return 'normal'
    elif 25 <= bmi < 29.9:
        return 'overweight'
    else:
        return 'obese'

def generate_weekly_plan(category):
    plan = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    breakfast_meals = meal_db[category]['breakfast'][:]
    lunch_meals = meal_db[category]['lunch'][:]
    dinner_meals = meal_db[category]['dinner'][:]

    random.shuffle(breakfast_meals)
    random.shuffle(lunch_meals)
    random.shuffle(dinner_meals)

    for day in days:
        breakfast = breakfast_meals.pop()
        lunch = lunch_meals.pop()
        dinner = dinner_meals.pop()

        plan[day] = {
            'Breakfast': breakfast,
            'Lunch': lunch,
            'Dinner': dinner
        }

        if not breakfast_meals:
            breakfast_meals = meal_db[category]['breakfast'][:]
            random.shuffle(breakfast_meals)
        if not lunch_meals:
            lunch_meals = meal_db[category]['lunch'][:]
            random.shuffle(lunch_meals)
        if not dinner_meals:
            dinner_meals = meal_db[category]['dinner'][:]
            random.shuffle(dinner_meals)

    return plan

@app.route("/diet-plan", methods=['GET', 'POST'])
def diet_plan():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender = request.form['gender']
            height = float(request.form['height'])
            weight = float(request.form['weight'])

            bmi = calculate_bmi(weight, height)
            category = classify_bmi(bmi)
            weekly_plan = generate_weekly_plan(category)

            return render_template('diet_result.html', bmi=bmi, category=category, weekly_plan=weekly_plan)
        except KeyError as e:
            return f"Missing form field: {str(e)}"
    return render_template('diet_form.html')




# New Chat functionality
def get_advice(user_input):
    # Example advice generation using TextBlob for sentiment analysis
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "It sounds like you're in a good mood! How about a healthy salad?"
    elif sentiment < 0:
        return "I'm sorry to hear you're feeling down. How about some comfort food?"
    else:
        return "Let's talk about your preferences! What are you in the mood for?"

@app.route("/chat", methods=["GET", "POST"])
def chat():
    reply = None
    if request.method == "POST":
        user_message = request.form.get("message", "").lower()

        # NLP intent detection and advice generation
        if re.search(r"(weight loss|lose weight|burn fat)", user_message, re.IGNORECASE):
            replies = [
        "Try adding more leafy greens and fiber-rich foods to your diet.",
        "Avoid sugary drinks — stick to water or herbal tea.",
        "Include 30 minutes of cardio daily.",
        "Cut down on refined carbs like white bread and pasta.",
        "Aim for a small calorie deficit each day."
    ]
            reply = random.choice(replies)

        elif re.search(r"(gain weight|build muscle|bulk up)", user_message, re.IGNORECASE):
            replies = [
        "Add calorie-dense snacks like nuts or granola.",
        "Don't skip meals — eat every 3-4 hours.",
        "Include strength training at least 3 times a week.",
        "Focus on protein-rich foods like eggs and chicken.",
        "Drink milk or smoothies after workouts."
    ]
            reply = random.choice(replies)
 
        elif re.search(r"(tired|light food|feel sleepy|low energy)", user_message, re.IGNORECASE):
            replies = [
        "Have a banana or some almonds for a quick boost.",
        "Try a small smoothie with spinach and fruit.",
        "Drink more water — dehydration causes fatigue.",
        "Get sunlight and take short walks if feeling sluggish.",
        "Eat whole grains like oats for lasting energy."
    ]
            reply = random.choice(replies)

        elif re.search(r"(healthy|healthy food|good food|nutritious)", user_message, re.IGNORECASE):
            replies = [
        "Grilled veggies and quinoa make a great meal.",
        "Snack on fruits instead of chips.",
        "Balance your plate with proteins, carbs, and fats.",
        "Add seeds like flax or chia to your yogurt or salad.",
        "Use olive oil instead of butter when cooking."
    ]
            reply = random.choice(replies)

        elif re.search(r"(exercise|workout|fitness|gym)", user_message, re.IGNORECASE):
            replies = [
        "A 15-minute walk after meals aids digestion.",
        "Stretch daily to prevent stiffness.",
        "Try combining cardio with weight training.",
        "Rest days are just as important as workouts.",
        "Track your workouts to stay motivated."
    ]
            reply = random.choice(replies)

        elif re.search(r"(meal prep|recipes|cooking ideas)", user_message, re.IGNORECASE):
            replies = [
        "Prepare overnight oats with berries for a quick breakfast.",
        "Cook once, eat twice — double your dinner for lunch tomorrow.",
        "Chop veggies in bulk and store for the week.",
        "Try making wraps with hummus and grilled veggies.",
        "Freeze soups or stews in portions for busy days."
    ]
            reply = random.choice(replies)

        else:
           reply = get_advice(user_message)

    return render_template("advisor_chat.html", reply=reply)

# --- Initialize a local Web server --- #
if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
