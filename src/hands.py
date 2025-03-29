import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

tracked_landmark_roots = [
  'PINKY',
  'RING_FINGER',
  'MIDDLE_FINGER',
  'INDEX_FINGER',
  'THUMB'
]
all_landmarks = [landmark for landmark in dir(mp_hands.HandLandmark) if landmark.isupper()]
tracked_landmarks = {}
for root_name in tracked_landmark_roots:
  tracked_landmarks[root_name] = [landmark for landmark in all_landmarks if root_name in landmark]