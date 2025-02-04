from flask import Flask, request, jsonify, send_file
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Craftland API is running on Vercel!"})

@app.route("/search", methods=["GET"])
def search():
    item_id = request.args.get("id")
    if not item_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    # Fetch the image from the new API
    image_url = f"https://item-id-image.vercel.app/image/{item_id}"
    response = requests.get(image_url)

    if response.status_code == 200:
        # Open the image
        image = Image.open(BytesIO(response.content))

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Define the font and size
        font = ImageFont.load_default()
        text = "IRONMAN"

        # Calculate text size and position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        image_width, image_height = image.size
        text_x = (image_width - text_width) / 2
        text_y = (image_height - text_height) / 2

        # Overlay the text on the image
        draw.text((text_x, text_y), text, fill="white", font=font)

        # Save the modified image
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png')

    else:
        return jsonify({"error": "Failed to fetch image", "status_code": response.status_code})


if __name__ == "__main__":
    app.run(debug=True)