import face_recognition
import cv2
import numpy as np  # dlib doesn't work well with numpy 2.0 so downgrade is needed
import os
from time import sleep

video = cv2.VideoCapture(0)
directory = "/home/powerfullz/face/faces"
os.chdir(directory)

knownFaces = []
knownFaceNames = []
isContinue = False


def recognizeAndEncode(faceName):
    global knownFaceNames, knownFaces
    faceImage = face_recognition.load_image_file(faceName)
    faceEncodings = face_recognition.face_encodings(faceImage)
    if faceEncodings:
        knownFaces.append(faceEncodings[0])
        knownFaceNames.append(faceName)
    else:
        print(f"No face found in {faceName}")


def loadKnownFaces():
    # Load faces from local folder
    # retrieve image from given dir
    global knownFaces, knownFaceNames, isContinue  # Global variables
    isContinue = False  # Halt the recognition process while loading
    sleep(1)  # wait for the recognition process to stop
    files = os.listdir(directory)

    # Clear previous face to start over when user upload a new face.
    knownFaces.clear()
    knownFaceNames.clear()

    progress = 1
    total = len(files)
    for fileName in files:
        print(f"Processing Faces ({progress}/{total})")
        faceName = fileName.split(".")[0]
        recognizeAndEncode(faceName)
        progress += 1
    isContinue = True


def updateFaceInfo(faceName):
    global knownFaces, knownFaceNames, isContinue
    isContinue = False
    sleep(1)
    recognizeAndEncode(faceName)
    isContinue = True


def takePhoto(faceName):
    global isContinue, video
    isContinue = False
    isSucessful, frame = video.read()

    if isSucessful:
        cv2.imwrite(faceName + ".jpg", frame)
        os.rename(faceName + ".jpg", faceName)
        recognizeAndEncode(faceName)
    else:
        print("Camera read error!")

    isContinue = True


loadKnownFaces()  # Initial load


def genFrame():
    global isContinue
    while isContinue:
        isSucessful, frame = video.read()
        smallFrame = cv2.resize(
            frame, (0, 0), fx=0.5, fy=0.5
        )  # Resize frame for faster processing
        convertedSmallFrame = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2RGB)
        # recognize faces in the frame and convert them to processable encodings
        faceLocations = face_recognition.face_locations(convertedSmallFrame)
        faceEncodings = face_recognition.face_encodings(
            convertedSmallFrame, faceLocations
        )

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
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
