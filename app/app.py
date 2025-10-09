from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Witaj w aplikacji QuizApp! 🚀"

if __name__ == "__main__":
    app.run(debug=True)