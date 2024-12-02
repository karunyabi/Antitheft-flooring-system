from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
import cv2
import face_recognition

app = Flask(__name__)

FACE_DIR = "faces"  # Directory to store faces

if not os.path.exists(FACE_DIR):
    os.makedirs(FACE_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        face_file = request.files["face"]
        save_path = os.path.join(FACE_DIR, name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Save the uploaded face image
        face_image_path = os.path.join(save_path, "face.jpg")
        face_file.save(face_image_path)

        # Encode and save the face data
        image = face_recognition.load_image_file(face_image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        np.save(os.path.join(save_path, "face_encoding.npy"), face_encoding)

        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/modify", methods=["GET", "POST"])
def modify():
    people = os.listdir(FACE_DIR)
    if request.method == "POST":
        person_name = request.form["name"]
        action = request.form["action"]
        person_path = os.path.join(FACE_DIR, person_name)
        if action == "delete" and os.path.exists(person_path):
            for file in os.listdir(person_path):
                os.remove(os.path.join(person_path, file))
            os.rmdir(person_path)
        return redirect(url_for("index"))

    return render_template("modify.html", people=people)

if __name__ == "__main__":
    app.run(debug=True)
