from flask import Flask, request, render_template
import re
from textblob import TextBlob

app = Flask(__name__)

def get_advice(user_input):
    blob = TextBlob(user_input)
    # Basic keyword-based advice
    if 'career' in user_input.lower():
        return "Focus on your passion and build relevant skills for your career."
    elif 'stress' in user_input.lower() or 'tired' in user_input.lower():
        return "Take short breaks, practice mindfulness, and prioritize your mental health."
    elif 'study' in user_input.lower() or 'exam' in user_input.lower():
        return "Stay consistent, make a study plan, and don't forget revision is key."
    elif 'happy' in user_input.lower() or 'motivation' in user_input.lower():
        return "Keep setting small goals. Celebrate little wins to stay motivated!"
    else:
        # Default fallback advice
        return "Stay positive and keep learning. I'm always here to chat!"

@app.route("/chat", methods=["GET", "POST"])
def chat():
    reply = None
    if request.method == "POST":
        user_message = request.form.get("message").lower()

        # Basic NLP: keyword intent detection
        if re.search(r"(weight loss|lose weight|burn fat)", user_message):
            reply = "To lose weight, focus on low-calorie, high-fiber foods like salads, soups, and fruits."
        elif re.search(r"(gain weight|build muscle|bulk up)", user_message):
            reply = "To gain weight, include protein-rich foods like eggs, nuts, and lean meats."
        elif re.search(r"(tired|light food|feel sleepy)", user_message):
            reply = "Feeling tired? A light meal like yogurt with berries or a veggie sandwich might help!"
        elif re.search(r"(healthy|healthy food|good food)", user_message):
            reply = "Healthy choices include steamed vegetables, grilled chicken, and quinoa salads!"
        else:
            # If no keyword matches, use TextBlob advice
            reply = get_advice(user_message)

    return render_template("chat.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=True)

