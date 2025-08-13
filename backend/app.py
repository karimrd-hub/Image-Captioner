from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.image_captioner import caption_image
import boto3
app = Flask(__name__)
CORS(app)  # Allow frontend requests

@app.route("/api/caption", methods=["POST"])
def generate_caption():
    """
    Endpoint to generate an AI caption for an image.
    Expects JSON: { "image": "<base64>", "model": "claude-3.5-sonnet-v1" }
    """
    try:
        data = request.get_json()
        if not data or "image" not in data or "model" not in data:
            return jsonify({"success": False, "error": "Missing 'image' or 'model' in request"}), 400

        image_b64 = data["image"]
        model_key = data["model"]

        # Call the captioning utility
        caption = caption_image(image_b64, model_key)

        
        return jsonify({
            "success": True,
            "caption": caption,
            "model_used": model_key
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
