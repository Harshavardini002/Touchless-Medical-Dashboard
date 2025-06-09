import cv2
from hand_detector import HandGestureDetector
import json

# Finger gesture mapping
FINGER_ZONE_MAP = {
    1: "Heart Rate",
    2: "Blood Pressure",
    3: "Oxygen Saturation",
    4: "Temperature",
    5: "Medication"
}

def count_fingers(hand_landmarks, hand_label):
    """
    Count number of extended fingers based on hand landmarks.
    """
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x)
    else:
        fingers.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)

    # Other fingers: tip is above pip joint
    for tip_id in [8, 12, 16, 20]:
        tip = hand_landmarks.landmark[tip_id].y
        pip = hand_landmarks.landmark[tip_id - 2].y
        fingers.append(tip < pip)

    return sum(fingers)

def main():
    cap = cv2.VideoCapture(0)
    detector = HandGestureDetector(max_hands=1)

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = detector.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        h, w, _ = frame.shape
        hover_zone = None

        if results.multi_hand_landmarks and results.multi_handedness:
            hand_landmarks = results.multi_hand_landmarks[0]
            hand_label = results.multi_handedness[0].classification[0].label  # "Right" or "Left"
            detector.draw_hand(frame, hand_landmarks)

            fingers_up = count_fingers(hand_landmarks, hand_label)
            hover_zone = FINGER_ZONE_MAP.get(fingers_up, None)

            cv2.putText(frame, f"Gesture: {fingers_up} fingers - {hover_zone}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            with open("gesture_module/hover.json", "w") as f:
                json.dump({"hover": hover_zone}, f)

        else:
            with open("gesture_module/hover.json", "w") as f:
                json.dump({"hover": None}, f)

        cv2.imshow("Gesture Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
