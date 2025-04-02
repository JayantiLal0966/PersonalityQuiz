from flask import Flask, render_template, request, send_file
import random
import matplotlib.pyplot as plt
import os
import json

app = Flask(__name__)

# 100 Unique Questions (as previously defined)
question_pool = [
    # Your questions go here (same as before)...
]

# Personality Types (same as before)
personality_types = [
    # Your personality types go here (same as before)...
]

# File paths for storing data
hits_file = "hits.json"
users_file = "users.json"

# Initialize data files if they don't exist
if not os.path.exists(hits_file):
    with open(hits_file, 'w') as f:
        json.dump({"hits": 0}, f)

if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        json.dump([], f)

@app.route("/", methods=["GET", "POST"])
def index():
    # Load hit data
    with open(hits_file, 'r') as f:
        hit_data = json.load(f)

    # Increment visit count
    hit_data["hits"] += 1
    with open(hits_file, 'w') as f:
        json.dump(hit_data, f)

    if request.method == "POST":
        # Get email from the form
        email = request.form["email"]
        responses = request.form
        scores = calculate_scores(responses)
        personality = determine_personality(scores)
        generate_chart(scores)

        # Save the user's email and personality to a file
        with open(users_file, 'r') as f:
            users = json.load(f)

        users.append({"email": email, "personality": personality})
        with open(users_file, 'w') as f:
            json.dump(users, f)

        return render_template("result.html", scores=scores, personality=personality, email=email)

    questions = random.sample(question_pool, 12)  # Pick 12 random questions
    return render_template("index.html", questions=questions)

def calculate_scores(responses):
    # Same as before...
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

@app.route("/hits")
def get_hits():
    with open(hits_file, 'r') as f:
        hit_data = json.load(f)
    return f"Total visits: {hit_data['hits']}"

if __name__ == "__main__":
    app.run(debug=True)
