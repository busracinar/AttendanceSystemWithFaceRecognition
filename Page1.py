import face_recognition
import cv2
import numpy as np
import os
import sqlite3


con = sqlite3.connect("attendance.db")
cursor = con.cursor()
video_capture = cv2.VideoCapture("Sinif.mp4")
known_face_numbers = []
known_face_encodings = []
def trainFaces():
    print("---- Training Started ----")
    for root, dirs, files in os.walk("./Students"):
        for filename in files:
            file_result = filename.split("_")
            known_face_numbers.append((file_result[0].split("."))[0])
            image = face_recognition.load_image_file("Students/"+filename)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(image_face_encoding)
            print("Student ID: " + (file_result[0].split("."))[0])
    print("---- Training Completed ----")
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
trainFaces()
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_numbers[best_match_index]
                cursor.execute("UPDATE attendance SET status = ? WHERE student_id = ? ",("Here",name))
                con.commit()
            face_names.append(name)
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.rectangle(frame, (left , bottom - 20), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.4, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
       break
video_capture.release()
cv2.destroyAllWindows()
con.close()
