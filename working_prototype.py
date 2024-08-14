import face_recognition
import cv2
import numpy as np  # dlib dosen't work well with numpy 2.0 so downgrade is needed

videoCapture = cv2.VideoCapture(0)

myFaceImage = face_recognition.load_image_file("image.png")
myFaceEncoding = face_recognition.face_encodings(myFaceImage)[0]

knownFaces = [
    myFaceEncoding
]

knownFaceNames = [
    ""
]

face_locations = []
face_encodings = []
face_names = []
processThisFrame = True

while 1:
    ret, frame = videoCapture.read()

    if processThisFrame:
        smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)    # resize the frame to 1/4 size for faster processing
        rgbSmallFrame = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgbSmallFrame)
        face_encodings = face_recognition.face_encodings(rgbSmallFrame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(knownFaces, face_encoding)
            name = "Unkown"

            face_distances = face_recognition.face_distance(knownFaces,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = knownFaceNames[best_match_index]

            face_names.append(name)
        
    processThisFrame = not processThisFrame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        #scale back to normal size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left + 6,bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv2.destroyAllWindows()