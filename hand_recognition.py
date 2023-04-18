import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, static_image_mode=False, max_hands=1, model_complexity=1, detection_con=0.6, track_con=0.6):
        self.mode = static_image_mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        # hands module of mediapipe
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity,self.detection_con, self.track_con)
        # draws the dots
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # takes rgb image and finds hands
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmark, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (0, 150, 255), 3)  # cv2.FILLED
        return lmlist
