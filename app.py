from flask import Flask, render_template, request
import requests
import os 
app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/textattack/roberta-base-CoLA"
API_TOKEN = os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None
    text = None
    print("YHello")
    if request.method == "POST":
        print("Post has been hit")
        text = request.form.get("text")
        if text:
            print(text)
            payload = {"inputs": text}
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
                data = response.json()
                print(data)
                prediction = data[0][0]
                confidence = round(prediction["score"] * 100, 2)

                if prediction["label"] == "LABEL_1":
                    result = "✅ Text is grammatically correct"
                else:
                    result = "❌ Text is grammatically incorrect"

            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result, confidence=confidence, text=text)

if __name__ == "__main__":
    app.run(debug=True)
