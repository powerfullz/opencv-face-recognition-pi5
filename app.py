from flask import Flask, Response, render_template, jsonify, request
from hardwareBackend import genFrame
import os

app = Flask(__name__)


@app.route("/video_feed")
def videoFeed():
    return Response(genFrame(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_faces", methods=["POST"])
def faceUpload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]  # Get the uploaded photo
    name = request.form.get("name")  # Get the input name

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the photo
    file.save(os.path.join("/home/powerfullz/face/faces", name))

    return jsonify({"success": "File uploaded successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
