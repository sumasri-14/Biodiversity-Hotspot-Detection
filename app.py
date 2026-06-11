from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Biodiversity Hotspot Detection Engine"

if __name__ == "__main__":
    app.run(debug=True)