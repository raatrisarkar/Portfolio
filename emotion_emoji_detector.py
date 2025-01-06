import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

happy_emoji = cv2.imread('happy-face.png', -1)
angry_emoji = cv2.imread('angry.jpeg', -1)  
neutral_emoji = cv2.imread('sad.jpg', -1)  

if happy_emoji is None:
    print("Error: Happy emoji image not found!")
    exit()
if angry_emoji is None:
    print("Error: Angry emoji image not found!")
    exit()
if neutral_emoji is None:
    print("Error: Neutral emoji image not found!")
    exit()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
       
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        is_angry = False

        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25))

        if len(smiles) > 0:
            emotion = 'Happy'
            cv2.putText(frame, 'Happy', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            emoji_resized = cv2.resize(happy_emoji, (w, h))
        else:
            if len(eyes) >= 2:
                emotion = 'Angry'
                is_angry = True
                cv2.putText(frame, 'Angry', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                emoji_resized = cv2.resize(angry_emoji, (w, h))
            else:
                emotion = 'Neutral'
                cv2.putText(frame, 'Neutral', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
                emoji_resized = cv2.resize(neutral_emoji, (w, h))

 
        if emoji_resized.shape[2] == 4:

            alpha_channel = emoji_resized[:, :, 3]
            emoji_rgb = emoji_resized[:, :, :3]

            mask = alpha_channel > 0
            for c in range(0, 3):
                frame[y:y + h, x:x + w, c] = frame[y:y + h, x:x + w, c] * (1 - mask) + emoji_rgb[:, :, c] * mask
        else:
            frame[y:y + h, x:x + w] = cv2.resize(emoji_resized, (w, h))

    cv2.imshow('Emotion Detection with Emoji Mask', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
