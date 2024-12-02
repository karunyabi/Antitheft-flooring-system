import cv2
import face_recognition
import os
import numpy as np
import serial
import smtplib
from threading import Thread
from tkinter import Tk, simpledialog
import pygame
import time

# ESP32 Serial Communication
esp32 = serial.Serial('COM3', 115200)  # Adjust COM port
FACE_DIR = "faces"  # Directory to load faces

# Initialize pygame mixer
pygame.mixer.init()
buzzer_sound_path = "buzzer.wav"
buzzer = pygame.mixer.Sound(buzzer_sound_path)

# Alarm state
alarm_active = False

# Load known faces
def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    for person in os.listdir(FACE_DIR):
        person_path = os.path.join(FACE_DIR, person)
        if os.path.isdir(person_path):
            encoding_path = os.path.join(person_path, "face_encoding.npy")
            if os.path.exists(encoding_path):
                known_face_encodings.append(np.load(encoding_path))
                known_face_names.append(person)
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

# Function to send email
def send_email(subject, body):
    sender_email = "enter your email"
    receiver_email = "enter receiver email"
    password = "enter app password" #note that it is not your acc password but your app password
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# Popup for secret code
def get_secret_code():
    root = Tk()
    root.withdraw()
    secret_code = simpledialog.askstring("Alarm Deactivation", "Enter the secret code:")
    root.destroy()
    return secret_code

# Play alarm sound in a loop
def play_alarm():
    while alarm_active:
        if not pygame.mixer.get_busy():  # Check if the sound is already playing
            buzzer.play(-1)  # -1 loops the sound
        time.sleep(0.1)  # Prevent tight looping

# Stop the alarm sound
def stop_alarm():
    buzzer.stop()  # Stop the looping sound
    pygame.mixer.quit()  # Cleanup mixer if needed

# Initialize variables
pressure_detected = False
camera_timeout = 10  # Seconds
camera_last_active_time = None

video_capture = cv2.VideoCapture(0)

try:
    while True:
        # Check for pressure signal
        if esp32.in_waiting > 0:
            signal = esp32.readline().decode().strip()
            if signal == "TRIGGER" and not pressure_detected:
                print("Pressure detected!")
                pressure_detected = True
                camera_last_active_time = time.time()

        # Start processing if pressure was detected
        if pressure_detected:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture frame from camera.")
                continue

            # Perform face recognition
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            face_recognized = False

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    name = known_face_names[matches.index(True)]
                    face_recognized = True
                    print(f"Welcome back, {name}!")
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    print("Unknown face detected!")
                    if not alarm_active:  # Start alarm only once
                        alarm_active = True
                        Thread(target=play_alarm, daemon=True).start()
                        send_email("ALERT!", "Anomaly detected")
                    secret_code = get_secret_code()
                    if secret_code == "1234":
                        print("Alarm deactivated!")
                        alarm_active = False
                        stop_alarm()
                    else:
                        print("Incorrect code!")

            # Update camera display
            cv2.imshow("Video", frame)

            # Reset pressure detection if no pressure and timeout
            if time.time() - camera_last_active_time > camera_timeout:
                print("No pressure detected. Resetting...")
                pressure_detected = False
                alarm_active = False
                stop_alarm()

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Cleanup
    video_capture.release()
    stop_alarm()
    cv2.destroyAllWindows()
