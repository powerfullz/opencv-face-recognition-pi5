from flask import Flask, Response, render_template, jsonify, request
from hardwareBackend import genFrame, loadKnownFaces, updateFaceInfo, takePhoto, getFileList, deleteFile
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

    # Save the photo and reload
    file.save(os.path.join("/home/powerfullz/face/faces", name))
    try:
        updateFaceInfo(name)
        return jsonify({"success": "File uploaded and processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reload_faces", methods=["POST"])
def faceReload():
    try:
        loadKnownFaces()
        return jsonify({"success": "Reload completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/take_photo", methods=["POST"])
def captureWebcam():
    faceName = request.form.get("name")

    try:
        takePhoto(faceName)
        return jsonify({"sucess": "Photo taken succesfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/manage_data", methods=["GET"])
def dataManage():
    files = getFileList()
    return jsonify(files)

@app.route("/delete_files", methods=["POST"])
def deletion():
    data = request.get_json()
    filesTodelete = data.get('files', [])
    for file in filesTodelete:
        deleteFile(file)
    return jsonify({"message": "Selected files have been deleted."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
