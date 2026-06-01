from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    project = {
        "name": "My Project",
        "description": "This is a mock website for my project.",
        "status": "In Development"
    }

    return render_template("index.html", project=project)

if __name__ == "__main__":
    app.run(debug=True)