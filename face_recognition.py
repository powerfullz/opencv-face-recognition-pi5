import face_recognition
import cv2
import numpy as np  # dlib doesn't work well with numpy 2.0 so downgrade is needed
from picamera2 import Picamera2


# Initializing camera
cam = Picamera2()


cam.preview_configuration.main.size = (640, 360)
cam.preview_configuration.main.format = "RGB888"
cam.configure("preview")
cam.start()


# Process known faces
myFace = face_recognition.load_image_file("image.png")  # load a local image file
myFaceEncoding = face_recognition.face_encodings(myFaceImage)[0]


knownFaces = [myFaceEncoding]


knownFaceNames = ["ZhengCheng Lei"]


while 1:
    frame = cam.capture_array()
    convertedFrame = cv2.cvtColor(
        frame, cv2.COLOR_BGR2RGB
    )  # convert to rgb for processing

    # recognize faces in the frame and convert them to processable encodings
    faceLocations = face_recognition.face_locations(convertedFrame)
    faceEncodings = face_recognition.face_encodings(convertedFrame, faceLocations)

    faceNames = []

    for faceEncoding in faceEncodings:
        matches = face_recognition.compare_faces(knownFaces, faceEncoding)
        name = "Unknown"

        faceDistances = face_recognition.face_distance(knownFaces, faceEncoding)
        bestMatchIndex = np.argmin(faceDistances)
        if matches[bestMatchIndex]:
            name = knownFaceNames[bestMatchIndex]

        faceNames.append(name)

    for (top, right, bottom, left), name in zip(faceLocations, faceNames):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(30) & 0xFF

    if key == 27:
        # ESC Key
        break


cam.stop()
cv2.destroyAllWindows()
