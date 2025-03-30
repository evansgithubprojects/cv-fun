import numpy as np
from hands import mp_hands, tracked_landmark_roots, tracked_landmarks, get_landmark

def calculate_angle(a, b, c):
  """Computes the angle (in degrees) between screen point vectors AB and BC"""
  # Convert points to numpy arrays
  a = np.array(a)  # MCP
  b = np.array(b)  # PIP (joint)
  c = np.array(c)  # DIP
  
  # Compute vectors
  ab = a - b
  bc = c - b
  
  # Compute dot product and magnitude
  dot_product = np.dot(ab, bc)
  mag_ab = np.linalg.norm(ab)
  mag_bc = np.linalg.norm(bc)
  
  # Compute angle in radians and convert to degrees
  angle = np.arccos(dot_product / (mag_ab * mag_bc))
  return np.degrees(angle)

def landmark_to_tuple(landmark):
  return (landmark.x, landmark.y)

def get_hand_angles(hand_landmarks):
  angles = {root_name: {} for root_name in tracked_landmark_roots}

  for root_name in tracked_landmark_roots:
    for i, landmark_name in enumerate(tracked_landmarks[root_name]):
      if i == 0 or i == len(tracked_landmarks[root_name]) - 1: continue
      index = mp_hands.HandLandmark[landmark_name]
      a = landmark_to_tuple(hand_landmarks.landmark[index - 1])
      b = landmark_to_tuple(hand_landmarks.landmark[index])
      c = landmark_to_tuple(hand_landmarks.landmark[index + 1])
      angle = calculate_angle(a, b, c)
      if np.isnan(angle): return
      angles[root_name][landmark_name] = angle

  return angles