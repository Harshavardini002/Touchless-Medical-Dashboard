# gesture_module/hand_detector.py

import cv2
import mediapipe as mp

class HandGestureDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def draw_hand(self, image, hand_landmarks):
        self.mp_draw.draw_landmarks(
            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
        )
