from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Hugging Face text generation modeli
generator = pipeline("text-generation", model="gpt2")

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.get_json(force=True, silent=True) or {}
    prompt = data.get("prompt", "Hello world")
    try:
        result = generator(
            prompt,
            max_new_tokens=50,
            num_return_sequences=1
        )
        return jsonify(result[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002, debug=True)
