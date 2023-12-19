# List of toast messages paired with their icons
TOAST_MESSAGES = [
    ("Ready to test your knowledge with some tricky questions?", "🧠"),
    ("MCQ Wizard is here to challenge your understanding!", "🔮"),
    ("Think you know your stuff? Let's put it to the test!", "📚"),
    ("It's quiz time! Get those neurons firing!", "⏱️"),
    ("Welcome to the land of quizzes! Are you prepared?", "🌟"),
    ("Time to turn information into answers!", "💡"),
    ("Unlock the mysteries with MCQ Wizard!", "🔐"),
    ("Put your learning to the ultimate test!", "🎯"),
    ("Curious to see how much you've absorbed?", "🤔"),
    ("MCQs incoming! Embrace the challenge.", "🔄"),
    ("Elevate your knowledge with a quiz session!", "🚀"),
    ("MCQs galore! Let's dive into the questions.", "💬"),
    ("Transform your learning into quiz mastery!", "🛠️"),
    ("Ready to ace the MCQ challenge?", "🏅"),
    ("MCQs await! Time to show what you know.", "📝"),
    ("Sharpen your mind with MCQ Wizard!", "✨"),
    ("Think you're prepared? Let's find out!", "🤓"),
    ("MCQs are calling! Are you up for it?", "🔔"),
    ("Curiosity piqued? Let's quiz!", "🔍"),
    ("MCQs at the ready! Let's get started.", "🚦",)
]


def get_random_toast():
    """Returns a random toast message and icon."""
    import random

    return random.choice(TOAST_MESSAGES)
