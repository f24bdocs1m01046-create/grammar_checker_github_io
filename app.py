from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Hugging Face API token
API_URL = "https://api-inference.huggingface.co/models/textattack/roberta-base-CoLA"
API_TOKEN ="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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            payload = {"inputs": text}
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
                data = response.json()

                # Parse the model response
                prediction = data[0][0]  # LABEL_1 or LABEL_0
                confidence = prediction["score"]
                if prediction["label"] == "LABEL_1":
                    result = "✅ Text is grammatically correct"
                else:
                    result = "❌ Text is grammatically incorrect"

            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)
