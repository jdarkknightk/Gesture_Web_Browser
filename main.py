import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Open webcam
cap = cv2.VideoCapture(0)

# Gesture control mappings
ACTION_THRESHOLD = 50  # Adjust sensitivity
SCROLL_THRESHOLD = 40  # Adjust scrolling sensitivity
TAB_SWITCH_THRESHOLD = 60  # Adjust tab switching sensitivity
SCROLL_SPEED = 10  # Adjust scroll speed dynamically

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert frame to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark positions
            index_tip = hand_landmarks.landmark[8]  # Index finger
            thumb_tip = hand_landmarks.landmark[4]  # Thumb
            palm_base = hand_landmarks.landmark[0]  # Palm base
            middle_tip = hand_landmarks.landmark[12]  # Middle finger
            ring_tip = hand_landmarks.landmark[16]  # Ring finger

            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            palm_x, palm_y = int(palm_base.x * w), int(palm_base.y * h)
            middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)
            ring_x, ring_y = int(ring_tip.x * w), int(ring_tip.y * h)

            # Gesture recognition
            if abs(index_x - thumb_x) < ACTION_THRESHOLD and abs(index_y - thumb_y) < ACTION_THRESHOLD:
                pyautogui.press("space")  # Pause/Play
                print("Gesture: Play/Pause")
                time.sleep(0.5)

            if abs(index_x - palm_x) < SCROLL_THRESHOLD:
                scroll_amount = (palm_y - index_y) // SCROLL_SPEED  # Dynamic scrolling
                if scroll_amount > 0:
                    pyautogui.scroll(scroll_amount * 10)  # Scroll Up
                    print("Gesture: Scroll Up")
                elif scroll_amount < 0:
                    pyautogui.scroll(scroll_amount * 10)  # Scroll Down
                    print("Gesture: Scroll Down")
                time.sleep(0.2)

            if ring_x < palm_x - TAB_SWITCH_THRESHOLD:
                pyautogui.hotkey("ctrl", "shift", "tab")  # Previous tab
                print("Gesture: Previous Tab")
                time.sleep(1)

            if ring_x > palm_x + TAB_SWITCH_THRESHOLD:
                pyautogui.hotkey("ctrl", "tab")  # Next tab
                print("Gesture: Next Tab")
                time.sleep(1)

    cv2.imshow("AI Gesture Web Browser", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
