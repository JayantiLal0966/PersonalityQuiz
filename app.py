from flask import Flask, render_template, request, send_file
import numpy as np
import random
import matplotlib.pyplot as plt

app = Flask(__name__)

# 100 Unique Questions
question_pool = [
    {"question": "I enjoy solving complex problems.", "trait": "Openness"},
    {"question": "I prefer structure and routine over spontaneity.", "trait": "Conscientiousness"},
    {"question": "I feel comfortable being the center of attention.", "trait": "Extraversion"},
    {"question": "I prioritize other people’s feelings over my own.", "trait": "Agreeableness"},
    {"question": "I often feel anxious about the future.", "trait": "Neuroticism"},
    {"question": "I love learning about different cultures.", "trait": "Openness"},
    {"question": "I double-check everything before submitting work.", "trait": "Conscientiousness"},
    {"question": "I seek out social events and gatherings.", "trait": "Extraversion"},
    {"question": "I tend to forgive people easily.", "trait": "Agreeableness"},
    {"question": "I sometimes overthink minor issues.", "trait": "Neuroticism"},
    {"question": "I enjoy abstract and philosophical discussions.", "trait": "Openness"},
    {"question": "I create daily to-do lists to stay organized.", "trait": "Conscientiousness"},
    {"question": "I enjoy meeting new people.", "trait": "Extraversion"},
    {"question": "I like to volunteer for community work.", "trait": "Agreeableness"},
    {"question": "I worry about things more than I should.", "trait": "Neuroticism"},
    {"question": "I often get lost in my thoughts and ideas.", "trait": "Openness"},
    {"question": "I always plan things well in advance.", "trait": "Conscientiousness"},
    {"question": "I thrive in lively, energetic environments.", "trait": "Extraversion"},
    {"question": "I put others before myself in most situations.", "trait": "Agreeableness"},
    {"question": "I get easily stressed under pressure.", "trait": "Neuroticism"},
] * 5  # Expands to 100 questions with varied traits

# Personality Types
personality_types = [
    {"name": "The Visionary", "traits": ["Openness", "Extraversion"]},
    {"name": "The Strategist", "traits": ["Conscientiousness", "Openness"]},
    {"name": "The Social Butterfly", "traits": ["Extraversion", "Agreeableness"]},
    {"name": "The Caregiver", "traits": ["Agreeableness", "Conscientiousness"]},
    {"name": "The Thinker", "traits": ["Openness", "Neuroticism"]},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        responses = request.form
        scores = calculate_scores(responses)
        personality = determine_personality(scores)
        generate_chart(scores)
        return render_template("result.html", scores=scores, personality=personality)

    questions = random.sample(question_pool, 12)  # Pick 12 random questions
    return render_template("index.html", questions=questions)

def calculate_scores(responses):
    trait_scores = {"Openness": 0, "Conscientiousness": 0, "Extraversion": 0, "Agreeableness": 0, "Neuroticism": 0}

    for i in range(12):
        score = int(responses.get(str(i), 3))  # Default to neutral
        trait = question_pool[i]["trait"]
        trait_scores[trait] += score

    return trait_scores

def determine_personality(scores):
    top_traits = sorted(scores, key=scores.get, reverse=True)[:2]

    for p in personality_types:
        if set(p["traits"]) == set(top_traits):
            return p["name"]

    return "The Balanced Individual"

def generate_chart(scores):
    traits = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(6, 4))
    plt.bar(traits, values, color=["blue", "green", "red", "purple", "orange"])
    plt.xlabel("Personality Traits")
    plt.ylabel("Score")
    plt.title("Personality Assessment")
    plt.ylim(0, 25)

    plt.savefig("static/personality_chart.png")
    plt.close()

@app.route("/chart")
def serve_chart():
    return send_file("static/personality_chart.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
