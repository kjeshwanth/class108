import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):
   if hand_landmarks:
      landmarks=hand_landmarks[handNo].landmark
      
      fingers=[]
      for index in tipIds:
        fingertipy=landmarks[index].y
        fingerbottomy=landmarks[index-2].y
        thumbtipx=landmarks[index].x
        thumbbottomx=landmarks[index-2].x
        #checking if any finger is open or close
        if index !=4:
           if fingertipy<fingerbottomy:
              fingers.append(1)
              print("finger with id",index,"is open")
           if fingertipy>fingerbottomy:
              fingers.append(0)
              print("finger with id",index,"is closed")
        else:
           if thumbtipx>thumbbottomx:
              fingers.append(1)
              print("thumb is opened")

           if thumbtipx<thumbbottomx:
              fingers.append(1)
              print("thumb is closed")


      totalfingers=fingers.count(1)
      
      #display text
      text=f'Fingers:{totalfingers}'
      cv2.putText(image,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)  

# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


#count fingers

while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image,hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
