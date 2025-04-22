import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,  # Changed to detect 2 hands
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# OpenCV webcam
cap = cv2.VideoCapture(0)

# Tip IDs of fingers (index to pinky)
tip_ids = [4, 8, 12, 16, 20]

def get_hand_gesture(fingers):
    total_fingers = fingers.count(1)
    if total_fingers == 0:
        return "Rock"
    elif total_fingers == 2 and fingers[1] == 1 and fingers[2] == 1:
        return "Scissors"
    elif total_fingers == 5:
        return "Paper"
    return "Unknown"

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # Clear previous text
    cv2.putText(img, "Hand 1: ", (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)
    cv2.putText(img, "Hand 2: ", (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            lm_list = []
            h, w, _ = img.shape

            # Collect landmark positions
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            fingers = []

            if lm_list:
                # Thumb: Compare x (depends on hand side, assume right hand)
                if lm_list[4][1] > lm_list[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers: Compare y
                for tip_id in tip_ids[1:]:
                    if lm_list[tip_id][2] < lm_list[tip_id - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                hand_sign = get_hand_gesture(fingers)

                # Draw results
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(img, f"{hand_sign}", (150, 50 + hand_idx * 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Rock Paper Scissors", img)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
