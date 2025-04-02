from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Big Five Personality Model
questions = [
    {"question": "I am full of ideas.", "trait": "Openness"},
    {"question": "I get chores done right away.", "trait": "Conscientiousness"},
    {"question": "I am the life of the party.", "trait": "Extraversion"},
    {"question": "I sympathize with others' feelings.", "trait": "Agreeableness"},
    {"question": "I get stressed out easily.", "trait": "Neuroticism"}
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        responses = request.form
        scores = calculate_scores(responses)
        generate_chart(scores)
        return render_template("result.html", scores=scores)

    return render_template("index.html", questions=questions)


def calculate_scores(responses):
    """Convert responses into scores for each personality trait."""
    trait_scores = {"Openness": 0, "Conscientiousness": 0, "Extraversion": 0, "Agreeableness": 0, "Neuroticism": 0}

    for i, question in enumerate(questions):
        score = int(responses.get(str(i), 3))  # Default to neutral
        trait_scores[question["trait"]] += score

    return trait_scores


def generate_chart(scores):
    """Generate a radar chart for personality traits."""
    labels = list(scores.keys())
    values = list(scores.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]  # Repeat the first value to close the radar chart
    angles += angles[:1]

    plt.figure(figsize=(6, 6))
    plt.subplot(polar=True)
    plt.fill(angles, values, color="blue", alpha=0.3)
    plt.plot(angles, values, color="blue", linewidth=2)
    plt.xticks(angles[:-1], labels, color="black", fontsize=12)

    plt.savefig("static/personality_chart.png")
    plt.close()


if __name__ == "__main__":
    app.run(debug=True)
