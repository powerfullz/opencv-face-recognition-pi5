import face_recognition
import cv2
import numpy as np  # dlib doesn't work well with numpy 2.0 so downgrade is needed
import os

video = cv2.VideoCapture(0)

# retrieve image from given dir
directory = "/home/powerfullz/face/faces"
os.chdir(directory)
files = os.listdir(directory)
knownFaces = []
knownFaceNames = []

# pre-process given images
progress = 1
total = len(files)
for fileName in files:
    print(f"Processing Faces ({progress}/{total})")
    faceName = fileName.split('.')[0]
    faceImage = face_recognition.load_image_file(fileName)
    faceEncodings = face_recognition.face_encodings(faceImage)
    if faceEncodings:
        knownFaces.append(faceEncodings[0])
        knownFaceNames.append(faceName)
        progress += 1
    else:
        print(f"No face found in {fileName}")

while 1:
    isSucessful, frame = video.read()
    smallFrame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Resize frame for faster processing
    convertedSmallFrame = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2RGB)
    # recognize faces in the frame and convert them to processable encodings
    faceLocations = face_recognition.face_locations(convertedSmallFrame)
    faceEncodings = face_recognition.face_encodings(convertedSmallFrame, faceLocations)

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
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(30) & 0xFF

    if key == 27:
        # ESC Key
        break


cv2.destroyAllWindows()

